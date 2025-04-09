from ..lib.types import Websites, ProductCategories

# Path to the images directory where product images will be saved.
IMAGE_PATH = "images"

# Required keys for product data.
# These keys are used to ensure that the scraped product data contains all necessary information.
REQUIRED_PRODUCT_KEYS = [
    "product_name",
    "product_price",
    "product_image",
    "product_rating",
    "product_url"
]

# Affiliate IDs for different e-commerce websites.
# These IDs are used to track referrals and earn commissions on sales generated through the bot.
AMAZON_AFFILIATE_ID = "?tag=aladdinloot3-21"
FLIPKART_AFFILIATE_ID = "?affid=admitad&affExtParam1=298614"
MYNTRA_AFFILIATE_ID = "?utm_source=admitad&utm_medium=affiliate"

# Web URLs for different e-commerce websites.
# These URLs are used to scrape product data from the respective websites.
COMMON_URLS = {
    Websites.AMAZON: "https://www.amazon.in/s?k={category}&i=apparel&rh=n%3A1571271031%2Cn%3A1968024031%2Cp_36%3A-200000%2Cp_72%3A1318476031%2Cp_n_pct-off-with-tax%3A27060457031&dc&ds=v1%3AbyRKzay5iYwlmgf4D5EJ5LaYdLVQOMoRibfk5Ipsff8&crid=2PS5VP6LCCJ36&qid=1744010988&rnid=1571271031&sprefix={category}",
    Websites.FLIPKART: "https://www.flipkart.com/search?q={category}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.rating%255B%255D%3D3%25E2%2598%2585%2B%2526%2Babove&p%5B%5D=facets.ideal_for%255B%255D%3DMen",
    Websites.MYNTRA: "https://www.myntra.com/{category}?f=Gender%3Amen%2Cmen%20women&rawQuery={category}&rf=Discount%20Range%3A70.0_100.0_70.0%20TO%20100.0%3A%3APrice%3A300.0_2900.0_300.0%20TO%202900.0"
}

# Product categories for different e-commerce websites.
PRODUCTS_PER_CATEGORY = {
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

# Maximum number of products to scrape from each website during a search operation
# MAX_PRODUCTS_PER_WEBSITE = 30
MAX_PRODUCTS_PER_WEBSITE = 10

PRICE_LIMITS = {
    ProductCategories.JEANS: 2500,
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
    ProductCategories.JEANS: "👖",
    ProductCategories.TSHIRT: "👕",
    ProductCategories.SHIRT: "👔",
    ProductCategories.CARGO: "👖",
    ProductCategories.FOOTWEAR: "🩴",
    ProductCategories.JACKET: "🧥",
    ProductCategories.SHORTS: "🩳",
    ProductCategories.PYJAMA: "🩲",
    ProductCategories.SWEATSHIRTS: "👕",
    ProductCategories.TRACKPANT: "🩳",
    ProductCategories.TROUSER: "👖",
    ProductCategories.CASUAL_SHOES: "👟",
    ProductCategories.FORMAL_SHOES: "👞",
    ProductCategories.SPORTS_SHOES: "👟",
    ProductCategories.SNEAKERS: "👟",
    ProductCategories.WALLET: "👛",
    ProductCategories.BELT: "👔",
    ProductCategories.WATCHES: "⌚",
    ProductCategories.SUNGLASSES: "🕶️",
    ProductCategories.PERFUME: "🧴",
}
