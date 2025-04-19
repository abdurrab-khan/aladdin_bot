from typing import Dict, List
from ..lib.types import Websites, ProductKey


# CSS Selectors for each website to extract product details.
# These selectors are used to locate and extract specific information from the HTML structure of the product pages.
PRODUCT_DETAILS: Dict[Websites, Dict[ProductKey, List[str]]] = {
    Websites.AMAZON: {
        "product_name": ["h2.a-size-base-plus.a-spacing-none span"],
        "product_price": ["span.a-price.a-text-price span.a-offscreen"],
        "product_discount": ["span.a-price-whole", "span#priceblock_ourprice"],
        "product_image_url": ["img.s-image"],
        "product_rating": ["span.a-icon-alt"],
        "product_url": ["a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal", "a.a-link-normal"],
    },
    Websites.FLIPKART: {
        "product_name": ["span.VU-ZEz"],
        "product_price": [r"div.yRaY8j"],
        "product_discount": ["div.Nx9bqj.CxhGGd"],
        "product_image_url": ["div._8id3KM img"],
        "product_rating": ["div.XQDdHH"],
        "product_url": ["a.rPDeLR"],
    },
    Websites.MYNTRA: {
        "product_name": ["h4.product-product"],
        "product_price": ["div.product-price span .product-strike"],
        "product_discount": ["div.product-price span .product-discountedPrice"],
        "product_image_url": ["div.product-imageSliderContainer img"],
        "product_rating": ["div.product-ratingsContainer span"],
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
