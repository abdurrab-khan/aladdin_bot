from typing import Dict

from ..constants.const import INDEX, CATEGORY_ID
from ..lib.types import ProductCategories, ProductUrlDetailsValue, Websites


MAX_PRODUCTS_PER_WEBSITE = 25

# UTILS FUNCTIONS


def getIndex(index: str):
    return INDEX.format(index=index)


def getCategoryId(categoryId: str):
    return CATEGORY_ID.format(category_id=categoryId)


# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
BASE_URLS: Dict[Websites, str] = {
    Websites.AMAZON: (
        "https://www.amazon.in/s?k={query}{index}"
        "{category_id}%2C"
        "%2Cp_n_pct-off-with-tax%3A27060457031"
        "%2Cp_n_availability%3A1318485031"
        "%2Cp_72%3A1318476031"
        "&dc&ref=sr_nr_p_72_1"
        "&low-price={min_price}&high-price={max_price}"
    ),
    Websites.FLIPKART: (
        "https://www.flipkart.com/search?q={query}"
        "&marketplace=FLIPKART"
        "&as-show=on&as=off"
        "&p[]=facets.discount_range_v1%5B%5D=70%25+or+more"
        "&p[]=facets.rating%5B%5D=3%E2%98%85+%26+above"
        "&p[]=facets.ideal_for%5B%5D=Men"
        "&p[]=facets.price_range.from={min_price}"
        "&p[]=facets.price_range.to={max_price}"
    ),
    Websites.MYNTRA: "https://www.myntra.com/{query}?f=Gender%3Amen%2Cmen%20women&rawQuery={query}&rf=Discount%20Range%3A80.0_100.0_80.0%20TO%20100.0%3A%3APrice%3A250.0_{max_price}.0_250.0%20TO%20{max_price}.0"
}

# SUPABASE PLATEFORM_IDS
PLATFORM_IDS = {
    "amazon": "55a353b7-5d4a-455f-b600-2803d7e545f3",
    "flipkart": "3a09abed-0d57-4914-a535-ec8fedbe9c71",
    "myntra": "cf0e243b-ab7b-40b0-8d33-fe56f75101e5"
}

# All Supported Websites based on category
SUPPORTED_WEBSITES = {
    "fashion": [
        Websites.AMAZON,
        Websites.FLIPKART,
        Websites.MYNTRA,
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
        "max_price": 2500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TSHIRT: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SHIRT: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.CARGO: {
        "max_price": 1800,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.JACKET: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SWEATSHIRTS: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TRACKPANT: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TROUSER: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1968024031"),
            "index": getIndex("fashion")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.WATCHES: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("2563504031"),
            "index": getIndex("watches")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.FOOTWEAR: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1983518031"),
            "index": getIndex("shoes")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SHOES: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("1983518031"),
            "index": getIndex("shoes")
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },

    # KITCHEN - SECTION
    ProductCategories.KITCHENWARE: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "website": SUPPORTED_WEBSITES["kitchenware"]
    },
    ProductCategories.SMALL_KITCHEN_APPLIANCES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "website": SUPPORTED_WEBSITES["small-kitchen-appliances"]
    },

    # CLEANING_SUPPLIES - SECTION
    ProductCategories.CLEANING_SUPPLIES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "website": SUPPORTED_WEBSITES["cleaning-supplies"]
    },

    # HOUSEHOLD - SECTION
    ProductCategories.HOUSEHOLD: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("1374515031"),
            "index": getIndex("hpc")
        },
        "website": SUPPORTED_WEBSITES["household"]
    },


    # FOOD_GROCERY - SECTION
    ProductCategories.FOOD_GROCERY: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("2454178031"),
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["food-grocery"]
    },

    # HOME_APPLIANCES - SECTION
    ProductCategories.HOME_APPLIANCES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": getCategoryId("976442031"),
            "index": getIndex("kitchen")
        },
        "website": SUPPORTED_WEBSITES["home-appliances"]
    },

    # GADGETS - SECTION
    ProductCategories.GADGETS: {
        "max_price": 2500,
        "amazon_url_props": {
            "category_id": getCategoryId(""),
            "index": getIndex("kitchen")
        },
        "website": SUPPORTED_WEBSITES["gadgets"]
    },

    # MOBILE ACCESSORIES
    ProductCategories.MOBILE_ACCESSORIES: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("976419031"),
            "index": getIndex("electronics")
        },
        "website": SUPPORTED_WEBSITES["gadgets"]
    },

    # COMPUTER ACCESSORIES
    ProductCategories.COMPUTER_ACCESSORIES: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": getCategoryId("976419031"),
            "index": getIndex("electronics")
        },
        "website": SUPPORTED_WEBSITES["gadgets"]
    }
}
