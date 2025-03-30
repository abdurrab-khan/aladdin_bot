from encodings.punycode import T
from typing import List, TypedDict, Union
from typing_extensions import NotRequired
from enum import Enum


class Product(TypedDict):
    product_name: str
    product_price: float
    product_discount: Union[float, None]
    product_rating: Union[float, None]
    product_url: str
    product_image: str
    product_color: NotRequired[str]


class ProductVariants(TypedDict):
    base_product_name: str
    variants: List[Product]


class ProductSearchResult:
    is_last_page: bool
    products: List[Product]


class Websites(Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"
    AJIO = "ajio"


class SendMessageTo(Enum):
    TELEGRAM = "telegram"
    TWITTER = "twitter"


class ProductCategories(Enum):
    JEANS = "jeans"
    SHIRTS = "shirts"
    SHOES = "shoes"
    WATCHES = "watches"
    TSHIRTS = "tshirts"
