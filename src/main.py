from logging import warning
from typing import Dict, List
from dotenv import load_dotenv

from .db.redis import RedisDB
from .helpers import HelperFunctions
from .utils import Utils, get_daily_category
from .helpers import TelegramHelper, XHelper
from .constants.product import PRODUCTS_PER_CATEGORY
from .constants.redis_key import PRODUCT_URL_EXPIRE_TIME
from .lib.types import Product, ProductCategories, Websites

load_dotenv()


def main(redis: RedisDB, categories: List[ProductCategories]) -> None:
    """
    Main function of the application that is called when the application is run.
    """
    telegram = TelegramHelper()
    x = XHelper()
    cached_url_key = HelperFunctions.generate_product_url_cache_key()

    urls: Dict[ProductCategories, Dict[Websites, str]
               ] = Utils.generate_urls(categories)

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
            urls = HelperFunctions.get_urls(best_discounted_products)

            for product in best_discounted_products:
                if product is None:
                    return

                Utils.send_message(telegram, x, product)

            redis.add_to_set(cached_url_key, urls, PRODUCT_URL_EXPIRE_TIME)
        except Exception as e:
            warning(
                f"Error occurred while processing category {category.value}: {str(e)}")
            continue


if __name__ == "__main__":
    with RedisDB() as redis_db:
        categories = get_daily_category(redis_db)

        main(redis_db, categories)
