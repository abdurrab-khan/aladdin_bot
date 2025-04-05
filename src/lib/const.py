from .types import Websites, ProductKey, SendMessageTo
from typing import Dict, List

MIN_PRICE = 200
MAX_PRICE = 2500

# Regex patterns for extracting product details.
# These patterns are used to match and extract specific information from product names and descriptions.
COLORS = "blue|green|white|red|black|yellow|pink|purple|orange|brown|gray|grey|navy blue|light|dark"
UNWANTED_CHARS = r"[(){}|\[\],.\-_/:;!?@#%^&*=+'\"<>\\$]"

# Path to the images directory where product images will be saved.
IMAGE_PATH = "product_images"


# Message templates for different platforms.
# These templates are used to format the messages that are sent to the users.
TELEGRAM_MESSAGE_TEMPLATE = """
<b>{product_name}</b>\n\n⭐ Reviews: {stars} ({product_rating} Stars)\n\n💰 Price: <s>❎ ₹{product_price}</s> ➡️ <b>₹{discount_price}</b>\n🔥 Discount: Save ➡️ {price_discount_percentage}%!!\n\n
{product_url}
"""

TWITTER_MESSAGE_TEMPLATE = """
{product_name}
{product_price}
{product_discount}
{product_rating}
{product_discount_percentage}
{product_url}
"""

MSG_TEMPLATE_BY_NAME = {
    SendMessageTo.TELEGRAM: TELEGRAM_MESSAGE_TEMPLATE,
    SendMessageTo.TWITTER: TWITTER_MESSAGE_TEMPLATE,
}


# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
COMMON_URLS = {
    Websites.AMAZON: "https://www.amazon.in/s?k={category}&i=apparel&rh=n%3A1571271031%2Cn%3A1968024031%2Cp_36%3A-300000%2Cp_n_pct-off-with-tax%3A27060457031&dc&ds=v1%3AzQuhUM0TKjXD7zlToqva1pRM3Ga9FnC4VV9Dh8QGXfI&qid=1743830561&ref=sr_ex_n_1",
    Websites.FLIPKART: "https://www.flipkart.com/{category}/pr?sid=clo%2Cash%2Cank%2Cedy&fm=neo%2Fmerchandising&iid=M_306f4f57-35bd-49c6-8adc-37f235257e69_1_372UD5BXDFYS_MC.IF56C41VGEYS&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Fashion~Men%27s%2BTop%2BWear~Men%27s%2BT-Shirts_IF56C41VGEYS&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L2_view-all&cid=IF56C41VGEYS&p%5B%5D=facets.rating%255B%255D%3D3%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=&p%5B%5D=facets.ideal_for%255B%255D%3DMen",
    Websites.MYNTRA: "https://www.myntra.com/{category}?rf=Discount%20Range%3A70.0_100.0_70.0%20TO%20100.0%3A%3APrice%3A300.0_3000.0_300.0%20TO%203000.0&sort=popularity"
}

# Product categories for different e-commerce websites.
PRODUCTS_COUNT = {
    "jeans": 8,
    "t-shirt": 8,
    "shirt": 8,
    "cargo": 3,
    "footwear": 3,
    "jacket": 4,
    "shorts": 3,
    "pyjama": 4,
    "sweatshirts": 4,
    "track-pant": 4,
    "trouser": 4,
    "casual-shoes": 4,
    "formal-shoes": 4,
    "sports-shoes": 4,
    "sneakers": 5,
    "ladies-kurta": 4,
    "ladies-handbag": 3,
    "saree": 5,
    "lehenga-choli": 4,
    "wallet": 4,
    "belt": 4,
    "watches": 5,
    "sunglasses": 3,
    "perfume": 4,
}

# Product emojis for different product categories.
# These emojis are used to represent different product categories in the messages sent to users.
PRODUCTS_EMOJI = {
    "jeans": "👖",
    "t-shirt": "👕",
    "shirt": "👔",
    "cargo": "👖",
    "footwear": "🩴",
    "jacket": "🧥",
    "shorts": "🩳",
    "pyjama": "🩲",
    "sweatshirts": "👕",
    "track-pant": "🩳",
    "trouser": "👖",
    "casual-shoes": "👟",
    "formal-shoes": "👞",
    "sports-shoes": "👟",
    "sneakers": "👟",
    "ladies-kurta": "👗",
    "ladies-handbag": "👜",
    "saree": "👗",
    "lehenga-choli": "👗",
    "wallet": "👛",
    "belt": "👔",
    "watches": "⌚",
    "sunglasses": "🕶️",
    "perfume": "🧴",
}

# Color emojis for different colors.
# These emojis are used to represent different colors in the messages sent to users.
color_emoji = {
    "blue": "🔵",
    "green": "🟢",
    "white": "⚪",
    "red": "🔴",
    "black": "⚫",
    "yellow": "🟡",
    "pink": "🟣",
    "purple": "🟣",
    "orange": "🟠",
    "brown": "🟤",
    "gray": "🟡",
}


# CSS SELECTORS
# CSS Selectors for each website to extract product details.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_DETAILS: Dict[Websites, Dict[ProductKey, List[str]]] = {
    Websites.AMAZON: {
        "product_name": ["h2.a-size-base-plus.a-spacing-none"],
        "product_price": ["span.a-price.a-text-price span.a-offscreen"],
        "product_discount": ["span.a-price-whole", "span#priceblock_ourprice"],
        "product_image": ["img.s-image"],
        "product_rating": ["span.a-icon-alt"],
        "product_url": ["a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal", "a.a-link-normal"],
    },
    Websites.FLIPKART: {
        "product_name": ["span.VU-ZEz"],
        "product_price": [r"div.yRaY8j"],
        "product_discount": ["div.Nx9bqj.CxhGGd"],
        "product_image": ["div._8id3KM img"],
        "product_rating": ["div.XQDdHH"],
        "product_url": ["a.rPDeLR"],
    },
    Websites.MYNTRA: {
        "product_name": ["h4.product-product"],
        "product_price": ["div.product-price span .product-strike"],
        "product_discount": ["div.product-price span .product-discountedPrice"],
        "product_image": ["div.product-imageSliderContainer img"],
        "product_rating": ["div.product-ratingsContainer span"],
        "product_url": ["a"],
    },
    Websites.AJIO: None

}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: ".s-main-slot.s-result-list",
    Websites.FLIPKART: "div.DOjaWF.gdgoEp:not(.col-2-12):not(.col-12-12), div.DOjaWF.YJG4Cf",
    Websites.MYNTRA: "ul.results-base",
    Websites.AJIO: None,
}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div._1sdMkc.LFEi7Z",
    Websites.MYNTRA: "li.product-base",
    Websites.AJIO: None,
}


# Affiliate IDs for different e-commerce websites.
# These IDs are used to track referrals and commissions for affiliate marketing purposes.
AMAZON_AFFILIATE_ID = "?tag=aladdinloot3-21"
FLIPKART_AFFILIATE_ID = "?affid=admitad&affExtParam1=298614"
MYNTRA_AFFILIATE_ID = "?utm_source=admitad&utm_medium=affiliate"


REQUIRED_PRODUCT_KEYS = [
    "product_name",
    "product_price",
    "product_image",
    "product_rating",
    "product_url"
]
