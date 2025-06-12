from enum import Enum
from typing import TypedDict, Literal


class Product(TypedDict):
    name: str
    description: str
    price: float
    discount_price: float
    average_rating: float
    review_count: str
    product_image: str
    product_url: str
    category: str
    associated_app: str


ProductKey = Literal[
    "name",
    "description",
    "price",
    "discount_price",
    "average_rating",
    "review_count",
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
    SHORTS = "shorts"
    SWEATSHIRTS = "sweatshirts"
    TRACKPANT = "track-pant"
    TROUSER = "trouser"
    CASUAL_SHOES = "casual-shoes"
    FORMAL_SHOES = "formal-shoes"
    SPORTS_SHOES = "sports-shoes"
    SNEAKERS = "sneakers"
    WALLET = "wallet"
    WATCHES = "watches"
    SUNGLASSES = "sunglasses"
    PERFUME = "perfume"


class Properties(Enum):
    CATEGORY_ID = "category_id"
    INDEX = "index"
