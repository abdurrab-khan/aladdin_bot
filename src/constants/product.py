from ..lib.types import ProductCategories


# Maximum number of products to scrape from each website during a search operation
MAX_PRODUCTS_PER_WEBSITE = 15

# Product categories for different e-commerce websites.
PRODUCTS_PER_CATEGORY = {
    ProductCategories.JEANS: 3,
    ProductCategories.TSHIRT: 3,
    ProductCategories.SHIRT: 3,
    ProductCategories.CARGO: 2,
    ProductCategories.FOOTWEAR: 2,
    ProductCategories.JACKET: 2,
    ProductCategories.SHORTS: 2,
    ProductCategories.SWEATSHIRTS: 3,
    ProductCategories.TRACKPANT: 3,
    ProductCategories.TROUSER: 3,
    ProductCategories.CASUAL_SHOES: 3,
    ProductCategories.FORMAL_SHOES: 3,
    ProductCategories.SPORTS_SHOES: 3,
    ProductCategories.SNEAKERS: 3,
    ProductCategories.WALLET: 2,
    ProductCategories.WATCHES: 2,
    ProductCategories.SUNGLASSES: 2,
    ProductCategories.PERFUME: 3,
}

PRICE_LIMITS = {
    ProductCategories.JEANS: 2500,
    ProductCategories.TSHIRT: 1500,
    ProductCategories.SHIRT: 1500,
    ProductCategories.CARGO: 1800,
    ProductCategories.FOOTWEAR: 2400,
    ProductCategories.JACKET: 2000,
    ProductCategories.SHORTS: 1200,
    ProductCategories.SWEATSHIRTS: 1500,
    ProductCategories.TRACKPANT: 2000,
    ProductCategories.TROUSER: 2000,
    ProductCategories.CASUAL_SHOES: 2000,
    ProductCategories.FORMAL_SHOES: 2500,
    ProductCategories.SPORTS_SHOES: 2500,
    ProductCategories.SNEAKERS: 2500,
    ProductCategories.WALLET: 1500,
    ProductCategories.WATCHES: 2000,
    ProductCategories.SUNGLASSES: 1200,
    ProductCategories.PERFUME: 1200,
}

TAGS = ["#fashion", "#style", "#ootd", "#instafashion", "#fashionblogger",
        "#fashionista", "#streetstyle", "#stylish", "#fyp", "#foryou", "#viral", "#trending"]

# fashion
# style
# ootd
# fashionblogger
# fashionista
# instafashion
# fashionstyle
# fashiongram
# fashioninspo
# streetstyle
# luxuryfashion
# luxurylifestyle
# highfashion
# mensfashion
# fashionaddict
# modafashion
# fashionstylist
# fashiongirl
# fashionistas
# fashionillustration
# fashioninsta
# fashionshow
# fashiondesign
# fashiondaily
# fashionhijab
# fashionjewelry
# fashionpost
# fashionkids
# hoodie
# fashionmodel
# fashionlover
# styleinspiration
# styling
# stylingtips"
