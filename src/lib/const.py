from .types import Websites, ProductKeys
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
    "TELEGRAM": TELEGRAM_MESSAGE_TEMPLATE,
    "TWITTER": TWITTER_MESSAGE_TEMPLATE,
}


# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
WEB_URLS = [
    "https://www.amazon.com",
    "https://www.flipkart.com",
    "https://www.myntra.com",
    "https://www.ajio.com",
]

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


# CSS Selectors for each website to extract product details.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_DETAILS: Dict[Websites, Dict[ProductKeys, List[str]]] = {
    Websites.AMAZON: {
        "product_price": ["span.a-price.a-text-price span.a-offscreen"],
        "product_image": ["img.s-image"],
        "product_name": ["h2.a-size-base-plus.a-spacing-none"],
        "product_rating": ["span.a-icon-alt"],
        "product_url": ["a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal", "a.a-link-normal"],
        "product_discount": ["span.a-price-whole", "span#priceblock_ourprice"],
    },
    Websites.FLIPKART: {
        "price": ["div.Nx9bqj", "div._30jeq3"],
        "image": ["div._8id3KM img", "div.vU5WPQ img"],
        "name": ["span.VU-ZEz", "span._35KyD6"],
        "rating": ["div.XQDdHH", "div._6er70b"],
    },
    Websites.MYNTRA: {

    },
    Websites.AJIO: {},
}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: ".s-main-slot.s-result-list",
    Websites.FLIPKART: "div._1AtVbE div._2kHMtA",
    Websites.MYNTRA: "div.product-base",
    Websites.AJIO: "div.item-list",
}

# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div._1AtVbE div._2kHMtA",
    Websites.MYNTRA: "div.product-base",
    Websites.AJIO: "div.item-list",
}

# Affiliate IDs for different e-commerce websites.
# These IDs are used to track referrals and commissions for affiliate marketing purposes.
AMAZON_AFFILIATE_ID = "?tag=aladdinloot3-21"
FLIPKART_AFFILIATE_ID = "?affid=admitad&affExtParam1=298614"
MYNTRA_AFFILIATE_ID = "?utm_source=admitad&utm_medium=affiliate"

AJIO_AFFILIATE_ID = "aladdinschirage-21"
