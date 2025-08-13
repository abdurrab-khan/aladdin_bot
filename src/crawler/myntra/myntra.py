from bs4 import Tag
from time import sleep
from typing import List
from random import uniform
from selenium.webdriver.common.by import By

from ..utils.css_selector.css_selector import NEXT_BUTTON, PRODUCT_CARDS
from ...lib.types import Product, Websites

from ..utils.crawler_utils import WebsiteScraper


class MyntraScraper(WebsiteScraper):
    """
    Myntra-specific scraper implementation.
    """

    def get_product_container(self, url=None) -> Tag | None:
        """
        Get the main container for Myntra products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(Websites.MYNTRA, url)

    def extract_products(self, container: Tag) -> List[Product] | None:
        """
        Extract Myntra products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        return super().extract_products(container, Websites.MYNTRA)

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return super().has_next_page(Websites.MYNTRA)

    def go_to_next_page(self):
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        current_url = self.driver_utility.driver.current_url
        old_product = set(self.driver_utility.safe_find_element(
            PRODUCT_CARDS[Websites.MYNTRA]))

        self.driver_utility.safe_find_element(
            NEXT_BUTTON[Websites.MYNTRA])[0].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url or set(d.find_elements(
                By.CSS_SELECTOR, PRODUCT_CARDS[Websites.MYNTRA])) != old_product)

        sleep(uniform(1, 3))
