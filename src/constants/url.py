from typing import Dict
from ..lib.types import ProductCategories, ProductUrlDetailsValue, Websites


MAX_PRODUCTS_PER_WEBSITE = 25

# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
BASE_URLS: Dict[Websites, str] = {
    Websites.AMAZON: (
        "https://www.amazon.in/s?k={query}&i={index}"
        "&rh=n%3A{category_id}%2Cp_36%3A25000-{max_price}00"
        "%2Cp_n_pct-off-with-tax%3A27060457031"
        "%2Cp_n_availability%3A1318485031"
        "%2Cp_72%3A1318476031"
        "&dc&ref=sr_nr_p_72_1"
    ),
    Websites.FLIPKART: (
        "https://www.flipkart.com/search?q={query}"
        "&marketplace=FLIPKART"
        "&as-show=on&as=off"
        "&p[]=facets.discount_range_v1%5B%5D=70%25+or+more"
        "&p[]=facets.rating%5B%5D=3%E2%98%85+%26+above"
        "&p[]=facets.ideal_for%5B%5D=Men"
        "&p[]=facets.price_range.from=250"
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
    "personal-care": [
        Websites.AMAZON,
        Websites.FLIPKART,
    ],
    "food-grocery": [
        Websites.AMAZON,
        Websites.FLIPKART,
        Websites.MYNTRA
    ],
    "gadgets": [
        Websites.AMAZON,
        Websites.FLIPKART,
        Websites.MYNTRA
    ],
    "home-appliances": [
        Websites.AMAZON,
        Websites.FLIPKART,
        Websites.MYNTRA
    ],
    "small-kitchen-appliances": [
        Websites.AMAZON,
        Websites.FLIPKART,
        Websites.MYNTRA
    ]
}


PRODUCT_URL_DETAILS: Dict[ProductCategories, ProductUrlDetailsValue] = {
    # FASHION - SECTION
    ProductCategories.JEANS: {
        "max_price": 2500,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TSHIRT: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SHIRT: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.CARGO: {
        "max_price": 1800,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.JACKET: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SWEATSHIRTS: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TRACKPANT: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.TROUSER: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": "1968024031",
            "index": "fashion"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.WATCHES: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": "2563504031",
            "index": "watches"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.FOOTWEAR: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": "1983518031",
            "index": "shoes"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },
    ProductCategories.SHOES: {
        "max_price": 2000,
        "amazon_url_props": {
            "category_id": "1983518031",
            "index": "shoes"
        },
        "website": SUPPORTED_WEBSITES["fashion"]
    },

    # KITCHENWARE - SECTION
    ProductCategories.KITCHENWARE: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "",
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["kitchenware"]
    },

    # HOME_TEXTILES - SECTION
    ProductCategories.HOME_TEXTILES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "",
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["home-textiles"]
    },

    # CLEANING_SUPPLIES - SECTION
    ProductCategories.CLEANING_SUPPLIES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "",
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["cleaning-supplies"]
    },

    # FOOD_GROCERY - SECTION
    ProductCategories.FOOD_GROCERY: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "",
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["food-grocery"]
    },

    # HOME_APPLIANCES - SECTION
    ProductCategories.HOME_APPLIANCES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "",
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["home-appliances"]
    },

    # SMALL_KITCHEN_APPLIANCES - SECTION
    ProductCategories.SMALL_KITCHEN_APPLIANCES: {
        "max_price": 1500,
        "amazon_url_props": {
            "category_id": "",
            "index": ""
        },
        "website": SUPPORTED_WEBSITES["small-kitchen-appliances"]
    },
}
