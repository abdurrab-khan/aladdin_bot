from datetime import datetime
from logging import warning

random_products = [
    "cargo",
    "footwear",
    "jacket",
    "shorts",
    "pyjama",
    "sweatshirts",
    "track-pant",
    "trouser",
]

random_shoes = [
    "casual-shoes",
    "formal-shoes",
    "sports-shoes",
    "sneakers",
]

random_mens_accessories = [
    "wallet",
    "belt",
    "watches",
    "sunglasses",
    "perfume",
]


daily_categories = {
    "saturday": [
        "t-shirt",
        "jeans",
        # lambda: gettingDistinctCategory("random_products"),
        # lambda: gettingDistinctCategory("random_mens_accessories"),
    ],
    "sunday": [
        "shirt",
        "jeans",
        "t-shirt",
        # lambda: gettingDistinctCategory("random_shoes"),
    ],
    "tuesday": [
        "shirt",
        "jeans",
        # lambda: gettingDistinctCategory("random_products"),
        # lambda: gettingDistinctCategory("random_shoes"),
    ],
    "wednesday": [
        "t-shirt",
        "shirt",
        "jeans",
        # lambda: gettingDistinctCategory("random_mens_accessories"),
    ],
    "friday": [
        "t-shirt",
        "shirt",
        "jeans",
        # lambda: gettingDistinctCategory("random_products"),
        # lambda: gettingDistinctCategory("random_shoes"),
    ],
}


# def gettingDistinctCategory(group_name: str) -> dict:
#     mongo = connectMongo()
#     last_time_category = mongo.get_random_history(group_name)

#     if last_time_category:
#         random_category = findRandomCategory(
#             group_name, last_time_category, mongo)
#         return random_category
#     else:
#         random_category = choice(eval(group_name))
#         category_data = {
#             "group_name": group_name,
#             "category_history": [random_category["category"]],
#         }
#         mongo.insert_random_category(category_data)
#         return random_category


def get_aggregation() -> list:
    current_day = datetime.now().strftime("%A").lower()

    if daily_categories.get(current_day) is None:
        warning(f"Daily categories not found for {current_day}")
        return None

    categories = [
        item() if callable(item) else item for item in daily_categories.get(current_day)
    ]

    print(categories)


get_aggregation()
