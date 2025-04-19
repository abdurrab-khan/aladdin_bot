from enum import Enum
from typing import List, TypedDict, Literal


class Product(TypedDict):
    product_name: str
    product_price: float
    product_discount: float
    product_rating: float
    product_url: str
    product_image_path: str
    product_image_url: str


ProductKey = Literal[
    "product_name",
    "product_price",
    "product_discount",
    "product_rating",
    "product_url",
    "product_image_path",
    "product_image_url",
]


class ProductVariants(TypedDict):
    variant_name: str
    variant_price: float
    variant_discount: float
    variant_urls: List[str]
    variant_image_path: List[str]
    variant_image_url: List[str]


class Websites(Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"


class SendMessageTo(Enum):
    TELEGRAM = "telegram"
    X = "x"
    META = "meta"


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
