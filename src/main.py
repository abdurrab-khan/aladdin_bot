from typing import Dict, List

from .lib import Websites, ProductCategories, Product, COMMON_URLS, PRODUCTS_COUNT
from .utils import Utils, get_daily_category
from logging import warning


def main(categories):
    """
    Main function of the application that is called when the application is run.
    """
    websites = [web for web in Websites]
    products: Dict[ProductCategories, List[Product]] = {}

    urls = {category: {website: COMMON_URLS[website].format(
        category=category.value) for website in websites} for category in categories}

    try:
        products = Utils.get_products_from_web(urls)
    except Exception as e:
        warning(f"Error occurred while fetching products from websites: {e}")

    for category in products:
        category_products = products[category]
        product_count = PRODUCTS_COUNT[category]

        best_discounted_products = Utils.sort_products(
            product_count, category_products)

        for product in best_discounted_products:
            if product is None:
                return

            Utils.send_telegram_message(product)
            Utils.send_twitter_message(product)


if __name__ == "__main__":
    categories = get_daily_category()

    main(categories)
