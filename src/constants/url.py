from typing import Dict, List, TypedDict
from ..lib.types import ProductCategories, Properties, Websites


class ProductUrlDetailsValue(TypedDict):
    website: List[Websites]


PRODUCT_URL_DETAILS_TYPE = Dict[ProductCategories, ProductUrlDetailsValue]

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

# Supabase Plateform id
PLATFORM_IDS = {
    "amazon": "55a353b7-5d4a-455f-b600-2803d7e545f3",
    "flipkart": "3a09abed-0d57-4914-a535-ec8fedbe9c71",
    "myntra": "cf0e243b-ab7b-40b0-8d33-fe56f75101e5"
}

# Product categories and their corresponding properties for Amazon.
# These properties are used to filter and search for products on Amazon.
AMAZON_URL_PROPERTIES: Dict[ProductCategories, Dict[Properties, str]] = {
    ProductCategories.JEANS: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.TSHIRT: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.SHIRT: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.CARGO: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.FOOTWEAR: {
        Properties.CATEGORY_ID: "1983518031",
        Properties.INDEX: "shoes"
    },
    ProductCategories.JACKET: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.TRACKPANT: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.TROUSER: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.SHOES: {
        Properties.CATEGORY_ID: "1983518031",
        Properties.INDEX: "shoes"
    },
    ProductCategories.WATCHES: {
        Properties.CATEGORY_ID: "2563504031",
        Properties.INDEX: "watches"
    },
}

FASHION_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

KITCHENWARE_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

HOME_TEXTILES_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

CLEANING_SUPPLIES_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

PERSONAL_CARE_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

FOOD_GROCERY_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

GADGETS_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

HOME_APPLIANCES_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

SMALL_KITCHEN_APPLIANCES_WEBSITES: List[Websites] = [
    Websites.AMAZON,
    Websites.FLIPKART,
    Websites.MYNTRA,
]

PRODUCT_URL_DETAILS: PRODUCT_URL_DETAILS_TYPE = {
    ProductCategories.JEANS: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.TSHIRT: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.SHIRT: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.CARGO: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.FOOTWEAR: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.JACKET: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.SWEATSHIRTS: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.TRACKPANT: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.TROUSER: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.WATCHES: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.SHOES: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.KITCHENWARE: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.HOME_TEXTILES: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.CLEANING_SUPPLIES: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.FOOD_GROCERY: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.HOME_APPLIANCES: {
        "website": FASHION_WEBSITES
    },
    ProductCategories.SMALL_KITCHEN_APPLIANCES: {
        "website": FASHION_WEBSITES
    },
}
