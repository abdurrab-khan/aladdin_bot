from calendar import c
from enum import Enum
from itertools import product
from logging import warning
from re import search
from time import sleep
from typing import Dict, Literal, NotRequired, Optional, TypedDict, Union, List
from urllib.parse import unquote
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class Product(TypedDict):
    product_name: str
    product_price: float
    product_discount: Union[float, None]
    product_rating: Union[float, None]
    product_url: str
    product_image: str
    product_color: NotRequired[str]


class Websites(Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"
    AJIO = "ajio"


Product_key = Literal[
    "product_name",
    "product_price",
    "product_discount",
    "product_rating",
    "product_url",
    "product_image",
    "product_color"
]

REQUIRED_PRODUCT_KEYS = [
    "product_name",
    "product_price",
    "product_image",
    "product_rating",
    "product_url"
]


PRODUCT_DETAILS: Dict[Websites, Dict[Product_key, List[str]]] = {
    Websites.AMAZON: {
        "product_name": ["h2.a-size-base-plus.a-spacing-none"],
        "product_price": ["span.a-price.a-text-price span.a-offscreen"],
        "product_discount": ["span.a-price-whole", "span#priceblock_ourprice"],
        "product_image": ["img.s-image"],
        "product_rating": ["span.a-icon-alt"],
        "product_url": ["a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal", "a.a-link-normal"],
    },
    Websites.FLIPKART: {
        "product_name": ["span.VU-ZEz"],
        "product_price": [r"div.yRaY8j"],
        "product_discount": ["div.Nx9bqj.CxhGGd"],
        "product_image": ["div._8id3KM img"],
        "product_rating": ["div.XQDdHH"],
        "product_url": ["a.rPDeLR"],
    },
    Websites.MYNTRA: {
        "product_name": ["h4.product-product"],
        "product_price": ["div.product-price span .product-strike"],
        "product_discount": ["div.product-price span .product-discountedPrice"],
        "product_image": ["div.product-imageSliderContainer img"],
        "product_rating": ["div.product-ratingsContainer span"],
        "product_url": ["a"],
    },
    Websites.AJIO: None

}

PRODUCT_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: ".s-main-slot.s-result-list",
    Websites.FLIPKART: "div.DOjaWF.gdgoEp:not(.col-2-12):not(.col-12-12), div.DOjaWF.YJG4Cf",
    Websites.MYNTRA: "ul.results-base",
    Websites.AJIO: None,
}

PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div._1sdMkc.LFEi7Z",
    Websites.MYNTRA: "li.product-base",
    Websites.AJIO: None,
}

# FUNCTIONS AND METHODS.
AMAZON_AFFILIATE_ID = "?tag=aladdinloot3-21"
FLIPKART_AFFILIATE_ID = "?affid=admitad&affExtParam1=298614"
MYNTRA_AFFILIATE_ID = "?utm_source=admitad&utm_medium=affiliate"


