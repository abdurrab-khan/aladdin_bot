
from time import sleep
from typing import List
from random import uniform
from logging import error, info
from bs4 import BeautifulSoup, Tag

from ...db.redis import RedisDB
from ..utils.data_processor import DataProcessingHelper
from ..utils.web_driver_utility import WebDriverUtility
from ...lib.types import Product, ProductCategories, Websites
from ...utils.best_discount_analyzer import BestDiscountAnalyzer
from ...constants.css_selectors import NEXT_BUTTON, PRODUCT_CARDS, PRODUCT_CONTAINER

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebsiteScraper:
    """
    Base class for website-specific scrapers.
    """

    def __init__(self, category: ProductCategories, driver_utility: WebDriverUtility, redis_client: RedisDB, discount_analyzer: BestDiscountAnalyzer):
        """
        Initialize the website scraper.

        Args:
            driver_utility (WebDriverUtility): The WebDriver utility instance.
            redis_client (RedisDB): The Redis client instance.
        """

        self.processed_product_urls = set()
        self.category = category
        self.driver_utility = driver_utility
        self.redis_client = redis_client
        self.discount_analyzer = discount_analyzer
        self.data_helper = DataProcessingHelper()

    def get_product_container(self, website_name: Websites, url: str | None = None) -> Tag | None:
        """
        Get the main container element containing product cards.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        if url:
            self.driver_utility.navigate_to(url)

        isLoaded = self._wait_for_page_load(website_name)
        if not isLoaded:
            error(f"⌛ Timeout waiting for {website_name.value} page to load")
            return None

        if self.driver_utility.driver is None:
            error("⛔ WebDriver is not initialized.")
            return None

        html = self.driver_utility.driver.page_source
        if html is None:
            error("⛔ Failed to retrieve HTML page content.")
            return None

        soup = BeautifulSoup(html, 'html.parser')
        main_container = soup.select_one(PRODUCT_CONTAINER[website_name])

        if main_container is None:
            error("⛔ Failed to find the main container for Amazon products.")
            return None

        return main_container

    def extract_products(self, container: Tag, website_name: Websites) -> List[Product] | None:
        """
        Extract products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        products: List[Product] = []
        products_soup = container.select(PRODUCT_CARDS[website_name])

        if not products_soup:
            return None

        for soup in products_soup:
            product_details: Product | None = DataProcessingHelper.get_product_details(
                soup, website_name, self.category)

            if product_details is None:
                continue

            # Checking -- Whether product is valid or not
            # >> Check Whether product is recently sended.
            # >> Product price is more that max price.
            # >> Review count should be greater than 10.
            if not DataProcessingHelper.is_product_valid(
                product_details.get("product_url"),
                product_details.get("price"),
                product_details.get("rating_count"),
                self.redis_client, self.category,
            ):
                continue

            # Check -- Whether product is valid or not
            # >> Check by using some ml algorithms.
            # >> Check whether already fetched or not.
            if not (self.discount_analyzer.is_best_discount(product_details)) or self.processed_product_urls.__contains__(product_details["product_url"]):
                continue

            products.append(product_details)
            self.processed_product_urls.add(product_details["product_url"])

            info(
                f"✅ Best Deal found! 🛍️  {product_details['name']} | 💰 Price: ₹{product_details['discount_price']} | ⭐ Rating: {product_details['rating']} | {website_name.value}")

        return products

    def has_next_page(self, website_name: Websites) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        try:
            next_page_btn = self.driver_utility.safe_find_element(
                NEXT_BUTTON[website_name])

            if next_page_btn is None:
                return False

            next_page_btn = next_page_btn[0]

            return next_page_btn.is_enabled() and next_page_btn.is_displayed() or next_page_btn.get_attribute("aria_disabled") == "false"
        except NoSuchElementException:
            return False

    def go_to_next_page(self):
        """
        Navigate to the next page of results.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _wait_for_page_load(self, website_name: Websites) -> bool:
        """
        Wait for the page to load completely.
        """
        attempt = 0
        max_retry = 2
        while attempt < max_retry:
            try:
                WebDriverWait(self.driver_utility.driver, 8).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, PRODUCT_CONTAINER[website_name]))
                )
                sleep(uniform(1.5, 3))

                return True
            except TimeoutException:
                attempt += 1
                base_url_before_ref = self.driver_utility.driver.current_url
                self.driver_utility.driver.refresh()

                if base_url_before_ref != self.driver_utility.driver.current_url:
                    return False

                sleep(uniform(1, 3))

        return False
