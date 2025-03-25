from typing import List, TypedDict, Union
from enum import Enum


class Product(TypedDict):
    product_name: str
    product_price: float
    product_discount: Union[float, None]
    product_rating: Union[float, None]
    product_url: str
    product_image: str

class ProductSearchResult:
    is_last_page: bool
    products: List[Product]

class Websites(Enum):
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    MYNTRA = "myntra"
    AJIO = "ajio"