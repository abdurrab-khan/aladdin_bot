from typing import Dict
from ..lib.types import ProductCategories, Properties, Websites

# Affiliate IDs for different e-commerce websites.
# These IDs are used to track referrals and earn commissions on sales generated through the bot.
AMAZON_AFFILIATE_ID = "?tag=aladdinloot3-21"
FLIPKART_AFFILIATE_ID = "?affid=admitad&affExtParam1=298614"
MYNTRA_AFFILIATE_ID = "?utm_source=admitad&utm_medium=affiliate"

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
    ProductCategories.SHORTS: {
        Properties.CATEGORY_ID: "1968024031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.SWEATSHIRTS: {
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
    ProductCategories.CASUAL_SHOES: {
        Properties.CATEGORY_ID: "1983518031",
        Properties.INDEX: "shoes"
    },
    ProductCategories.FORMAL_SHOES: {
        Properties.CATEGORY_ID: "1983518031",
        Properties.INDEX: "shoes"
    },
    ProductCategories.SPORTS_SHOES: {
        Properties.CATEGORY_ID: "1983518031",
        Properties.INDEX: "shoes"
    },
    ProductCategories.SNEAKERS: {
        Properties.CATEGORY_ID: "1983518031",
        Properties.INDEX: "shoes"
    },
    ProductCategories.WALLET: {
        Properties.CATEGORY_ID: "2454169031",
        Properties.INDEX: "luggage"
    },
    ProductCategories.WATCHES: {
        Properties.CATEGORY_ID: "2563504031",
        Properties.INDEX: "watches"
    },
    ProductCategories.SUNGLASSES: {
        Properties.CATEGORY_ID: "1968036031",
        Properties.INDEX: "fashion"
    },
    ProductCategories.PERFUME: {
        Properties.CATEGORY_ID: "1374357031",
        Properties.INDEX: "beauty"
    },
}
