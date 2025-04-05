from datetime import datetime
from logging import warning
from src.db.db import RedisDB
from src.lib import ProductCategories
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
        "t-shirt",
        "jeans",
        lambda: get_unique_random_category(random_apparel, "random_apparel),"),
        lambda: get_unique_random_category(
            random_mens_accessories, "random_mens_accessories"),
    ],
    "sunday": [
        "shirt",
        "jeans",
        "t-shirt",
        lambda: get_unique_random_category(random_shoes, "random_shoes"),
    ],
    "tuesday": [
        "shirt",
        "jeans",
        lambda: get_unique_random_category(random_apparel, "random_apparel"),
        lambda: get_unique_random_category(random_shoes, "random_shoes"),
    ],
    "wednesday": [
        "t-shirt",
        "shirt",
        "jeans",
        lambda: get_unique_random_category(
            random_mens_accessories, "random_mens_accessories"),
    ],
    "friday": [
        "t-shirt",
        "shirt",
        "jeans",
        lambda: get_unique_random_category(random_apparel, "random_apparel"),
        lambda: get_unique_random_category(random_shoes, "random_shoes"),
    ],
}


def get_unique_random_category(category: ProductCategories, variable_name: str) -> dict:
    """
    Get a random category from the database that is not in the last time category.

    args:
        group_name (str): The name of the group to get the category from.

    return:
        dict: A random category from the database.
    """
    client = RedisDB()
    REDIS_KEY = f"product_categories_history_{variable_name}"

    try:
        if client.connect():
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
    finally:
        client.disconnect()


def get_daily_category() -> List[ProductCategories] | None:
    current_day = datetime.now().strftime("%A").lower()

    if daily_categories.get(current_day) is None:
        warning(f"Category not found for {current_day}")
        return None

    categories = [
        item() if callable(item) else item for item in daily_categories.get(current_day)
    ]

    return categories
