from typing import Dict, List, Optional
from ..helpers import HelperFunctions, SeleniumHelper
from ..lib import Product, ProductVariants, Websites, SendMessageTo, ProductCategories, PRODUCTS_COUNT
from logging import error


class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(urls: Dict[ProductCategories, Dict[Websites, str]]) -> Dict[ProductCategories, List[Product]]:
        """
        Get products from a given URL and return a list of Product objects
        """
        selenium_helper = SeleniumHelper()
        products: Dict[ProductCategories, List[Product]] = {}

        try:
            for category in urls:
                for website, url in urls[category].items():
                    products[category] = selenium_helper.get_products(
                        website, category, url)
        except Exception as e:
            error(f"An error occurred while getting products: {e}")
        finally:
            selenium_helper.driver.quit()

        return products

    @staticmethod
    def filter_products(products: List[Product]) -> List[Product | ProductVariants]:
        """
        Filter the products based on the product title and price. If the product is same with same price, but different color then keep in single list.
        """
        all_products: List[Product | ProductVariants] = []
        mapped_products = {}

        for index, product in enumerate(products):
            normalized_name = HelperFunctions.normalize_name(
                product["product_name"])
            download_image_path = HelperFunctions.download_image(
                product["product_image"])

            if download_image_path is None:
                continue

            updated_product = {
                **product,
                "product_color": HelperFunctions.get_product_color(product["product_name"]),
            }
            if productIndex := mapped_products.get((normalized_name, product["product_discount"])):
                productIndex -= 1
                getted_product = all_products[productIndex]
                if (getted_product.get("variants")):
                    all_products[productIndex]['variants'].append(
                        updated_product)
                    all_products[productIndex]["product_image"].append(
                        download_image_path)
                else:
                    all_products[productIndex] = {
                        "base_name": normalized_name,
                        "product_image": [download_image_path, getted_product["product_image"]],
                        "variants": [
                            getted_product,
                            updated_product
                        ]
                    }
            else:
                mapped_products[(
                    normalized_name, product["product_discount"])] = index + 1
                updated_product["product_image"] = download_image_path
                all_products.append(updated_product)

        return all_products

    @staticmethod
    def sort_products(product_count: int, products: Optional[List[Product]] = None) -> List[Product | ProductVariants] | None:
        """
        Sort the products based on the discount price and filter them
        """
        if products is None:
            return None

        sort_products = sorted(
            products, key=lambda x: x["product_discount"])[:product_count]

        return Utils.filter_products(sort_products)

    # Send message to Telegram and Twitter
    @staticmethod
    def send_telegram_message(product: Product | ProductVariants, image_path: str | List[str]) -> None:
        """
        Send a message to the Telegram channel
        """
        message = HelperFunctions.generate_message(
            SendMessageTo.TELEGRAM, product)

        print("TELEGRAM::- ", message)

        pass

    @staticmethod
    def send_twitter_message(product: Product | ProductVariants, image_path: str | List[str]) -> None:
        """
        Send a message to the Twitter channel
        """
        message = HelperFunctions.generate_message(
            SendMessageTo.TELEGRAM, product)

        print("TWITTER::- ", message)
        pass
