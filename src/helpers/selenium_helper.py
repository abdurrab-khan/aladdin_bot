from re import search
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import unquote
from logging import info
from random import choice, uniform
from selenium.webdriver import Chrome
from typing import Optional, Union, List
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ..db.redis import RedisDB
from .helper_functions import retry
from ..lib.ml_model.predict_deal import predict_deal
from ..lib.types import Websites, ProductCategories, ProductKey, Product
from ..constants.css_selectors import NEXT_BUTTON, PRODUCT_CONTAINER, PRODUCT_DETAILS, PRODUCT_CARDS
from ..constants.product import REQUIRED_PRODUCT_KEYS, PRICE_LIMITS, MAX_PRODUCTS_PER_WEBSITE
from ..constants.url import AMAZON_AFFILIATE_ID, FLIPKART_AFFILIATE_ID, MYNTRA_AFFILIATE_ID


def extract_amazon_product_id(url) -> str | None:
    decoded_url = unquote(url)
    pattern = r'/dp/([a-zA-Z0-9]{10})'

    match = search(pattern, decoded_url)

    if match:
        return match.group(1)
    else:
        return None


class SeleniumHelper:
    def __init__(self, redis: RedisDB):
        """
            Initialize the WebDriver with Chrome options and navigate to the URL
            """
        self.redis: RedisDB = redis
        self.website_name: Websites | None = None
        self.category: ProductCategories | None = None
        self.processed_product_urls = set()

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
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
        chrome_options.add_argument(f"user-agent={choice(user_agents)}")

        self.driver = Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)

    def get_all_products(self, website_name: Websites, category: ProductCategories, url: str, ) -> List[Product] | None:
        """
        Get products details from a given URL and return a list of Product objects.

        args:
            url (str): The URL to scrape products from.

        return:
            List[Product] | None: A list of Product objects or None if no products found.
        """
        self.website_name = website_name
        self.category = category
        page_counter = 1
        self.processed_product_urls = set()
        products: List[Product] = []

        while len(products) <= MAX_PRODUCTS_PER_WEBSITE:
            try:
                main_container = self.fetch_product_container(
                    url, "container", page_counter)

                if main_container is None:
                    break

                extracted_products = self.extract_products_by_website(
                    main_container)
                products.extend(extracted_products)

                if not self.has_next_page():
                    break

                self.go_to_next_page()
                page_counter += 1
            except Exception as e:
                raise Exception(
                    f"Error occurred while getting products: {str(e)}")

        return products

    def extract_products_by_website(self, main_container: BeautifulSoup) -> List[Product]:
        """
        Extract product details from the main container based on the website.

        args:
            main_container (BeautifulSoup): The main container element containing product cards.

        return:
            List[Product]: A list of Product objects extracted from the main container.
        """
        products: List[Product] = []
        product_cards = main_container.select(PRODUCT_CARDS[self.website_name])

        if not product_cards:
            return []

        for product_soup in product_cards:
            if self.website_name != Websites.FLIPKART and product_soup == None:
                continue

            product_details: Product = {}
            product_url = product_soup.select_one(" ,".join(
                PRODUCT_DETAILS[self.website_name]['product_url']))
            product_price = product_soup.select_one(
                " ,".join(PRODUCT_DETAILS[self.website_name]["product_price"]))

            if not self.is_product_valid(product_price, product_url):
                continue

            flipkart_soup = self.get_flipkart_data(product_url)

            if self.website_name == Websites.FLIPKART and flipkart_soup == None:
                continue

            for key, selectors in PRODUCT_DETAILS[self.website_name].items():
                try:
                    soup = product_soup if self.website_name != Websites.FLIPKART else flipkart_soup
                    elements = soup.select_one(" ,".join(selectors))

                    if self.website_name == Websites.FLIPKART and key == "product_url":
                        element = product_url
                    else:
                        element = elements

                    formatted_data = self.format_extracted_data(key, element)
                    if formatted_data != None:
                        product_details[key] = formatted_data
                except:
                    continue

            if not all([product_details.get(key) for key in REQUIRED_PRODUCT_KEYS]):
                continue

            if self.processed_product_urls.__contains__(product_details["product_url"]):
                continue

            prediction = predict_deal(product_details)
            if prediction['prediction'] == "Best Deal":
                self.processed_product_urls.add(product_details["product_url"])

                products.append(product_details)
                info(
                    f"✅ Best Deal found! 🛍️  {product_details['product_name']} | 💰 Price: ₹{product_details['product_discount']} | ⭐ Rating: {product_details['product_rating']} | {self.website_name.value}")
            else:
                continue

        return products

    def get_flipkart_data(self, url: Optional[str] = None) -> BeautifulSoup | None:
        """
        Get the main container for Flipkart products to get the product details efficiently.

        args:
            url (str): The URL to scrape products from.

        return:
            BeautifulSoup | None: The main container element containing product cards.
        """
        if self.website_name != Websites.FLIPKART or url == None:
            return None

        url = f"https://www.flipkart.com{url["href"].split("?")[0]}"

        main_container = self.fetch_product_container(url, "product")
        if main_container is None:
            return None

        return main_container

    @retry(3)
    def fetch_product_container(self, url: str, request_type, page_counter: int | None = None) -> BeautifulSoup:
        """
        Fetches and returns the main product container from the specified website URL.

        args:
            url (str): The URL to scrape products from.

        return:
            BeautifulSoup | None: The main container element containing product cards.
        """
        if (page_counter and page_counter == 1) or request_type == "product":
            self.driver.get(url)

        attempt = 0
        while attempt < 2:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, PRODUCT_CONTAINER[self.website_name])))
                sleep_time = uniform(
                    1.2, 3) if request_type == "product" else uniform(3, 5)
                sleep(sleep_time)

                break
            except TimeoutException:
                attempt += 1
                self.driver.refresh()
                sleep(uniform(1, 3))

        html = self.driver.page_source

        if html is None:
            raise Exception("Failed to retrieve HTML page content.")

        soup = BeautifulSoup(html, 'html.parser')
        main_container = soup.select_one(PRODUCT_CONTAINER[self.website_name])

        return main_container

    # Helper functions ⬇️
    def format_extracted_data(self, key: ProductKey, element_data: BeautifulSoup | None) -> Union[float, int, str, None]:
        """
        Format the extracted data based on the selector type.

        args:
            selector (Product_key): The type of data to format.
            element_data (BeautifulSoup | None): The extracted data to format.

        return:
            Union[float, int, str, None]: The formatted data.
        """
        if element_data == None:
            return None

        if key == "product_image_url" or key == "product_url":
            attr = "href" if key == "product_url" else "src"
            element = element_data[attr]

            return element if key == "product_image_url" else self.short_url_with_affiliate_code(element)
        else:
            element = element_data.get_text(strip=True)

        match self.website_name:
            case Websites.AMAZON:
                if key == "product_price" or key == "product_discount":
                    return int(float(element.replace(",", "").replace("₹", "")))

                elif key == "product_rating":
                    return float(element.split(" ")[0])

            case Websites.FLIPKART:
                if key == "product_price" or key == "product_discount":
                    return int(float(element.replace(",", "").replace("₹", "")))

                elif key == "product_rating":
                    return float(element)

            case Websites.MYNTRA:
                if key == "product_price" or key == "product_discount":
                    return int(float(element.replace("Rs.", "").replace(",", "")))

                elif key == "product_rating":
                    return float(element)

        return element

    def short_url_with_affiliate_code(self, url: str) -> str:
        """
        Generate a short URL with the affiliate code based on the website.

        args:
            url (str): The original URL to shorten.

        return:
            str: The short URL with the affiliate code.
        """
        formatted_url = None
        match self.website_name:
            case Websites.AMAZON:
                product_id = extract_amazon_product_id(url)
                formatted_url = f"https://www.amazon.in/dp/{product_id}/{AMAZON_AFFILIATE_ID}" if product_id is not None else None

            case Websites.FLIPKART:
                formatted_url = f"https://www.flipkart.com{url.split("?")[0]}/{FLIPKART_AFFILIATE_ID}"

            case Websites.MYNTRA:
                formatted_url = f"https://www.myntra.com/{url}/{MYNTRA_AFFILIATE_ID}"

            case _:
                raise ValueError("Invalid website specified")

        return unquote(formatted_url, encoding="utf-8")

    def is_product_valid(self, price: BeautifulSoup, url: BeautifulSoup) -> bool:
        if price is None or url is None:
            return False

        product_price = self.format_extracted_data("product_price", price)
        product_url = self.format_extracted_data("product_url", url)

        if product_price <= PRICE_LIMITS[self.category]:
            if self.redis.is_url_cached(product_url):
                return False
            else:
                return True
        else:
            return False

    def safe_find_element(self, selector) -> Optional[WebElement]:
        """
        Safely find an element using a selector.

        args:
            selector (str): The CSS selector to find the element.

        return:
            WebElement | None: The found element or None if not found.
        """
        try:
            return self.driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return None

    def go_to_next_page(self):
        current_url = self.driver.current_url
        old_product = set(self.driver.find_elements(
            By.CSS_SELECTOR, PRODUCT_CARDS[self.website_name]))

        self.driver.find_element(
            By.CSS_SELECTOR, NEXT_BUTTON[self.website_name]).click()

        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url != current_url or set(d.find_elements(By.CSS_SELECTOR, PRODUCT_CARDS[self.website_name])) != old_product)

        sleep(uniform(1, 3))

    def has_next_page(self) -> bool:
        try:
            next_button = self.safe_find_element(
                NEXT_BUTTON[self.website_name])

            if next_button is None:
                return False

            return next_button.is_enabled() or next_button.is_displayed() or next_button.get_attribute("aria-disabled") == "false"
        except NoSuchElementException:
            return False
