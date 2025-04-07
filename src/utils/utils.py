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

            print(product)

            if download_image_path is None:
                continue

            if productIndex := mapped_products.get((normalized_name, product["product_discount"])):
                getted_product: Product | ProductVariants = all_products[productIndex]

                if (getted_product.get("variant_name")):
                    all_products[productIndex]['variant_urls'].append(
                        product["product_url"])
                    all_products[productIndex]["variant_images"].append(
                        download_image_path)
                else:
                    all_products[productIndex] = {
                        "variant_name": normalized_name,
                        "variant_price": getted_product["product_price"],
                        "variant_discount": getted_product["product_discount"],
                        "variant_images": [getted_product["product_image"], download_image_path],
                        "variant_urls": [product["product_url"], getted_product["product_url"]],
                    }
            else:
                mapped_products[(
                    normalized_name, product["product_discount"])] = index
                product["product_image"] = download_image_path
                all_products.append(product)

        return all_products

    @staticmethod
    def sort_products(product_count: int, products: Optional[List[Product]] = None) -> List[Product | ProductVariants] | None:
        """
        Sort the products based on the discount price and filter them
        """
        if products is None:
            return None

        sort_products = (sorted(
            products, key=lambda x: x["product_discount"]))[:product_count]

        return Utils.filter_products(sort_products)

    # Send message to Telegram and Twitter
    @staticmethod
    def send_telegram_message(product: Product | ProductVariants) -> None:
        """
        Send a message to the Telegram channel
        """
        message = HelperFunctions.generate_message(
            SendMessageTo.TELEGRAM, product)

        # print("TELEGRAM::- ", message)
        pass

    @staticmethod
    def send_twitter_message(product: Product | ProductVariants) -> None:
        """
        Send a message to the Twitter channel
        """
        message = HelperFunctions.generate_message(
            SendMessageTo.TWITTER, product)

        # print("TWITTER::- ", message)
        pass
