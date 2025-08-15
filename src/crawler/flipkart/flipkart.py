
from time import sleep
from logging import info
from random import uniform
from typing import List, Optional
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
from ..utils.css_selector.css_selector import NEXT_BUTTON, PRODUCT_CARDS, PRODUCT_CONTAINER, PRODUCT_DETAILS


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
        products: List[Product] = []
        isRatingThere = False

        products_cards = driver_utility.find_elements_from_parent(
            container, PRODUCT_CARDS[Websites.FLIPKART])
        if products_cards is None or len(products_cards) == 0:
            return []

        for card in products_cards:
            rating = driver_utility.find_element_from_parent(
                card, PRODUCT_DETAILS[Websites.FLIPKART]['rating'])
            product_details = None

            # If rating is there means we does not have to go and fetch rating
            if rating is not None:
                product_details = self.extract_product_details(card)
                isRatingThere = True
            else:
                if isRatingThere:
                    continue

                product_details = self.extract_product_without_rating(
                    card, driver_utility)
                print(product_details, end="\n\n")

            if product_details is not None:
                products.append(product_details)

        return products

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

    def extract_product_without_rating(self, card: WebElement, driverUtility: WebDriverUtility) -> Product | None:
        """
        Extract Flipkart products if rating is not there.

        Returns:
            List[Product] | None: List of extracted products.
        """
        url_elem = driverUtility.find_element_from_parent(
            card, PRODUCT_DETAILS[Websites.FLIPKART]["product_url"])
        price_elem = driverUtility.find_element_from_parent(
            card, PRODUCT_DETAILS[Websites.FLIPKART]["price"])

        price = DataProcessingHelper.format_extracted_data(
            "price", price_elem, self.website_name)
        url = url_elem.get_attribute('href') if url_elem is not None else None

        # Checking -- Product is Valid or not
        isProductValid = DataProcessingHelper.is_product_valid(
            url, price, self.redis_client, self.category) and not self.processed_product_urls.__contains__(url)

        if not isProductValid:
            return None

        product_details = self.__get_product_details(url)

        # Checking -- Whether product details is there or not
        if product_details is None:
            return None

        # Checking -- Whether product has best_discount or not
        if not self.discount_analyzer.is_best_discount(product_details):
            return None

        info(
            f"✅ Best Deal found! 🛍️  {product_details['name']} | 💰 Price: ₹{product_details['discount_price']} | ⭐ Rating: {product_details['rating']} | flipkart")

        self.processed_product_urls.add(url)

        return product_details

    def __get_product_details(self, url: str | None) -> Optional[Product]:
        """
        Extract product details from the given URL.

        Args:
            url (str): The URL to scrape product details from.

        Returns:
            Product: A dictionary containing product details.
        """
        if url is None:
            return None

        container = self.get_product_container(url)

        if container is None:
            return None

        product_details: Product | None = DataProcessingHelper.get_product_details(
            container, Websites.FLIPKART, self.category)

        if product_details is not None:
            if product_details.get("rating_count", None) is None:
                return None

            product_details["product_url"] = url

        return product_details
