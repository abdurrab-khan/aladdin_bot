from ..lib.types import ProductCategories

# Path to the images directory where product images will be saved.
IMAGE_PATH = "images"

# Maximum number of products to scrape from each website during a search operation
# MAX_PRODUCTS_PER_WEBSITE = 30
MAX_PRODUCTS_PER_WEBSITE = 10

# Required keys for product data.
# These keys are used to ensure that the scraped product data contains all necessary information.
REQUIRED_PRODUCT_KEYS = {
    "product_name",
    "product_price",
    "product_discount",
    "product_image",
    "product_rating",
    "product_url"
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
    ProductCategories.WATCHES: 3,
    ProductCategories.SUNGLASSES: 3,
    ProductCategories.PERFUME: 4,
}

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
    ProductCategories.WATCHES: "⌚",
    ProductCategories.SUNGLASSES: "🕶️",
    ProductCategories.PERFUME: "🧴",
}
