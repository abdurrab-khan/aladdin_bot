from logging import error
from typing import Dict, List
from selenium.common.exceptions import WebDriverException, TimeoutException

from .best_discount_analyzer import BestDiscountAnalyzer

from ..constants.product import PRICE_LIMITS
from ..constants.url import AMAZON_URL_PROPERTIES, BASE_URLS
from ..db.supabase import SupaBaseClient


from ..db.redis import RedisDB
from ..helpers import SeleniumHelper
from ..lib.types import Properties, Websites, ProductCategories
from ..utils.best_discount_analyzer import BestDiscountAnalyzer


class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(urls: Dict[ProductCategories, Dict[Websites, str]], redis: RedisDB, supabase: SupaBaseClient):
        """
        Get the products from the websites using Selenium.

        args:
            urls: Dict[ProductCategories, Dict[Websites, str]] - The URLs of the products to fetch.

        return:
            Dict[ProductCategories, List[Product]] - The fetched products.
        """
        discount_analyzer = BestDiscountAnalyzer()
        selenium_helper = SeleniumHelper(redis, discount_analyzer)

        try:
            for category in urls:
                for website, url in urls[category].items():
                    try:
                        fetched_product = selenium_helper.get_product(
                            website, category, url)

                        if fetched_product is not None and len(fetched_product) > 0:
                            supabase.insert_products(fetched_product)

                    except (WebDriverException, TimeoutException) as e:
                        error(
                            f"⚠️ Error fetching from {website} ({category.value}): {str(e)}")
                        continue
                    except Exception as e:
                        error(
                            f"⚠️ Unexpected error for {website} ({category.value}): {str(e)}")
                        continue
        finally:
            selenium_helper.close()
            discount_analyzer.clear_cache()

    @staticmethod
    def generate_urls(categories: List[ProductCategories]) -> Dict[ProductCategories, Dict[Websites, str]]:
        """
        Generate the URLs for the products based on the categories.
        This function uses the BASE_URLS and AMAZON_URL_PROPERTIES constants to generate the URLs.

        args:
            categories: List[ProductCategories] - The list of categories to generate URLs for.

        return:
            Dict[ProductCategories, Dict[Websites, str]] - The generated URLs.
        """
        urls: Dict[ProductCategories, Dict[Websites, str]] = {}
        for category in categories:
            urls[category] = {}
            query = category.value

            for website in Websites:
                base_url = BASE_URLS[website]
                price_limit = PRICE_LIMITS[category]

                if website == Websites.AMAZON:
                    urls[category][website] = base_url.format(
                        query=query,
                        index=AMAZON_URL_PROPERTIES[category][Properties.INDEX],
                        category_id=AMAZON_URL_PROPERTIES[category][Properties.CATEGORY_ID],
                        max_price=price_limit
                    )
                else:
                    urls[category][website] = base_url.format(
                        query=query,
                        index=AMAZON_URL_PROPERTIES[category][Properties.INDEX],
                        category_id=AMAZON_URL_PROPERTIES[category][Properties.CATEGORY_ID],
                        max_price=price_limit
                    )

        return urls
