from asyncio import run
from typing import Dict, List
from dotenv import load_dotenv
from logging import warning, basicConfig, INFO

from .db.redis import RedisDB
from .helpers import HelperFunctions
from .utils import Utils, get_daily_category
from .lib.types import Product, ProductCategories, Websites

load_dotenv()

basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s  - %(message)s'
)


async def main(redis: RedisDB, categories: List[ProductCategories]) -> None:
    """
    Main function of the application that is called when the application is run.
    """
    urls: Dict[ProductCategories, Dict[Websites, str]
               ] = Utils.generate_urls(categories)

    try:
        Utils.get_products_from_web(urls, redis)
    except Exception as e:
        warning(f"⚠️ Error occurred while fetching products: {str(e)}")

if __name__ == "__main__":
    with RedisDB() as redis_db:
        categories = get_daily_category(redis_db)

        run(main(redis_db, categories))