def retry(max_retries: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for retry_count in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry_count < max_retries - 1:
                        wait_time = 2 ** retry_count
                        warning(
                            f"Attempt {retry_count + 1}/{max_retries} failed: {str(e)}. Retrying in {wait_time} seconds...")
                        sleep(wait_time)
                    else:
                        raise
        return wrapper
    return decorator


def extract_amazon_product_id(url):
    decoded_url = unquote(url)
    pattern = r'/dp/([a-zA-Z0-9]{10})'

    match = search(pattern, decoded_url)

    if match:
        return match.group(1)
    else:
        raise (f"Invalid Amazon URL: {url}")


class SeleniumHelper:
    def __init__(self, website_name: Websites):
        """
        Initialize the WebDriver with Chrome options and navigate to the URL
        """
        self.products: List[Product] = []
        self.website_name = website_name

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        # Initialize the WebDriver
        self.driver = Chrome(options=chrome_options)

        # Set window size to appear more like a real browser
        self.driver.set_window_size(1920, 1080)

    def get_products(self, url: str) -> List[Product] | None:
        """
        Get products details from a given URL and return a list of Product objects.

        args:
            url (str): The URL to scrape products from.

        return:
            List[Product] | None: A list of Product objects or None if no products found.
        """

        try:
            main_container = self.fetch_product_container(url)

            if main_container != None:
                self.extract_products_by_website(main_container)

                return self.products
        except Exception as e:
            raise Exception(f"Error occurred while getting products: {str(e)}")

        finally:
            self.driver.quit()

    def extract_products_by_website(self, main_container: BeautifulSoup):
        """
        Extract product details from the main container based on the website.

        args:
            main_container (BeautifulSoup): The main container element containing product cards.

        return:
            None
        """
        product_cards = main_container.select(
            PRODUCT_CARDS[self.website_name])

        if not product_cards:
            raise Exception("No product cards found.")

        for product_soup in product_cards:
            product_details = {}
            product_url = product_soup.select_one(" ,".join(
                PRODUCT_DETAILS[Websites.FLIPKART]['product_url'])) if self.website_name == Websites.FLIPKART else None
            flipkart_product_soup = self.get_flipkart_data(product_url)

            for key, selectors in PRODUCT_DETAILS[self.website_name].items():
                if self.website_name == Websites.FLIPKART:
                    elements = flipkart_product_soup.select_one(
                        " ,".join(selectors))
                else:
                    elements = product_soup.select_one(" ,".join(selectors))

                if elements is None and key != "product_url":
                    continue

                if key == "product_price" or key == "product_discount":
                    price_data = elements.get_text(strip=True)
                    product_details[key] = self.format_extracted_data(
                        key, price_data)

                elif key == "product_image":
                    product_details[key] = elements["src"]

                elif key == "product_rating":
                    rating_text = elements.get_text(strip=True)
                    product_details[key] = self.format_extracted_data(
                        key, rating_text)

                elif key == "product_url":
                    url = elements['href'] if self.website_name != Websites.FLIPKART else product_url["href"]
                    short_url = self.short_url_with_affiliate_code(url)
                    product_details[key] = short_url

                else:
                    product_details[key] = elements.get_text(strip=True)

            if None in [product_details.get(key) for key in REQUIRED_PRODUCT_KEYS]:
                continue

            predict_deal = "Best Deal"

            if predict_deal == "Best Deal":
                self.products.append(product_details)
            else:
                continue

    def format_extracted_data(self, selector: Product_key, element_data: str) -> Union[float, int, None]:
        """
        Format the extracted data based on the selector type.

        args:
            selector (Product_key): The type of data to format.
            element_data (str): The extracted data to format.

        return:
            Union[float, int, None]: The formatted data.
        """
        if element_data is None:
            return None

        match self.website_name:
            case Websites.AMAZON:
                if selector == "product_price" or selector == "product_discount":
                    return int(float(element_data.replace(",", "").replace("₹", "")))

                elif selector == "product_rating":
                    return float(element_data.split(" ")[0])

            case Websites.FLIPKART:
                if selector == "product_price" or selector == "product_discount":
                    return int(float(element_data.replace(",", "").replace("₹", "")))

                elif selector == "product_rating":
                    return float(element_data)

            case Websites.MYNTRA:
                if selector == "product_price" or selector == "product_discount":
                    return int(float(element_data.replace("Rs.", "").replace(",", "")))

                elif selector == "product_rating":
                    return float(element_data)

            case Websites.AJIO:
                pass

    def short_url_with_affiliate_code(self, url: str) -> str:
        """
        Generate a short URL with the affiliate code based on the website.

        args:
            url (str): The original URL to shorten.

        return:
            str: The short URL with the affiliate code.
        """
        match self.website_name:
            case Websites.AMAZON:
                product_id = extract_amazon_product_id(url)
                short_url = f"https://www.amazon.in/dp/{product_id}/{AMAZON_AFFILIATE_ID}"
                return short_url

            case Websites.FLIPKART:
                short_url = f"https://www.flipkart.com{url.split("?")[0]}/{FLIPKART_AFFILIATE_ID}"
                return short_url

            case Websites.MYNTRA:
                return f"https://www.myntra.com/{url}/{MYNTRA_AFFILIATE_ID}"

            case Websites.AJIO:
                pass
            case _:
                raise ValueError("Invalid website specified")

    def get_flipkart_data(self, url: Optional[str] = None) -> BeautifulSoup | None:
        """
        Get the main container for Flipkart products to get the product details efficiently.

        args:
            url (str): The URL to scrape products from.

        return:
            BeautifulSoup | None: The main container element containing product cards.
        """
        if self.website_name != Websites.FLIPKART or url is None:
            return None
        url = f"https://www.flipkart.com{url["href"].split("?")[0]}"

        main_container = self.fetch_product_container(url)
        if main_container is None:
            raise Exception(
                "Due to some reason does not getting Container.")

        return main_container

    @retry(3)
    def fetch_product_container(self, url: str) -> BeautifulSoup | None:
        """
        Fetches and returns the main product container from the specified website URL.

        args:
            url (str): The URL to scrape products from.

        return:
            BeautifulSoup | None: The main container element containing product cards.
        """
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, PRODUCT_CONTAINER[self.website_name])))

        sleep(random.uniform(0.5, 1.5))

        html = self.driver.page_source

        if html is None:
            raise Exception("Failed to retrieve HTML page content.")

        soup = BeautifulSoup(html, 'html.parser')
        main_container = soup.select_one(PRODUCT_CONTAINER[self.website_name])

        return main_container


if __name__ == "__main__":
    sel = SeleniumHelper(Websites.AMAZON)
    list_products = sel.get_products(
        url="https://www.amazon.in/s?k=jeans&crid=2TGODIWQ3XENE&sprefix=jean%2Caps%2C216&ref=nb_sb_noss_1")

    print(list_products)
