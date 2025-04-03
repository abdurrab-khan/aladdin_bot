from calendar import c
from enum import Enum
from itertools import product
from re import search
from time import sleep
from typing import Dict, Literal, NotRequired, TypedDict, Union, List
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
    "product_name", "product_price", "product_discount",
    "product_rating", "product_url", "product_image", "product_color"
]

REQUIRED_PRODUCT_KEYS = ["product_name", "product_price",
                         "product_image", "product_rating", "product_url"]


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
        "product_name": ["a.wjcEIp"],
        "product_price": ["div.yRaY8j"],
        "product_discount": ["div.Nx9bqj"],
        "product_image": ["a.VJA3rP div._4WELSP img"],
        "product_rating": ["div.XQDdHH"],
        "product_url": ["a.VJA3rP"],
    },
    Websites.MYNTRA: {
        "product_name": ["h4.product-product"],
        "product_price": ["div.product-price span .product-strike"],
        "product_discount": ["div.product-price span .product-discountedPrice"],
        "product_image": ["div.product-imageSliderContainer img"],
        "product_rating": ["div.product-ratingsContainer span"],
        "product_url": ["a"],
    }
}

PRODUCT_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: ".s-main-slot.s-result-list",
    Websites.FLIPKART: "div.DOjaWF.gdgoEp",
    Websites.MYNTRA: "ul.results-base",
    Websites.AJIO: "div.item-list",
}

PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div.slAVV4",
    Websites.MYNTRA: "li.product-base",
    Websites.AJIO: "div.item-list",
}

# FUNCTIONS AND METHODS.
AMAZON_AFFILIATE_ID = "?tag=aladdinloot3-21"
FLIPKART_AFFILIATE_ID = "?affid=admitad&affExtParam1=298614"
MYNTRA_AFFILIATE_ID = "?utm_source=admitad&utm_medium=affiliate"


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

    def get_products(self, url: str):
        try:
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, PRODUCT_CONTAINER[self.website_name]))
                )

                sleep(random.uniform(1, 2))

            except Exception as wait_error:
                print(f"Wait error: {wait_error}")

            html = self.driver.page_source

            if html is None:
                raise Exception("Something went wrong HTML is not found.")

            soup = BeautifulSoup(html, "html.parser")

            container = soup.select_one(
                PRODUCT_CONTAINER[self.website_name]) if self.website_name != Websites.FLIPKART else soup.select_one(f"{PRODUCT_CONTAINER[self.website_name]}:not(.col-2-12):not(.col-12-12)")

            if container != None:
                product_data = self.extract_products_by_website(container)

                return product_data
        except Exception as e:
            raise Exception(f"Something went wrong: {e}")
        finally:
            self.driver.quit()

    def extract_products_by_website(self, main_container: BeautifulSoup):
        """
        Get products from a given URL and return a list of Product objects.
        """
        list_products = []
        all_product_cards = main_container.select(
            PRODUCT_CARDS[self.website_name])

        if not all_product_cards:
            raise Exception("No product cards found.")

        for product in all_product_cards:
            product_info = {}
            for key, selectors in PRODUCT_DETAILS[self.website_name].items():
                elements = product.select_one(" ,".join(selectors))

                if elements:
                    if key == "product_price" or key == "product_discount":
                        price_data = elements.get_text(strip=True)
                        product_info[key] = self.get_element_value_by_selector(
                            key, price_data)

                    elif key == "product_image":
                        product_info[key] = elements["src"]

                    elif key == "product_rating":
                        rating_text = elements.get_text(strip=True)
                        product_info[key] = self.get_element_value_by_selector(
                            key, rating_text)

                    elif key == "product_url":
                        url = elements['href']
                        short_url = self.short_url_with_affiliate_code(url)
                        product_info[key] = short_url

                    else:
                        product_info[key] = elements.get_text(strip=True)
                else:
                    continue

            if None in [product_info.get(key) for key in REQUIRED_PRODUCT_KEYS]:
                predict_deal = "Best Deal"

                if predict_deal == "Best Deal":
                    list_products.append(product_info)
                else:
                    continue
            else:
                continue

        return list_products

    def get_element_value_by_selector(self, selector: Product_key, element_data: str):
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
                    pass

                elif selector == "product_rating":
                    pass

            case Websites.MYNTRA:
                if selector == "product_price" or selector == "product_discount":
                    return int(float(element_data.replace("Rs.", "").replace(",", "")))

                elif selector == "product_rating":
                    return float(element_data)

            case Websites.AJIO:
                pass

    def short_url_with_affiliate_code(self, url: str) -> str:
        """
        Shorten the URL and add affiliate code to the URL
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
                return f"https://www.myntra.com{url}/{MYNTRA_AFFILIATE_ID}"
            case Websites.AJIO:
                pass
            case _:
                raise ValueError("Invalid website specified")


if __name__ == "__main__":
    sel = SeleniumHelper(Websites.MYNTRA)
    list_products = sel.get_products(
        url="https://www.myntra.com/jeans")

    print(list_products)
