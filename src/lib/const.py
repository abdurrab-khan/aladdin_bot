MIN_PRICE = 200
MAX_PRICE = 2500

# Message Template for TELEGRAM && TWITTER (X)
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

# For Regex
COLORS = "blue|green|white|red|black|yellow|pink|purple|orange|brown|gray|grey|navy blue|light|dark"
UNWANTED_CHARS = r"[(){}|\[\],.\-_/:;!?@#%^&*=+'\"<>\\$]"


# Product image path where they are going to be store.
IMAGE_PATH = "product_images"

# All list Websites.
WEB_URLS = [
    "https://www.amazon.com",
    "https://www.flipkart.com",
    "https://www.myntra.com",
    "https://www.ajio.com",
]

# All product categories.
MAX_PRODUCTS_COUNT = {
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


# CSS Selectors for each website to extract product data.
CSS_SELECTORS_BY_WEBSITE = {
    "amazon": {
        "price": ["span.a-price-whole", "span#priceblock_ourprice"],
        "image": ["img#landingImage", "img#imgBlkFront"],
        "name": ["span#productTitle"],
        "rating": ["span.a-icon-alt"],
    },
    "flipkart": {
        "price": ["div.Nx9bqj", "div._30jeq3"],
        "image": ["div._8id3KM img", "div.vU5WPQ img"],
        "name": ["span.VU-ZEz", "span._35KyD6"],
        "rating": ["div.XQDdHH", "div._6er70b"],
    },
    "myntra": {

    },
    "ajio": {},
}

# CSS Selectors for each website to extract the product container.
CSS_SELECTORS_BY_WEBSITE_CONTAINER = {
    "amazon": {
        "container": [".s-main-slot.s-result-list"],
    },
    "flipkart": {
        "container": ["div._1AtVbE div._2kHMtA"],
    },
    "myntra": {
        "container": ["div.product-base"],
    },
    "ajio": {
        "container": ["div.item-list"],
    },
}
