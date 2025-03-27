MIN_PRICE = 200
MAX_PRICE = 2500
MAX_PRODUCTS = 4


TELEGRAM_MESSAGE_TEMPLATE = """
{product_name}
{product_price}
{product_discount}
{product_rating}
{product_discount_percentage}
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

IMAGE_PATH = "product_images"

WEB_URLS = [
    "https://www.amazon.com",
    "https://www.flipkart.com",
    "https://www.myntra.com",
    "https://www.ajio.com",
]

PRODUCT_CATEGORY = [
    "Men's Clothing",
    "Men's Footwear",
    "Men's Accessories",
    "Men's Watches",
    "Men's Sunglasses",
]
