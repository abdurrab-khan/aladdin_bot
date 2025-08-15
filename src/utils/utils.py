from collections import defaultdict
from logging import error
from typing import Dict, List
from selenium.common.exceptions import WebDriverException, TimeoutException

from ..crawler.crawler import Crawler
from ..constants.redis_key import PRODUCT_URL_CACHE_KEY
from .best_discount_analyzer import BestDiscountAnalyzer
from ..constants.url import BASE_URLS, PRODUCT_URL_DETAILS
from ..constants.const import FLIPKART_QUERY_WITH_CAT, FLIPKART_QUERY_WITHOUT_CAT


from ..db.redis import RedisDB
from ..lib.types import Product, Websites, ProductCategories
from ..utils.best_discount_analyzer import BestDiscountAnalyzer

MAX_PRODUCT_TO_SEND = 15

# <================> HELPER FUNCTIONS <================>


def getAmazonUrl(query: str, min_price: int, max_price: int, category_id: str, index: str) -> str:
    base_url = BASE_URLS[Websites.AMAZON]

    return base_url.format(
        query=query,
        index=index,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )


def getFlipkartUrl(query: str, min_price: int, max_price: int, category: str) -> str:
    base_url = BASE_URLS[Websites.FLIPKART]

    return base_url.format(
        category=category,
        query=query,
        min_price=min_price,
        max_price=max_price
    )


class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(urls: Dict[ProductCategories, Dict[Websites, str]], redis: RedisDB) -> List[Product]:
        """
        Get the products from the websites using Selenium.

        args:
            urls: Dict[ProductCategories, Dict[Websites, str]] - The URLs of the products to fetch.

        return:
            Dict[ProductCategories, List[Product]] - The fetched products.
        """
        discount_analyzer = BestDiscountAnalyzer()
        selenium_helper = Crawler(redis, discount_analyzer)

        products_by_cat: List[Product] = []
        all_products: List[Product] = []

        try:
            for category in urls:
                for website, url in urls[category].items():
                    try:
                        fetched_product = selenium_helper.get_product(
                            website, category, url)

                        if fetched_product is None or len(fetched_product) == 0:
                            continue

                        products_by_cat.extend(fetched_product)

                    except (WebDriverException, TimeoutException) as e:
                        error(
                            f"⚠️ Error fetching from {website} ({category.value}): {str(e)}")
                        continue
                    except Exception as e:
                        error(
                            f"⚠️ Unexpected error for {website} ({category.value}): {str(e)}")
                        continue

                # Let's sort the product based on "discount_price"
                if len(products_by_cat) > 0:
                    best_discounted_products = Utils.sort_products(
                        products_by_cat)

                    # Let's cache the products url to prevent re-fetching
                    product_urls = [product["product_url"]
                                    for product in best_discounted_products]

                    redis.add_to_set(
                        f"{PRODUCT_URL_CACHE_KEY}_{category.value}",
                        product_urls,
                        expire_time=60 * 60 * 4 * 24  # 4 days
                    )
                    all_products.extend(best_discounted_products)

                # Let's clear products_by_cat
                products_by_cat = []
        finally:
            selenium_helper.close()
            discount_analyzer.clear_cache()

        return all_products

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
        urls: Dict[ProductCategories, Dict[Websites, str]] = defaultdict(dict)

        for category in categories:
            supported_websites = PRODUCT_URL_DETAILS[category]["website"]
            min_price = PRODUCT_URL_DETAILS[category]["min_price"]
            max_price = PRODUCT_URL_DETAILS[category]["max_price"]
            category_value = category.value

            for website in supported_websites:
                url = ""

                # Based on website generating urls
                if website == Websites.AMAZON:
                    url_props = PRODUCT_URL_DETAILS[category].get(
                        "amazon_url_props", {})

                    category_id = url_props.get("category_id", "")
                    index = url_props.get("index", "")

                    url = getAmazonUrl(
                        category_value, min_price, max_price, category_id, index)
                elif website == Websites.FLIPKART:
                    url_props = PRODUCT_URL_DETAILS[category].get(
                        "flipkart_url_props", {})

                    category_props = url_props.get("category", "")
                    query_base = FLIPKART_QUERY_WITH_CAT if category_props else FLIPKART_QUERY_WITHOUT_CAT
                    query = query_base.format(query=category_value)

                    url = getFlipkartUrl(
                        query, min_price, max_price, category_props)
                elif website == Websites.MYNTRA:
                    url = BASE_URLS[Websites.MYNTRA].format(
                        query=category_value,
                        max_price=max_price
                    )

                urls[category][website] = urls[category][website] = url

        return dict(urls)

    @staticmethod
    def sort_products(products: List[Product]) -> List[Product]:
        """
       Sort the products based on the discount price.
       This function also filters the products based on the discount price.

       args:
           products: Optional[List[Product]] - The list of products to sort.

       return:
           List[Product] - The sorted products.
       """
        if len(products) == 0:
            return []

        sorted_products = (sorted(products, key=lambda x: x["discount_price"]))[
            :MAX_PRODUCT_TO_SEND]

        return sorted_products
