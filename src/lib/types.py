from enum import Enum
from typing import TypedDict, Literal


class Product(TypedDict):
    name: str
    price: float
    discount_price: float
    rating: float
    rating_count: int
    product_image: str
    product_url: str
    website_name: str
    category: str
    associated_app: str
    platform_id: str
    user_id: str


ProductKey = Literal[
    "name",
    "price",
    "discount_price",
    "rating",
    "rating_count",
    "product_image",
    "product_url",
]


class Websites(Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"


class ProductCategories(Enum):
    JEANS = "jeans"
    TSHIRT = "t-shirt"
    SHIRT = "shirt"
    CARGO = "cargo"
    FOOTWEAR = "footwear"
    JACKET = "jacket"
    SWEATSHIRTS = "sweatshirts"
    TRACKPANT = "track-pant"
    TROUSER = "trouser"
    WATCHES = "watches"
    SHOES = "shoes"
    KITCHENWARE = "kitchenware"
    HOME_TEXTILES = "home-textiles"
    CLEANING_SUPPLIES = "cleaning-supplies"
    FOOD_GROCERY = "food&grocery"
    HOME_APPLIANCES = "home-appliances"
    SMALL_KITCHEN_APPLIANCES = "small-kitchen-appliances"


class Properties(Enum):
    CATEGORY_ID = "category_id"
    INDEX = "index"
