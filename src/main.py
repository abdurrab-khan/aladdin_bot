from asyncio import run
from typing import List
from dotenv import load_dotenv
from logging import warning, basicConfig, INFO

from .db.supabase import SupaBaseClient
from .db.redis import RedisDB

from .utils import Utils, get_daily_category
from .lib.types import ProductCategories

load_dotenv()

basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s  - %(message)s'
)


async def main(redis: RedisDB, supabase: SupaBaseClient, categories: List[ProductCategories]) -> None:
    """
    Main function of the application that is called when the application is run.
    """

    urls = Utils.generate_urls(categories)

    try:
        products = Utils.get_products_from_web(urls, redis)

        # Let's add products in to the supabase database
        if len(products) > 0:
            supabase.insert_products(products)
        else:
            warning("⚠️ No products found to insert into the database.")

    except Exception as e:
        warning(f"⚠️ Error occurred while fetching products: {str(e)}")

if __name__ == "__main__":
    with RedisDB() as redis_db:
        try:
            supabase = SupaBaseClient().connect()

            if not supabase or not supabase.supabase:
                warning("⚠️ Supabase client is not connected properly.")
                exit(1)

            if not redis_db:
                warning("⚠️ Redis client is not connected properly.")
                exit(1)

            categories = get_daily_category(redis_db)

            run(main(redis_db, supabase, categories))
        except Exception as e:
            warning(f"⚠️ Error connecting to Supabase: {str(e)}")
            supabase = None
            exit(1)
