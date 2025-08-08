from pytz import timezone
from random import sample
from typing import List
from logging import info, error
from datetime import datetime, timezone as dt

from ..db.redis import RedisDB
from ..lib.types import ProductCategories
from ..constants.redis_key import PRODUCT_CATEGORY_CACHE_KEY

NUMBER_OF_CATEGORIES_AT_TIME = 3


def get_unique_random_category(client: RedisDB) -> List[ProductCategories]:
    """
    Get a random category from the database that is not in the last time category.

    args:
        category (ProductCategories): The category to get a random value from.
        variable_name (str): The name of the variable to use for the Redis key.
        client (RedisDB): The Redis client.

    return:
        ProductCategories | None: The selected category or None if an error occurs.
    """
    REDIS_KEY = PRODUCT_CATEGORY_CACHE_KEY
    try:
        used_members = client.get_all_member(REDIS_KEY)
        all_category = [key.value for key in list(ProductCategories)]
        available_categories = [
            c for c in all_category if c not in used_members]

        if not available_categories:
            client.remove_set(REDIS_KEY)
            available_categories = all_category

        num_categories = NUMBER_OF_CATEGORIES_AT_TIME if len(
            available_categories) >= NUMBER_OF_CATEGORIES_AT_TIME else len(available_categories)

        selected_value = sample(available_categories, num_categories)
        client.add_to_set(REDIS_KEY, selected_value)

        selected_category = [
            c for c in ProductCategories if c.value in selected_value]

        return selected_category
    except Exception as e:
        error(f"⛔ Error: {e}")
        return []


def get_daily_category(redis: RedisDB) -> List[ProductCategories]:
    """
    Get the daily category based on the current day and time.

    args:
        redis (RedisDB): The Redis client.

    return:
        List[ProductCategories]: The list of categories for the current day.
    """
    utc_now = datetime.now(dt.utc)
    ist_now = utc_now.astimezone(timezone("Asia/Kolkata"))
    hour = ist_now.hour
    hour = 6

    if hour >= 6 and hour <= 8:
        info("🌄 Running morning products (6 AM):")
    elif hour >= 22 and hour <= 23:
        info("🌙 Running night product (10 PM):")
    else:
        info(
            f"⏳ Current time is not 6 AM or 10 PM. No products to run. Current time: {hour}")
        exit(0)

    return get_unique_random_category(redis)
