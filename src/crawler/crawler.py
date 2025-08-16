
from time import sleep
from typing import List
from logging import error, warning

from ..db.redis import RedisDB
from ..constants.url import MAX_PRODUCTS_PER_WEBSITE
from .utils.web_driver_utility import WebDriverUtility
from selenium.webdriver.common.by import By
from ..lib.types import Product, ProductCategories, Websites
from ..utils.best_discount_analyzer import BestDiscountAnalyzer
from .utils.website_crawler_factory import WebsiteScraperFactory


class Crawler:
    """
    Main class to coordinate the scraping operations across different websites.
    """

    def __init__(self, redis: RedisDB, discount_analyzer: BestDiscountAnalyzer):
        """
        Initialize the SeleniumHelper with necessary components.

        Args:
            redis (RedisDB): The Redis client instance.
        """
        self.redis_client = redis
        self.discount_analyzer = discount_analyzer
        self.driver_utility = WebDriverUtility()

    def get_product(self, website_name: Websites, category: ProductCategories, url: str) -> List[Product] | None:
        """
        Get products details from a given URL for a specific website and category.

        Args:
            website_name (Websites): The website to scrape from.
            category (ProductCategories): The product category.
            url (str): The URL to scrape products from.

        Returns:
            List[Product] | None: A list of Product objects or None if no products found.
        """
        scraper = WebsiteScraperFactory.get_scraper(
            website_name, category, self.driver_utility, self.redis_client, self.discount_analyzer)

        all_products = []
        page_counter = 1
        empty_page_count = 0

        try:
            while len(all_products) < MAX_PRODUCTS_PER_WEBSITE:
                url: str | None = url if page_counter == 1 else None
                container = scraper.get_product_container(url)

                if container is None:
                    return all_products if all_products else None

                page_products = scraper.extract_products(container)

                #  Check if we have less than 15 products and page_counter is greater than 20
                # This is to prevent scraping too many pages if not enough products are found
                if len(all_products) < 15 and page_counter >= 20:
                    warning(
                        f"⚠️  Less than 15 products found on page {page_counter} for {website_name.value}. Stopping further scraping.")
                    break

                # Prevent infinite loop if no products are found
                if page_products is None or len(page_products) == 0:
                    empty_page_count += 1

                    if empty_page_count >= 8:
                        warning(
                            f"⚠️  No products found on page {page_counter} for {website_name.value}. Stopping further scraping.")
                        break

                else:
                    if empty_page_count > 0:
                        empty_page_count = 0

                    # Add new product into the list
                    all_products.extend(page_products)

                if len(all_products) > MAX_PRODUCTS_PER_WEBSITE:
                    all_products = all_products[:MAX_PRODUCTS_PER_WEBSITE]
                    break

                if not scraper.has_next_page():
                    break

                go_next_page = scraper.go_to_next_page()

                if go_next_page == False:
                    break

                page_counter += 1
                sleep(1)

            return all_products
        except Exception as e:
            error(f"Error scraping {website_name} products: {str(e)}")
            return all_products if all_products else None

    def close(self):
        """
        Clean up resources.
        """
        self.driver_utility.close_driver()
