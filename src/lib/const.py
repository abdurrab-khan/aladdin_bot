from .types import Websites, ProductKey, SendMessageTo, ProductCategories
from typing import Dict, List

# Regex patterns for extracting product details.
# These patterns are used to match and extract specific information from product names and descriptions.
COLORS = "blue|green|white|red|black|yellow|pink|purple|orange|brown|gray|grey|navy blue|light|dark"
UNWANTED_CHARS = r"[(){}|\[\],.\-_/:;!?@#%^&*=+'\"<>\\$]"

# Path to the images directory where product images will be saved.
IMAGE_PATH = "images"


# Message templates for different platforms.
# These templates are used to format the messages that are sent to the users.
TELEGRAM_MESSAGE_TEMPLATE = """
<b>{product_name}</b>\n\n⭐ Reviews: {stars} ({product_rating} Stars)\n\n💰 Price: <s>❎ ₹{product_price}</s> ➡️ <b>₹{product_discount}</b>\n🔥 Discount: Save ➡️ {product_discount_percentage}%!!\n\n
{product_url}
"""

X_MESSAGE_TEMPLATE = """
{product_name}
{product_price}
{product_discount}
{product_rating}
{product_discount_percentage}
{product_url}
"""

MESSAGE_TEMPLATES = {
    SendMessageTo.TELEGRAM: TELEGRAM_MESSAGE_TEMPLATE,
    SendMessageTo.X: X_MESSAGE_TEMPLATE,
}


# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
COMMON_URLS = {
    Websites.AMAZON: "https://www.amazon.in/s?k={category}&i=apparel&rh=n%3A1571271031%2Cn%3A1968024031%2Cp_36%3A-200000%2Cp_72%3A1318476031%2Cp_n_pct-off-with-tax%3A27060457031&dc&ds=v1%3AbyRKzay5iYwlmgf4D5EJ5LaYdLVQOMoRibfk5Ipsff8&crid=2PS5VP6LCCJ36&qid=1744010988&rnid=1571271031&sprefix={category}",
    Websites.FLIPKART: "https://www.flipkart.com/search?q={category}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.rating%255B%255D%3D3%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=facets.ideal_for%255B%255D%3DMen",
    Websites.MYNTRA: "https://www.myntra.com/{category}?f=Gender%3Amen%2Cmen%20women&rawQuery={category}&rf=Discount%20Range%3A70.0_100.0_70.0%20TO%20100.0%3A%3APrice%3A300.0_2900.0_300.0%20TO%202900.0"
}

# Product categories for different e-commerce websites.
PRODUCTS_COUNT = {
    ProductCategories.JEANS: 6,
    ProductCategories.TSHIRT: 6,
    ProductCategories.SHIRT: 6,
    ProductCategories.CARGO: 3,
    ProductCategories.FOOTWEAR: 3,
    ProductCategories.JACKET: 4,
    ProductCategories.SHORTS: 3,
    ProductCategories.PYJAMA: 4,
    ProductCategories.SWEATSHIRTS: 4,
    ProductCategories.TRACKPANT: 4,
    ProductCategories.TROUSER: 4,
    ProductCategories.CASUAL_SHOES: 4,
    ProductCategories.FORMAL_SHOES: 4,
    ProductCategories.SPORTS_SHOES: 4,
    ProductCategories.SNEAKERS: 5,
    ProductCategories.WALLET: 3,
    ProductCategories.BELT: 3,
    ProductCategories.WATCHES: 3,
    ProductCategories.SUNGLASSES: 3,
    ProductCategories.PERFUME: 4,
}

MAX_PRODUCT_PRICE = {
    ProductCategories.JEANS: 2000,
    ProductCategories.TSHIRT: 1500,
    ProductCategories.SHIRT: 1500,
    ProductCategories.CARGO: 1800,
    ProductCategories.FOOTWEAR: 2400,
    ProductCategories.JACKET: 2000,
    ProductCategories.SHORTS: 1000,
    ProductCategories.PYJAMA: 1000,
    ProductCategories.SWEATSHIRTS: 1500,
    ProductCategories.TRACKPANT: 2000,
    ProductCategories.TROUSER: 2000,
    ProductCategories.CASUAL_SHOES: 2000,
    ProductCategories.FORMAL_SHOES: 2500,
    ProductCategories.SPORTS_SHOES: 2500,
    ProductCategories.SNEAKERS: 2500,
    ProductCategories.WALLET: 1000,
    ProductCategories.BELT: 1200,
    ProductCategories.WATCHES: 2000,
    ProductCategories.SUNGLASSES: 1200,
    ProductCategories.PERFUME: 1000,
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
}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: ".s-main-slot.s-result-list",
    Websites.FLIPKART: "div.DOjaWF.gdgoEp:not(.col-2-12):not(.col-12-12), div.DOjaWF.YJG4Cf",
    Websites.MYNTRA: "ul.results-base",
}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div._1sdMkc.LFEi7Z",
    Websites.MYNTRA: "li.product-base",
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
