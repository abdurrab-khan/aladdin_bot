from random import uniform
from time import sleep
from typing import List
from bs4 import Tag

from ...db.supabase import retry

from ...constants.css_selectors import NEXT_BUTTON
from ...lib.types import Product, Websites
from ..utils.crawler_utils import WebsiteScraper


class AmazonScraper(WebsiteScraper):
    """
    Amazon-specific scraper implementation.
    """

    @retry(3)
    def get_product_container(self, url=None) -> Tag | None:
        """
        Get the main container for Amazon products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(Websites.AMAZON, url)

    def extract_products(self, container: Tag) -> List[Product] | None:
        """
        Extract Amazon products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        return super().extract_products(container, Websites.AMAZON)

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return super().has_next_page(Websites.AMAZON)

    def go_to_next_page(self):
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        if self.driver_utility.driver is None or self.driver_utility is None:
            return False

        current_url = self.driver_utility.driver.current_url
        next_button_elements = self.driver_utility.safe_find_element(
            NEXT_BUTTON[Websites.AMAZON])

        if next_button_elements is None or len(next_button_elements) == 0:
            return False

        next_button_elements[0].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url)

        sleep(uniform(1, 3))
