from pytz import timezone
from random import choice
from typing import List, Union
from logging import warning, info, error
from datetime import datetime, timezone as dt

from ..db.redis import RedisDB
from ..lib.types import ProductCategories
from ..constants.redis_key import PRODUCT_CATEGORY_CACHE_KEY

random_apparel = [
    ProductCategories.CARGO,
    ProductCategories.FOOTWEAR,
    ProductCategories.JACKET,
    ProductCategories.SHORTS,
    ProductCategories.SWEATSHIRTS,
    ProductCategories.TRACKPANT,
    ProductCategories.TROUSER,
]

random_shoes = [
    ProductCategories.CASUAL_SHOES,
    ProductCategories.FORMAL_SHOES,
    ProductCategories.SPORTS_SHOES,
    ProductCategories.SNEAKERS,
]

random_mens_accessories = [
    ProductCategories.WALLET,
    ProductCategories.WATCHES,
    ProductCategories.SUNGLASSES,
    ProductCategories.PERFUME,
]

daily_categories = {
    "saturday": [
        ProductCategories.TSHIRT,
        ProductCategories.JEANS,
        [random_apparel, "random_apparel"]
    ],
    "sunday": [
        ProductCategories.SHIRT,
        ProductCategories.JEANS,
        [random_shoes, "random_shoes"]
    ],
    "tuesday": [
        ProductCategories.SHIRT,
        ProductCategories.JEANS,
        [random_shoes, "random_shoes"]
    ],
    "wednesday": [
        ProductCategories.JEANS,
        [random_mens_accessories, "random_mens_accessories"],
        ProductCategories.TSHIRT,
    ],
    "friday": [
        ProductCategories.SHIRT,
        [random_apparel, "random_apparel"],
        [random_shoes, "random_shoes"],
    ],
}


def get_unique_random_category(category_info: List[Union[ProductCategories, str]], client: RedisDB) -> ProductCategories | None:
    """
    Get a random category from the database that is not in the last time category.

    args:
        category (ProductCategories): The category to get a random value from.
        variable_name (str): The name of the variable to use for the Redis key.
        client (RedisDB): The Redis client.

    return:
        ProductCategories | None: The selected category or None if an error occurs.
    """
    REDIS_KEY = PRODUCT_CATEGORY_CACHE_KEY.format(category=category_info[-1])
    try:
        used_memebers = client.get_all_member(REDIS_KEY)
        all_category = [key.value for key in category_info[0]]
        available_categories = [
            c for c in all_category if c not in used_memebers]

        if not available_categories:
            client.remove_set(REDIS_KEY)
            available_categories = all_category

        selected_value = choice(available_categories)
        client.add_to_set(REDIS_KEY, selected_value)

        selected_category = next(
            c for c in category_info[0] if c.value == selected_value)

        return selected_category
    except Exception as e:
        error(f"⛔ Error: {e}")
        return None


def get_daily_category(redis: RedisDB) -> List[ProductCategories]:
    """
    Get the daily category based on the current day and time.

    args:
        redis (RedisDB): The Redis client.

    return:
        List[ProductCategories]: The list of categories for the current day.
    """
    week_day = datetime.now().strftime("%A").lower()
    utc_now = datetime.now(dt.utc)
    ist_now = utc_now.astimezone(timezone("Asia/Kolkata"))
    hour = ist_now.hour
    hour = 22

    categories_today = daily_categories.get(week_day, [])
    if not categories_today:
        warning(f"❌ Category not found for {week_day.title()}")
        exit(0)

    if hour == 6:
        categories_today = categories_today[:2]
        info("🌄 Running morning products (6 AM):")
    elif hour == 22:
        categories_today = [categories_today[-1]]
        info("🌙 Running night product (10 PM):")
    else:
        info(
            f"⏳ Current time is not 6 AM or 10 PM. No products to run. Current time: {hour}")
        exit(0)

    categories: List[ProductCategories] = []
    for item in categories_today:
        if isinstance(item, list):
            result = get_unique_random_category(item, redis)
            if result is not None:
                categories.append(result)
        else:
            categories.append(item)

    return categories
