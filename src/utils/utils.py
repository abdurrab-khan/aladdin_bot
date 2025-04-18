from typing import Dict, List, Optional

from ..db.redis import RedisDB
from ..constants.product import PRICE_LIMITS
from ..constants.url import BASE_URLS, AMAZON_URL_PROPERTIES
from ..helpers import HelperFunctions, SeleniumHelper, TelegramHelper, XHelper, MetaHelper
from ..lib.types import Product, ProductVariants, Websites, SendMessageTo, ProductCategories, Properties


class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(urls: Dict[ProductCategories, Dict[Websites, str]], redis: RedisDB) -> Dict[ProductCategories, List[Product]]:
        """
        Get the products from the websites using Selenium.

        args:
            urls: Dict[ProductCategories, Dict[Websites, str]] - The URLs of the products to fetch.

        return:
            Dict[ProductCategories, List[Product]] - The fetched products.
        """
        selenium_helper = SeleniumHelper(redis)
        products: Dict[ProductCategories, List[Product]] = {}

        try:
            for category in urls:
                for website, url in urls[category].items():
                    fetched_product = selenium_helper.get_all_products(
                        website, category, url)

                    if fetched_product is None or not fetched_product:
                        continue

                    if products.get(category):
                        products[category].extend(fetched_product)
                    else:
                        products[category] = fetched_product

        except Exception as e:
            raise Exception(str(e))
        finally:
            selenium_helper.driver.quit()

        return products

    @staticmethod
    def filter_products(products: List[Product]) -> List[Product | ProductVariants]:
        """
        Filter the products based on the discount price and group them by name.
        This function also downloads the images of the products.

        args:
            products: List[Product] - The list of products to filter.

        return:
            List[Product | ProductVariants] - The filtered products.
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
        Sort the products based on the discount price.
        This function also filters the products based on the discount price.

        args:
            product_count: int - The number of products to return.
            products: Optional[List[Product]] - The list of products to sort.

        return:
            List[Product | ProductVariants] | None - The sorted products.
        """
        if products is None:
            return None

        sort_products = (sorted(
            products, key=lambda x: x["product_discount"]))[:product_count]

        return Utils.filter_products(sort_products)

    @staticmethod
    async def send_message(telegram: TelegramHelper, x: XHelper, product: Product | ProductVariants) -> None:
        """
        Send message to the user via Telegram and X (formerly Twitter).

        args:
            telegram: TelegramHelper - The Telegram helper instance.
            x: XHelper - The X helper instance.
            product: Product | ProductVariants - The product to send the message about.

        return:
            None
        """
        image_path: str | List[str] = product.get("product_image") or product.get(
            "variant_images")

        for destination in SendMessageTo:
            message: str = HelperFunctions.generate_message(
                destination, product)

            if destination == SendMessageTo.TELEGRAM:
                await telegram.send_message(message, image_path)

            elif destination == SendMessageTo.X:
                x.send_message(message, image_path)

        HelperFunctions.delete_images(image_path)

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
