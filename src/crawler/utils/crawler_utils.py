
from time import sleep
from typing import List, cast
from random import uniform
from logging import error, info

from ...db.redis import RedisDB
from ..utils.data_processor import DataProcessingHelper
from ..utils.web_driver_utility import WebDriverUtility
from ...lib.types import Product, ProductCategories, Websites
from ...utils.best_discount_analyzer import BestDiscountAnalyzer
from ..utils.css_selector.css_selector import NEXT_BUTTON, PRODUCT_CARDS, PRODUCT_CONTAINER

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebsiteScraper:
    """
    Base class for website-specific scrapers.
    """

    def __init__(self, category: ProductCategories, driver_utility: WebDriverUtility, redis_client: RedisDB, discount_analyzer: BestDiscountAnalyzer, website_name: Websites):
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
        self.website_name: Websites = website_name

    def get_product_container(self, url: str | None) -> WebElement | None:
        """
        Get the main container element containing product cards.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        website = self.website_name

        # Navigate to that url
        if url:
            self.driver_utility.navigate_to(url)

        # Checking whether website is loaded or not
        isLoaded = self._wait_for_page_load()
        if not isLoaded:
            error(f"⌛ Timeout waiting for {website.value} page to load")
            return None

        main_container = self.driver_utility.find_element_with_wait(
            PRODUCT_CONTAINER[website])

        if main_container is None:
            error("⛔ Failed to find the main container for Amazon products.")
            return None

        return main_container

    def extract_products(self, container: WebElement) -> List[Product] | None:
        """
        Extract products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        if self.website_name is None:
            return []

        driver_utility = self.driver_utility

        products: List[Product] = []
        product_cards = driver_utility.find_elements_from_parent(
            container, PRODUCT_CARDS[self.website_name])

        if product_cards is None or len(product_cards) == 0:
            return []

        for card in product_cards:
            product_details = self.extract_product_details(card)

            if product_details is None:
                continue

            products.append(product_details)

        return products

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        website = self.website_name
        driver = self.driver_utility.driver

        if driver is None:
            return False

        try:
            next_page_btn = self.driver_utility.find_elements_from_parent(
                driver, NEXT_BUTTON[website])

            if next_page_btn is None:
                return False

            next_page_btn = next_page_btn[0]

            isBtnWorkable = next_page_btn.is_enabled() and next_page_btn.is_displayed(
            ) or next_page_btn.get_attribute("aria_disabled") == "false"
            return isBtnWorkable
        except NoSuchElementException:
            return False

    def go_to_next_page(self):
        """
        Navigate to the next page of results.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def extract_product_details(self, card: WebElement) -> Product | None:
        product_details = DataProcessingHelper.get_product_details(
            card, self.website_name, self.category)

        # Simple -- Return is "product_details" are None
        if product_details is None:
            return None

        # Extract some details
        url, price = (product_details.get(
            k, None) for k in ("product_url", "price"))

        # Checking in the flipkart is rating and rating count is there or not.
        flipkartHasRating = (self.website_name == Websites.FLIPKART and (
            product_details["rating"] is not None or product_details["rating_count"] is not None))

        # Checking -- Whether product is valid or not.
        isProductValid = (
            DataProcessingHelper.is_product_valid(
                url, price, self.redis_client, self.category)
            and (
                (self.website_name !=
                 Websites.FLIPKART and self.discount_analyzer.is_best_discount(
                     product_details)
                 )
                or (
                    (self.website_name == Websites.FLIPKART and flipkartHasRating
                     and self.discount_analyzer.is_best_discount(product_details))
                ) or (
                    self.website_name == Websites.FLIPKART and not flipkartHasRating
                )
            )
            and (not self.processed_product_urls.__contains__(url))
        )

        if not isProductValid:
            return None

        if product_details['rating'] is not None:
            info(
                f"✅ Best Deal found! 🛍️  {product_details['name']} | 💰 Price: ₹{product_details['price']} | 💰 Discount Price: ₹{product_details['discount_price']} | ⭐ Rating: {product_details['rating']} | 📱 {self.website_name.value}")

        self.processed_product_urls.add(url)

        return product_details

    def _wait_for_page_load(self) -> bool:
        """
        Wait for the page to load completely.
        """
        driver = self.driver_utility.driver

        if driver is None:
            return False

        attempt = 0
        max_retry = 2
        while attempt < max_retry:
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ", ".join(PRODUCT_CONTAINER[self.website_name])))
                )
                sleep(uniform(1.5, 3))

                return True
            except TimeoutException:
                attempt += 1
                base_url_before_ref = driver.current_url
                driver.refresh()

                if base_url_before_ref != driver.current_url:
                    return False

                sleep(uniform(1, 3))

        return False
