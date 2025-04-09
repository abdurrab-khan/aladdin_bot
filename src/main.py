from logging import warning
from typing import Dict, List
from .db.redis import RedisDB
from .utils import Utils, get_daily_category
from .helpers import TelegramHelper, XHelper
from .lib.types import Product, Websites, ProductCategories
from .constants.product import COMMON_URLS, PRODUCTS_PER_CATEGORY


def main(redis: RedisDB, categories: List[ProductCategories]) -> None:
    """
    Main function of the application that is called when the application is run.
    """
    websites = [web for web in Websites]
    products: Dict[ProductCategories, List[Product]] = {}
    telegram = TelegramHelper()
    x = XHelper()

    urls = {category: {website: COMMON_URLS[website].format(
        category=category.value) for website in websites} for category in categories}

    try:
        products = Utils.get_products_from_web(urls, redis)
    except Exception as e:
        warning(e)

    for category in products:
        try:
            category_products = products[category]
            product_count = PRODUCTS_PER_CATEGORY[category]
            best_discounted_products = Utils.sort_products(
                product_count, category_products)

            for product in best_discounted_products:
                if product is None:
                    return

                Utils.send_message(telegram, x, product, redis)
        except Exception as e:
            warning(
                f"Error occurred while processing category {category}: {e}")
            continue


if __name__ == "__main__":
    with RedisDB() as redis_db:
        categories = get_daily_category(redis_db)

        main(redis_db, categories)
