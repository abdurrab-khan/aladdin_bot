from json import dumps
from asyncio import run
from typing import Dict, List
from dotenv import load_dotenv
from logging import warning, basicConfig, INFO

from .db.redis import RedisDB
from .helpers import HelperFunctions
from .utils import Utils, get_daily_category
from .constants.product import PRODUCTS_PER_CATEGORY
from .helpers import TelegramHelper, XHelper, MetaHelper
from .constants.redis_key import PRODUCT_URL_EXPIRE_TIME
from .lib.types import Product, ProductCategories, Websites

load_dotenv()

basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
)


async def main(redis: RedisDB, categories: List[ProductCategories]) -> None:
    """
    Main function of the application that is called when the application is run.
    """
    products: Dict[ProductCategories, List[Product]] = {}
    cached_url_key = HelperFunctions.generate_product_url_cache_key()

    urls: Dict[ProductCategories, Dict[Websites, str]
               ] = Utils.generate_urls(categories)

    try:
        products = Utils.get_products_from_web(urls, redis)
    except Exception as e:
        warning(f"⚠️ Error occurred while fetching products: {str(e)}")

    # Initialize helpers (Telegram, X, Meta)
    telegram = TelegramHelper()
    x = XHelper()
    # meta = MetaHelper()

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

                await Utils.send_message(telegram, x,  product)

            redis.add_to_set(cached_url_key, urls, PRODUCT_URL_EXPIRE_TIME)
        except Exception as e:
            warning(
                f"⚠️ Error occurred while processing category {category.value}: {str(e)}")
            continue

# TODO: If Discount is more than 90% then also send Story on Instagram and Facebook.
# TODO: Instead of send image url in (Instagram,Facebook). Send image data and get image url from meta api and send them on instagram.
# TODO: Edit product download image, Add Price Tag on them.

if __name__ == "__main__":
    with RedisDB() as redis_db:
        categories = get_daily_category(redis_db)

        run(main(redis_db, categories))
