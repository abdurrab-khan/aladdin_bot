from logging import warning
from typing import Dict, List
from .db.redis import RedisDB
from .utils import Utils, get_daily_category
from .helpers import TelegramHelper, XHelper
from .lib.types import Product, Properties, Websites, ProductCategories
from .constants.url import BASE_URLS, AMAZON_URL_PROPERTIES
from .constants.product import PRICE_LIMITS, PRODUCTS_PER_CATEGORY


def main(redis: RedisDB, categories: List[ProductCategories]) -> None:
    """
    Main function of the application that is called when the application is run.
    """
    websites = [web for web in Websites]
    products: Dict[ProductCategories, List[Product]] = {}
    telegram = TelegramHelper()
    x = XHelper()

    # urls = {category: {website: BASE_URLS[website].format(
    #     category=category.value) for website in websites} for category in categories}
    urls: Dict[ProductCategories, Dict[Websites, str]] = {}
    for category in categories:
        urls[category] = {}
        for website in websites:
            if website == Websites.AMAZON:
                urls[category][website] = BASE_URLS[website].format(
                    query=category,
                    index=AMAZON_URL_PROPERTIES[category][Properties.INDEX],
                    category_id=AMAZON_URL_PROPERTIES[category][Properties.CATEGORY_ID],
                    max_price=PRICE_LIMITS[website]
                )
            else:
                urls[category][website] = BASE_URLS[website].format(
                    query=category.value, max_price=PRICE_LIMITS[website]
                )

    print(urls)
    exit(0)

    try:
        products = Utils.get_products_from_web(urls, redis)
    except Exception as e:
        warning(e)

    print(f"Products: {products}")

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
