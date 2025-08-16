from time import sleep
from typing import List
from random import uniform
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement

from ..utils.web_driver_utility import WebDriverUtility
from ...db.redis import RedisDB
from ...lib.types import ProductCategories
from ...utils.best_discount_analyzer import BestDiscountAnalyzer
from ..utils.css_selector.css_selector import NEXT_BUTTON, PRODUCT_CARDS
from ...lib.types import Product, Websites

from ..utils.crawler_utils import WebsiteScraper


class MyntraScraper(WebsiteScraper):
    """
    Myntra-specific scraper implementation.
    """

    def __init__(self, category: ProductCategories, driver_utility: WebDriverUtility, redis_client: RedisDB, discount_analyzer: BestDiscountAnalyzer, website_name: Websites):
        super().__init__(category, driver_utility,
                         redis_client, discount_analyzer, website_name)

    def get_product_container(self, url=None) -> WebElement | None:
        """
        Get the main container for Myntra products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(url)

    def extract_products(self, container: WebElement) -> List[Product] | None:
        """
        Extract Myntra products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        return super().extract_products(container)

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return super().has_next_page()

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
        old_products = self.driver_utility.find_elements_from_parent(
            driver, PRODUCT_CARDS[self.website_name])
        next_btn = self.driver_utility.find_element_from_parent(
            driver, NEXT_BUTTON[Websites.MYNTRA])

        if old_products is None or next_btn is None:
            return False

        old_products_set = set(old_products)

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url or set(d.find_elements(
                By.CSS_SELECTOR, PRODUCT_CARDS[Websites.MYNTRA])) != old_products_set)

        sleep(uniform(1, 3))
