from datetime import datetime
from logging import warning
from ..db.redis import RedisDB
from ..lib.types import ProductCategories
from typing import List
from random import choice

random_apparel = [
    ProductCategories.CARGO,
    ProductCategories.FOOTWEAR,
    ProductCategories.JACKET,
    ProductCategories.SHORTS,
    ProductCategories.PYJAMA,
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
    ProductCategories.BELT,
    ProductCategories.WATCHES,
    ProductCategories.SUNGLASSES,
    ProductCategories.PERFUME,
]

daily_categories = {
    "saturday": [
        ProductCategories.TSHIRT,
        ProductCategories.JEANS,
        lambda: get_unique_random_category(random_apparel, "random_apparel"),
        lambda: get_unique_random_category(
            random_mens_accessories, "random_mens_accessories"),
    ],
    "sunday": [
        ProductCategories.SHIRT,
        ProductCategories.JEANS,
        # ProductCategories.TSHIRT,
        # [random_shoes, "random_shoes"]
    ],
    "tuesday": [
        ProductCategories.SHIRT,
        ProductCategories.JEANS,
        lambda: get_unique_random_category(random_apparel, "random_apparel"),
        lambda: get_unique_random_category(random_shoes, "random_shoes"),
    ],
    "wednesday": [
        ProductCategories.TSHIRT,
        ProductCategories.SHIRT,
        ProductCategories.JEANS,
        lambda: get_unique_random_category(
            random_mens_accessories, "random_mens_accessories"),
    ],
    "friday": [
        ProductCategories.TSHIRT,
        ProductCategories.SHIRT,
        ProductCategories.JEANS,
        lambda: get_unique_random_category(random_apparel, "random_apparel"),
        lambda: get_unique_random_category(random_shoes, "random_shoes"),
    ],
}


def get_unique_random_category(category: ProductCategories, variable_name: str, client: RedisDB) -> ProductCategories | None:
    """
    Get a random category from the database that is not in the last time category.

    args:
        category (ProductCategories): The category to get a random value from.
        variable_name (str): The name of the variable to use for the Redis key.
        client (RedisDB): The Redis client.

    return:
        ProductCategories | None: The selected category or None if an error occurs.
    """
    REDIS_KEY = f"product_categories_history_{variable_name}"

    try:
        used_memebers = client.get_all_member(REDIS_KEY)
        all_category = [key.value for key in category]

        available_categories = [
            c for c in all_category if c not in used_memebers]

        if not available_categories:
            client.remove_set(REDIS_KEY)
            available_categories = all_category

        selected_value = choice(available_categories)
        client.add_to_set(REDIS_KEY, selected_value)

        selected_category = next(
            c for c in category if c.value == selected_value)

        return selected_category
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_daily_category(redis: RedisDB) -> List[ProductCategories]:
    # current_day = datetime.now().strftime("%A").lower()
    current_day = "sunday"

    if daily_categories.get(current_day) is None:
        warning(f"Category not found for {current_day}")
        exit(0)

    categories: List[ProductCategories] = []
    for item in daily_categories.get(current_day):
        if isinstance(item, list):
            result = get_unique_random_category(item[0], item[1], redis)
            if result is not None:
                categories.append(result)
        else:
            categories.append(item)

    return categories
