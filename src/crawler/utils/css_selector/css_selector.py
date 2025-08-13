from typing import Dict, List
from ....lib.types import Websites, ProductKey


# CSS Selectors for each website to extract product details.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_DETAILS: Dict[Websites, Dict[ProductKey, List[str]]] = {
    Websites.AMAZON: {
        "name": ["h2.a-size-base-plus.a-spacing-none span"],
        "price": ["span.a-price.a-text-price span.a-offscreen"],
        "discount_price": ["span.a-price-whole", "span#priceblock_ourprice"],
        "rating": ["span.a-icon-alt"],
        "rating_count": ["span.a-size-base.s-underline-text"],
        "product_image": ["img.s-image"],
        "product_url": ["a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal", "a.a-link-normal"],
    },
    Websites.FLIPKART: {
        "name": ["span.VU-ZEz"],
        "price": [r"div.yRaY8j"],
        "discount_price": ["div.hl05eU div.Nx9bqj"],
        "rating": ["div.XQDdHH"],
        "rating_count": ["span.Wphh3N"],
        "product_image": ["div._8id3KM img"],
        "product_url": ["a.rPDeLR"],
    },
    Websites.MYNTRA: {
        "name": ["h4.product-product"],
        "price": ["div.product-price span .product-strike"],
        "discount_price": ["div.product-price span .product-discountedPrice"],
        "rating": ["div.product-ratingsContainer span"],
        "rating_count": ["div.product-ratingsCount"],
        "product_image": ["div.product-imageSliderContainer img"],
        "product_url": ["a"],
    },
}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CONTAINER: Dict[Websites, str] = {
    Websites.AMAZON: "div.s-main-slot.s-result-list",
    Websites.FLIPKART: "div.DOjaWF.gdgoEp:not(.col-2-12):not(.col-12-12), div.DOjaWF.YJG4Cf",
    Websites.MYNTRA: "div.search-searchProductsContainer.row-base",
}


# CSS Selectors for each website to extract product cards.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_CARDS: Dict[Websites, str] = {
    Websites.AMAZON: "div.a-section.a-spacing-base",
    Websites.FLIPKART: "div._1sdMkc.LFEi7Z",
    Websites.MYNTRA: "li.product-base",
}


NEXT_BUTTON: Dict[Websites, str] = {
    Websites.AMAZON: "span.s-pagination-strip a.s-pagination-next",
    Websites.FLIPKART: "nav.WSL9JP a._9QVEpD",
    Websites.MYNTRA: "li.pagination-next",
}
