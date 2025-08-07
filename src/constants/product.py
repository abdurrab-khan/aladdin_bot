from typing import Dict
from ..lib.types import ProductCategories


# Maximum number of products to scrape from each website during a search operation
MAX_PRODUCTS_PER_WEBSITE = 25

PRICE_LIMITS: Dict[ProductCategories, int] = {
    ProductCategories.JEANS: 2500,
    ProductCategories.TSHIRT: 1500,
    ProductCategories.SHIRT: 1500,
    ProductCategories.CARGO: 1800,
    ProductCategories.FOOTWEAR: 2400,
    ProductCategories.JACKET: 2000,
    ProductCategories.SHORTS: 1200,
    ProductCategories.SWEATSHIRTS: 1500,
    ProductCategories.TRACKPANT: 2000,
    ProductCategories.TROUSER: 2000,
    ProductCategories.SHOES: 2000,
    ProductCategories.WATCHES: 2000
}
