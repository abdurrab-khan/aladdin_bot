from typing import Dict, List, Optional
from ..helpers import HelperFunctions, SeleniumHelper
from ..lib import Product, ProductVariants, Websites, SendMessageTo, ProductCategories, CategoryName, PRODUCTS_COUNT


class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(url: str, website_name: Websites, category: ProductCategories) -> List[Product]:
        """
        Get products from a given URL and return a list of Product objects
        """
        selenium_helper = SeleniumHelper(website_name, category)

        return selenium_helper.get_products(url)

    @staticmethod
    def filter_products(products: Dict[CategoryName, List[Product]]):
        """
        Filter the products based on the product title and price. If the product is same with same price, but different color then keep in single list.
        """
        all_products: List[Product | ProductVariants] = []
        mapped_products = {}

        for cat in products:
            sort_products = sorted(
                products[cat], key=lambda x: x["product_discount"])
            products[cat] = sort_products[:PRODUCTS_COUNT]

            for index, product in enumerate(products[cat]):
                normalized_name = HelperFunctions.normalize_name(
                    product["product_name"])
                download_image_path = HelperFunctions.download_image(
                    product["product_image"])

                if download_image_path is None:
                    return

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
                        all_products[productIndex]["list_images"].append(
                            download_image_path)
                    else:
                        all_products[productIndex] = {
                            "base_name": normalized_name,
                            "list_images": [download_image_path, getted_product["product_image"]],
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
    def sort_products(products: Optional[List[Product]] = None) -> List[Product | ProductVariants] | None:
        """
        Sort the products based on the discount price and filter them
        """
        if products is None:
            return None

        filtered_products = Utils.filter_products(products)

        return filtered_products

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
