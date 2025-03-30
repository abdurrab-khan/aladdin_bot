MIN_PRICE = 200
MAX_PRICE = 2500
MAX_PRODUCTS = 4

# Message Template for TELEGRAM && TWITTER (X)
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
PRODUCT_CATEGORY = [
    "Men's Clothing",
    "Men's Footwear",
    "Men's Accessories",
    "Men's Watches",
    "Men's Sunglasses",
]


sample_products = {
    "jeans": [
        {
            "product_name": "Levi's 501 Original Fit Jeans",
            "product_price": 69.99,
            "product_discount": 49.99,
            "product_rating": 4.7,
            "product_url": "http://example.com/levis501",
            "product_image": "http://example.com/levis501.jpg",
        },
        {
            "product_name": "Wrangler Authentics Comfort Flex Jeans",
            "product_price": 59.99,
            "product_discount": 39.99,
            "product_rating": 4.5,
            "product_url": "http://example.com/wrangler-flex",
            "product_image": "http://example.com/wrangler-flex.jpg",
        },
        {
            "product_name": "Calvin Klein Slim Fit Jeans",
            "product_price": 79.99,
            "product_discount": 59.99,
            "product_rating": 4.3,
            "product_url": "http://example.com/calvin-slim",
            "product_image": "http://example.com/calvin-slim.jpg",
        },
        {
            "product_name": "Lee Modern Series Slim Straight Leg Jeans",
            "product_price": 54.99,
            "product_discount": 44.99,
            "product_rating": 4.2,
            "product_url": "http://example.com/lee-modern",
            "product_image": "http://example.com/lee-modern.jpg",
        },
        {
            "product_name": "Diesel Thommer Slim Fit Jeans",
            "product_price": 128.99,
            "product_discount": 89.99,
            "product_rating": 4.6,
            "product_url": "http://example.com/diesel-thommer",
            "product_image": "http://example.com/diesel-thommer.jpg",
        }
    ],
    "shirts": [
        {
            "product_name": "Ralph & Lauren >>>>>>>>>>>>>>>>>>>> Oxford Button-Down Shirt | , > ? < * & ^ % $ # @ ! - White",
            "product_price": 89.99,
            "product_discount": 69.99,
            "product_rating": 4.6,
            "product_url": "http://example.com/ralph-oxford-white",
            "product_image": "http://example.com/ralph-oxford-white.jpg",
        },
        {
            "product_name": "Ralph Lauren Oxford Button-Down Shirt - Blue",
            "product_price": 89.99,
            "product_discount": 69.99,
            "product_rating": 4.7,
            "product_url": "http://example.com/ralph-oxford-blue",
            "product_image": "http://example.com/ralph-oxford-blue.jpg",
        },
        {
            "product_name": "Ralph Lauren Oxford Button-Down Shirt - Black",
            "product_price": 89.99,
            "product_discount": 69.99,
            "product_rating": 4.5,
            "product_url": "http://example.com/ralph-oxford-black",
            "product_image": "http://example.com/ralph-oxford-black.jpg",
        },
        {
            "product_name": "Tommy Hilfiger Classic Fit Shirt",
            "product_price": 69.99,
            "product_discount": 54.99,
            "product_rating": 4.4,
            "product_url": "http://example.com/tommy-classic",
            "product_image": "http://example.com/tommy-classic.jpg",
        },
        {
            "product_name": "Brooks Brothers Non-Iron Dress Shirt",
            "product_price": 99.99,
            "product_discount": 79.99,
            "product_rating": 4.8,
            "product_url": "http://example.com/brooks-noniron",
            "product_image": "http://example.com/brooks-noniron.jpg",
        },
    ],
    "shoes": [
        {
            "product_name": "Nike Air Max 270 - Black",
            "product_price": 150.00,
            "product_discount": 129.99,
            "product_rating": 4.6,
            "product_url": "http://example.com/nike-airmax-black",
            "product_image": "http://example.com/nike-airmax-black.jpg",
        },
        {
            "product_name": "Nike Air Max 270 - White",
            "product_price": 150.00,
            "product_discount": 129.99,
            "product_rating": 4.5,
            "product_url": "http://example.com/nike-airmax-white",
            "product_image": "http://example.com/nike-airmax-white.jpg",
        },
        {
            "product_name": "Adidas Ultraboost",
            "product_price": 180.00,
            "product_discount": 159.99,
            "product_rating": 4.8,
            "product_url": "http://example.com/adidas-ultraboost",
            "product_image": "http://example.com/adidas-ultraboost.jpg",
        },
        {
            "product_name": "New Balance 574 Classic",
            "product_price": 89.99,
            "product_discount": 74.99,
            "product_rating": 4.4,
            "product_url": "http://example.com/newbalance-574",
            "product_image": "http://example.com/newbalance-574.jpg",
        },
        {
            "product_name": "Converse Chuck Taylor All Star",
            "product_price": 60.00,
            "product_discount": 49.99,
            "product_rating": 4.7,
            "product_url": "http://example.com/converse-chucktaylor",
            "product_image": "http://example.com/converse-chucktaylor.jpg",
        }
    ],
    "watches": [
        {
            "product_name": "Rolex Submariner",
            "product_price": 8999.99,
            "product_discount": 8499.99,
            "product_rating": 4.9,
            "product_url": "http://example.com/rolex-submariner",
            "product_image": "http://example.com/rolex-submariner.jpg",
        },
        {
            "product_name": "Omega Seamaster Professional",
            "product_price": 4599.99,
            "product_discount": 4299.99,
            "product_rating": 4.7,
            "product_url": "http://example.com/omega-seamaster",
            "product_image": "http://example.com/omega-seamaster.jpg",
        },
        {
            "product_name": "Tag Heuer Carrera Chronograph",
            "product_price": 2999.99,
            "product_discount": 2699.99,
            "product_rating": 4.6,
            "product_url": "http://example.com/tag-carrera",
            "product_image": "http://example.com/tag-carrera.jpg",
        },
        {
            "product_name": "Seiko Prospex Diver",
            "product_price": 799.99,
            "product_discount": 649.99,
            "product_rating": 4.5,
            "product_url": "http://example.com/seiko-prospex",
            "product_image": "http://example.com/seiko-prospex.jpg",
        },
        {
            "product_name": "Citizen Eco-Drive Titanium",
            "product_price": 499.99,
            "product_discount": 399.99,
            "product_rating": 4.4,
            "product_url": "http://example.com/citizen-ecodrive",
            "product_image": "http://example.com/citizen-ecodrive.jpg",
        }
    ],
}
