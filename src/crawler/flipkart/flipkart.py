
from bs4 import Tag
from time import sleep
from logging import info
from random import uniform
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from ...lib.types import Product, Websites
from ..utils.crawler_utils import WebsiteScraper
from ..utils.data_processor import DataProcessingHelper
from ...constants.css_selectors import NEXT_BUTTON, PRODUCT_CARDS, PRODUCT_DETAILS


class FlipkartScraper(WebsiteScraper):
    """
    Flipkart-specific scraper implementation.
    """

    def get_product_container(self, url=None) -> Tag | None:
        """
        Get the main container for Flipkart products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(Websites.FLIPKART, url)

    def extract_products(self, container: Tag) -> List[Product] | None:
        """
        Extract Flipkart products from the container.

        Args:
            container (Tag): The container element.

        Returns:
            List[Product] | None: List of extracted products.
        """
        products: List[Product] = []
        products_soup = container.select(PRODUCT_CARDS[Websites.FLIPKART])

        for soup in products_soup:
            url = soup.select_one(
                " ,".join(PRODUCT_DETAILS[Websites.FLIPKART]["product_url"]))
            price = DataProcessingHelper.format_extracted_data(
                "price",
                soup.select_one(
                    " ,".join(PRODUCT_DETAILS[Websites.FLIPKART]["price"])),
                Websites.FLIPKART
            )
            formatted_url = DataProcessingHelper.format_extracted_data(
                "product_url", url, Websites.FLIPKART)

            # Ensure price is of correct type (float | None)
            actual_price = price if isinstance(
                price, (float, int, type(None))) else None

            # Checking --- Whether Product is Valid or None
            if not DataProcessingHelper.is_product_valid(str(formatted_url), actual_price, None, self.redis_client, self.category):
                continue

            # Check --- Whether give product is already there
            if self.processed_product_urls.__contains__(formatted_url):
                continue

            url_href = str(url.get("href")) if url is not None else None

            product_details: Product | None = self.__get_product_details(
                url_href)

            # Checking -- Whether product is None
            if product_details is None:
                continue

            products.append(product_details)
            self.processed_product_urls.add(product_details["product_url"])

            info(
                f"✅ Best Deal found! 🛍️  {product_details['name']} | 💰 Price: ₹{product_details['discount_price']} | ⭐ Rating: {product_details['rating']} | flipkart")

        return products

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        try:
            next_page_btn = self.driver_utility.safe_find_element(
                NEXT_BUTTON[Websites.FLIPKART])

            if next_page_btn is None:
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
        current_url = self.driver_utility.driver.current_url
        next_page_btn = self.driver_utility.safe_find_element(
            NEXT_BUTTON[Websites.FLIPKART])

        if len(next_page_btn) == 1:
            next_page_btn[0].click()
        else:
            next_page_btn[1].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url)

        sleep(uniform(1, 3))

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

        product_url = f"https://www.flipkart.com{url.split('?')[0]}"

        container = self.get_product_container(product_url)

        if container is None:
            return None

        product_details: Product | None = DataProcessingHelper.get_product_details(
            container, Websites.FLIPKART, self.category)

        if product_details is not None:
            if product_details.get("rating_count", None) is None:
                return None

            product_details["product_url"] = product_url

        return product_details
