from enum import Enum
from time import sleep
from typing import Dict, Literal, NotRequired, TypedDict, Union, List
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


ProductKeys = Literal[
    "product_name", "product_price", "product_discount",
    "product_rating", "product_url", "product_image", "product_color"
]


CSS_SELECTORS_BY_WEBSITE: Dict[Websites, Dict[ProductKeys, List[str]]] = {
    Websites.AMAZON: {
        "product_price": ["span.a-price-whole", "span#priceblock_ourprice"],
        "product_image": ["img.s-image"],
        "product_name": ["h2.a-size-base-plus.a-spacing-none"],
        "product_rating": ["span.a-icon-alt"],
        "product_url": ["a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal", "a.a-link-normal"],
        "product_discount": ["span.a-price.a-text-price span.a-offscreen"],
    },
    Websites.FLIPKART: {
        "price": ["div.Nx9bqj", "div._30jeq3"],
        "image": ["div._8id3KM img", "div.vU5WPQ img"],
        "name": ["span.VU-ZEz", "span._35KyD6"],
        "rating": ["div.XQDdHH", "div._6er70b"],
    },
    Websites.MYNTRA: {

    },
    Websites.AJIO: {},
}

CSS_SELECTORS_BY_WEBSITE_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: ".s-main-slot.s-result-list",
    Websites.FLIPKART: "div._1AtVbE div._2kHMtA",
    Websites.MYNTRA: "div.product-base",
    Websites.AJIO: "div.item-list",
}

CSS_SELECTORS_FOR_PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div._1AtVbE div._2kHMtA",
    Websites.MYNTRA: "div.product-base",
    Websites.AJIO: "div.item-list",
}


class SeleniumHelper:
    def __init__(self):
        """
        Initialize the WebDriver with Chrome options and navigate to the URL
        """
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

    def get_products(self, url: str, website_name):
        try:
            list_products = []
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, CSS_SELECTORS_BY_WEBSITE_CONTAINER[website_name]))
                )

                sleep(random.uniform(1, 3))
            except Exception as wait_error:
                print(f"Wait error: {wait_error}")

            html = self.driver.page_source

            if html is None:
                raise Exception("Something went wrong HTML is not found.")

            soup = BeautifulSoup(html, "html.parser")
            container = soup.select_one(
                CSS_SELECTORS_BY_WEBSITE_CONTAINER[website_name])

            if container != None:
                product_data = self.extract_products_by_website(
                    container, website_name)

                list_products.append(product_data)

            return list_products
        except Exception as e:
            raise Exception(f"Something went wrong: {e}")
        finally:
            self.driver.quit()

    def extract_products_by_website(self, main_container: BeautifulSoup, website_name):
        """
        Get products from a given URL and return a list of Product objects.
        """
        list_products = []
        all_product_cards = main_container.select(
            CSS_SELECTORS_FOR_PRODUCT_CARDS[website_name])

        if not all_product_cards:
            raise Exception("No product cards found.")

        for product in all_product_cards:
            product_info = {}
            for key, selectors in CSS_SELECTORS_BY_WEBSITE[website_name].items():
                elements = product.select_one(" ,".join(selectors))

                if elements:
                    if key == "product_image":
                        product_info[key] = elements["src"]

                    elif key == "product_discount":
                        product_info[key] = float(int(elements.get_text(
                            strip=True).replace(",", "").replace("₹", "")))

                    elif key == "product_rating":
                        rating_text = elements.get_text(strip=True)
                        product_info[key] = float(rating_text.split(
                            " ")[0]) if website_name == Websites.AMAZON else float(rating_text)

                    elif key == "product_price":
                        product_info[key] = int(float(elements.get_text(
                            strip=True).replace(",", "").replace("₹", "")))

                    elif key == "product_url":
                        url = elements['href']
                        product_info[key] = url

                    else:
                        product_info[key] = elements.get_text(strip=True)

                else:
                    product_info[key] = None

            list_products.append(product_info)

        return list_products


if __name__ == "__main__":
    sel = SeleniumHelper()
    list_products = sel.get_products(
        url="https://www.amazon.in/s?k=jeans&page=2&xpid=f8G6VrxZiX5Yv&crid=3DAAZ7JC2UMRK&qid=1743565901&sprefix=jean%2Caps%2C199&ref=sr_pg_1", website_name=Websites.AMAZON)

    print(list_products)
