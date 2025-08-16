
from logging import info
from time import sleep
from random import uniform
from typing import Dict, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from ..utils.web_driver_utility import WebDriverUtility
from ...db.redis import RedisDB
from ...lib.types import ProductCategories
from ...utils.best_discount_analyzer import BestDiscountAnalyzer

from ...lib.types import Product, Websites
from ..utils.crawler_utils import WebsiteScraper
from ..utils.data_processor import DataProcessingHelper
from ..utils.css_selector.css_selector import NEXT_BUTTON, PRODUCT_CARDS, PRODUCT_DETAILS


class FlipkartScraper(WebsiteScraper):
    """
    Flipkart-specific scraper implementation.
    """

    def __init__(self, category: ProductCategories, driver_utility: WebDriverUtility, redis_client: RedisDB, discount_analyzer: BestDiscountAnalyzer, website_name: Websites):
        super().__init__(category, driver_utility,
                         redis_client, discount_analyzer, website_name)

    def get_product_container(self, url: str | None) -> WebElement | None:
        """
        Get the main container for Flipkart products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(url)

    def extract_products(self, container: WebElement) -> List[Product]:
        """
        Extract Flipkart products from the container.

        Args:
            container (Tag): The container element.

        Returns:
            List[Product] | None: List of extracted products.
        """
        driver_utility = self.driver_utility

        isProductHasRating = False
        products: List[Product] = []
        product_without_rating: List[Product] = []

        products_cards = driver_utility.find_elements_from_parent(
            container, PRODUCT_CARDS[Websites.FLIPKART])
        if products_cards is None or len(products_cards) == 0:
            return []

        # Extract all basic data from product card
        for card in products_cards:
            product_details = None

            product_details = self.extract_product_details(card)

            # append if product details is not None
            if product_details is not None:
                products.append(product_details)

        # Let's extract product rating and rating count
        for product in products:
            if product["rating"] is not None:
                isProductHasRating = True
                break

            product_rating_details = self.extract_product_rating(
                product["product_url"], driver_utility)

            if product_rating_details is None:
                continue

            product["rating"] = product_rating_details["rating"]
            product["rating_count"] = product_rating_details["rating_count"]

            if not self.discount_analyzer.is_best_discount(product):
                continue

            info(
                f"✅ Best Deal found! 🛍️  {product['name']} | 💰 Price: ₹{product['price']} | 💰 Discount Price: ₹{product['discount_price']} | ⭐ Rating: {product["rating"]} | 📱 {self.website_name.value}")

            product_without_rating.append(product)

        return products if isProductHasRating else product_without_rating

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        driver = self.driver_utility.driver

        if driver is None:
            return False

        try:
            next_page_btn = self.driver_utility.find_elements_from_parent(
                driver, NEXT_BUTTON[Websites.FLIPKART])

            if next_page_btn is None or len(next_page_btn) == 0:
                return False

            if len(next_page_btn) == 1:
                if next_page_btn[0].find_element(
                        By.CSS_SELECTOR, "span").get_property("innerHTML") == "Previous":
                    return False

                next_page_btn = next_page_btn[0]
            else:
                next_page_btn = next_page_btn[1]

            return next_page_btn.is_enabled() and next_page_btn.is_displayed() or next_page_btn.get_attribute("aria_disabled") == "false"
        except NoSuchElementException:
            return False

    def go_to_next_page(self):
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        driver = self.driver_utility.driver

        if driver is None:
            return False

        current_url = driver.current_url
        next_page_btn = self.driver_utility.find_elements_from_parent(
            driver, NEXT_BUTTON[Websites.FLIPKART])

        if next_page_btn is None or len(next_page_btn) == 0:
            return False

        if len(next_page_btn) == 1:
            next_page_btn[0].click()
        else:
            next_page_btn[1].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url)

        sleep(uniform(1, 3))

    def extract_product_rating(self, url: str, driverUtility: WebDriverUtility) -> Dict | None:
        """
        Extract Flipkart products rating and rating count.

        Returns:
            List[Product] | None: List of extracted products.
        """
        # Extract product container
        container = self.get_product_container(url)

        # Simply return None if container is None
        if container is None:
            return None

        product_rating = driverUtility.find_element_from_parent(
            container, PRODUCT_DETAILS[self.website_name]["rating"])
        product_rating_count = driverUtility.find_element_from_parent(
            container, PRODUCT_DETAILS[self.website_name]["rating_count"])

        rating = DataProcessingHelper.format_extracted_data(
            "rating", product_rating, self.website_name)
        rating_count = DataProcessingHelper.format_extracted_data(
            "rating_count", product_rating_count, self.website_name)

        if rating is None or rating_count is None:
            return None

        return {"rating": rating, "rating_count": rating_count}
