from typing import Dict

from ..constants.const import FLIPKART_CATEGORY, INDEX, CATEGORY_ID
from ..lib.types import ProductCategories, ProductUrlDetailsValue, Websites


MAX_PRODUCTS_PER_WEBSITE = 30

# UTILS FUNCTIONS


def getIndex(index: str):
    return INDEX.format(index=index)


def getCategoryId(categoryId: str):
    return CATEGORY_ID.format(category_id=categoryId)


def formatCategoryIdAndIndex(categoryId: str | None, indexId: str | None) -> str:
    if categoryId is None and indexId is None:
        return ""

    index = INDEX.format(index=indexId) if indexId else ""
    category = CATEGORY_ID.format(category_id=categoryId) if categoryId else ""

    return (index + category)


def getFlipkartCategory(categoryName: str, categoryId: str):
    return FLIPKART_CATEGORY.format(category_name=categoryName, category_id=categoryId)


# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
BASE_URLS: Dict[Websites, str] = {
    Websites.AMAZON: (
        "https://www.amazon.in/s?k={query}{index}"
        "{category_id}%2C"
        "%2Cp_n_pct-off-with-tax%3A2665401031"
        "%2Cp_n_availability%3A1318485031"
        "%2Cp_72%3A1318476031"
        "&dc&ref=sr_nr_p_72_1"
        "&low-price={min_price}&high-price={max_price}"
    ),
    Websites.FLIPKART: (
        "https://www.flipkart.com/{category}{query}"
        "&marketplace=FLIPKART"
        "&as-show=on&as=off"
        "&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore"
        "&p[]=facets.rating%5B%5D=3%E2%98%85+%26+above"
        "&p[]=facets.ideal_for%5B%5D=Men"
        "&p[]=facets.price_range.from={min_price}"
        "&p[]=facets.price_range.to={max_price}"
    ),
    # Websites.MYNTRA: "https://www.myntra.com/{query}?f=Gender%3Amen%2Cmen%20women&rawQuery={query}&rf=Discount%20Range%3A80.0_100.0_80.0%20TO%20100.0%3A%3APrice%3A250.0_{max_price}.0_250.0%20TO%20{max_price}.0"
}

# SUPABASE PLATEFORM_IDS
PLATFORM_IDS = {
    "amazon": "55a353b7-5d4a-455f-b600-2803d7e545f3",
    "flipkart": "3a09abed-0d57-4914-a535-ec8fedbe9c71",
    # "myntra": "cf0e243b-ab7b-40b0-8d33-fe56f75101e5"
}

# All Supported Websites based on category
SUPPORTED_WEBSITES = {
    "fashion": [
        Websites.AMAZON,
        Websites.FLIPKART,
        # Websites.MYNTRA,
    ],
    "kitchenware": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "home-textiles": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "cleaning-supplies": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "household": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "food-grocery": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "home-appliances": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "small-kitchen-appliances": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "gadgets": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
}


PRODUCT_URL_DETAILS: Dict[ProductCategories, ProductUrlDetailsValue] = {
    # FASHION - SECTION
    ProductCategories.JEANS: {
        "min_price": 100,
        "max_price": 2500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/bottomwear/jeans/mens-jeans", "clo,vua,k58,i51")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TSHIRT: {
        "min_price": 100,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/topwear/tshirts/mens-tshirts", "clo,ash,ank,edy")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SHIRT: {
        "min_price": 100,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/topwear/shirts/mens-shirts", "clo,ash,axc,mmk")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.CARGO: {
        "min_price": 100,
        "max_price": 1800,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/bottomwear/cargos/mens-cargos", "clo,vua,rqy,nli")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.JACKET: {
        "min_price": 100,
        "max_price": 2500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/winter-wear/jackets/mens-jackets", "clo,qvw,z0g,jbm")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SWEATSHIRTS: {
        "min_price": 100,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/winter-wear/sweatshirts/mens-sweatshirts", "clo,qvw,64a,vui")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TRACKPANT: {
        "min_price": 100,
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TROUSER: {
        "min_price": 100,
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("clothing-and-accessories/bottomwear/trousers/mens-trousers", "clo,vua,mle,lhk")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.WATCHES: {
        "min_price": 100,
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("2563504031"),
            "index": getIndex("watches")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("watches/wrist-watches", "r18,f13")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.FOOTWEAR: {
        "min_price": 100,
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1983518031"),
            "index": getIndex("shoes")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("footwear/mens-footwear", "osp,cil")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },

    # KITCHEN - SECTION
    ProductCategories.KITCHENWARE: {
        "min_price": 50,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("kitchen-cookware-serveware", "upp"),
        },
        "website": SUPPORTED_WEBSITES["kitchenware"]
    },
    ProductCategories.SMALL_KITCHEN_APPLIANCES: {
        "min_price": 50,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("home-kitchen", "j9e"),
        },
        "website": SUPPORTED_WEBSITES["small-kitchen-appliances"]
    },

    # CLEANING_SUPPLIES - SECTION
    ProductCategories.CLEANING_SUPPLIES: {
        "min_price": 80,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("home-cleaning-bathroom-accessories", "rja"),
        },
        "website": SUPPORTED_WEBSITES["cleaning-supplies"]
    },

    # HOUSEHOLD - SECTION -- CHECK AGAIN
    ProductCategories.HOUSEHOLD: {
        "min_price": 80,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1374515031"),
            "index": getIndex("hpc")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("home-cleaning-bathroom-accessories", "rja")
        },
        "website": SUPPORTED_WEBSITES["household"]
    },

    # FOOD_GROCERY - SECTION
    ProductCategories.FOOD_GROCERY: {
        "min_price": 100,
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("2454178031"),
            "index": ""
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("food-products", "eat")
        },
        "website": SUPPORTED_WEBSITES["food-grocery"]
    },

    # HOME_APPLIANCES - SECTION
    ProductCategories.HOME_APPLIANCES: {
        "min_price": 100,
        "max_price": 3500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("home-kitchen/home-appliances", "j9e,abm")
        },
        "website": SUPPORTED_WEBSITES["home-appliances"]
    },

    # GADGETS - SECTION
    ProductCategories.GADGETS: {
        "min_price": 50,
        "max_price": 3500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("computers", "6bo")
        },
        "website": SUPPORTED_WEBSITES["gadgets"]
    },

    # MOBILE ACCESSORIES
    ProductCategories.MOBILE_ACCESSORIES: {
        "min_price": 200,
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("976419031"),
            "index": getIndex("electronics")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("mobiles-accessories", "tyy")
        },
        "website": SUPPORTED_WEBSITES["gadgets"]
    },

    # COMPUTER ACCESSORIES
    ProductCategories.COMPUTER_ACCESSORIES: {
        "min_price": 200,
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("976419031"),
            "index": getIndex("electronics")
        },
        "flipkart_url_props": {
            "category": getFlipkartCategory("laptop-accessories", "6bo,ai3"),
        },
        "website": SUPPORTED_WEBSITES["gadgets"]
    }
}
