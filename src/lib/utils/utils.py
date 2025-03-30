from typing import List, Optional
from ...helpers import HelperFunctions, retry, SeleniumHelper
from ...lib import Product, ProductSearchResult, ProductVariants, Websites


class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(url: str, website_name: Websites) -> ProductSearchResult | None:
        """
        Get products from a given URL and return a list of Product objects 
        """

        max_retry = 3

        @retry(max_retry)
        def get_products(url: str, website_name: Websites) -> List[Product] | None:
            selenium_helper = SeleniumHelper()
            return selenium_helper.get_products(url, website_name)

        return get_products(url, website_name)

    @staticmethod
    def filter_products(products: List[Product]) -> List[Product | ProductVariants] | None:
        """
        Filter the products based on the product title and price. If the product is same with same price, but different color then keep in single list.
        """
        return

    @staticmethod
    def sort_products(products: Optional[List[Product]] = None) -> List[Product | ProductVariants] | None:
        """
        Sort the products based on the discount price and filter them
        """
        if products is None:
            return None

        sorted_products = sorted(products, key=lambda p: p["product_discount"])
        filtered_products = HelperFunctions.filter_products(sorted_products)

        return filtered_products

    @staticmethod
    def download_images(products: Product | ProductVariants) -> str | List[str]:
        """
        Download the images of the product
        """
        images_path = None

        if isinstance(product, Product):
            pass
        elif isinstance(product, ProductVariants):
            pass

        return images_path

    # Send message to Telegram and Twitter
    @staticmethod
    def send_telegram_message(product: Product | ProductVariants, image_path: str | List[str]) -> None:
        """
        Send a message to the Telegram channel
        """
        message = HelperFunctions.generate_message("telegram", product)

        pass

    @staticmethod
    def send_twitter_message(product: Product | ProductVariants, image_path: str | List[str]) -> None:
        """
        Send a message to the Twitter channel
        """
        message = HelperFunctions.generate_message("twitter", product)

        pass
