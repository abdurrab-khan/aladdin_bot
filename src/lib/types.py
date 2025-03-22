from typing import TypedDict, Union


class Product(TypedDict):
    product_name: str
    product_price: float
    product_discount: Union[float, None]
    product_rating: Union[float, None]
    product_url: str
    product_image: str