from logging import error
from re import search, sub
from typing import Optional, cast
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from ...db.redis import RedisDB
from ...constants.const import ASSOCIATED_APP, USER_ID
from ..utils.css_selector.css_selector import PRODUCT_DETAILS
from ...constants.url import PLATFORM_IDS, PRODUCT_URL_DETAILS

from selenium.webdriver.remote.webelement import WebElement
from ...helpers.helper_functions import HelperFunctions
from ...lib.types import Product, ProductCategories, ProductKey, Websites


def increaseImageQuality(image_url: str, website: Websites) -> str:
    if website == Websites.MYNTRA:
        return image_url.replace('q_60', 'q_100').replace('w_210', 'w_510')
    elif website == Websites.AMAZON:
        return image_url.replace('_AC_UL320_', '_AC_UL720_')
    elif website == Websites.FLIPKART:
        encoded_url = unquote(image_url)

        # Replace the size (e.g /612/612 -> /720/720)
        url = sub(r"/image/[0-9]+/[0-9]+", f"/image/720/720", encoded_url)

        # Replace the quality (e.g. q=70 → q=100)
        url = sub(r"q=\d+", f"q=100", url)

        return url


class DataProcessingHelper:
    """
    Handles data processing, formatting, and validation operations.
    This class contains helper methods for processing scraped data.
    """

    @staticmethod
    def get_product_details(card: WebElement, website_name: Websites, category: ProductCategories) -> Optional[Product]:
        """
        Extract product details from the BeautifulSoup object.

        Args:
            soup (Tag): The BeautifulSoup object containing product data.
            website_name (Website): Name of the website
            category (ProductCategories): Category of the product

        Returns:
            Optional[Product]: A dictionary containing product details.
        """
        product_details: Product = {}

        for key, selectors in PRODUCT_DETAILS[website_name].items():
            try:
                element = DataProcessingHelper.extract_product_detail(
                    card, ", ".join(selectors))
                formatted_data = DataProcessingHelper.format_extracted_data(
                    key, element, website_name)

                isProductValid = formatted_data is None and not (
                    website_name == Websites.FLIPKART and (key == "rating" or key == "rating_count"))

                if isProductValid:
                    return None

                if key == "product_image":
                    url = cast(str, formatted_data)
                    image_url = increaseImageQuality(url, website_name)
                    formatted_data = image_url

                product_details[key] = formatted_data
            except Exception as e:
                error(f"Error extracting {key}: {str(e)}")
                return None

        if USER_ID is None or ASSOCIATED_APP is None:
            error(
                "💀 USER_ID and ASSOCIATED_APP is None check immediately what's wrong...")
            return None

        if product_details:
            product_details["user_id"] = USER_ID
            product_details["platform_id"] = PLATFORM_IDS[website_name.value]
            product_details["category"] = category.value
            product_details["associated_app"] = ASSOCIATED_APP

        return product_details

    @staticmethod
    def format_extracted_data(key: ProductKey, element_data: WebElement | None, website_name: Websites):
        """
        Format the extracted data based on the selector type.

        Args:
            key (ProductKey): The type of data to format.
            element_data (BeautifulSoup | None): The extracted data to format.

        Returns:
            Union[float, int, str, None]: The formatted data.
        """
        if element_data is None:
            return None

        element = None
        if key == "product_image" or key == "product_url":
            attr = "href" if key == "product_url" else "src"
            element = element_data.get_attribute(attr)

            if element is None:
                return None

            return element if key == "product_image" else DataProcessingHelper.url_shorter(element, website_name)
        else:
            elem = element_data.get_attribute("innerHTML")

            if elem is not None:
                soup = BeautifulSoup(elem, "html.parser")
                element = soup.text

        if element is None:
            return None

        # Format the give data by website_name
        if key == "price" or key == "discount_price":
            return HelperFunctions.format_price(element, website_name)

        elif key == "rating":
            return HelperFunctions.format_rating(element, website_name)

        elif key == "rating_count":
            return HelperFunctions.format_rating_count(element, website_name)

        return element

    @staticmethod
    def is_product_valid(url: str | None, original_price: str | int | float | None, redis: RedisDB, category: ProductCategories) -> bool:
        """
        Validate if a product has the necessary information.

        Args:
            price (BeautifulSoup): The price element.
            url (BeautifulSoup): The URL element.

        Returns:
            bool: True if the product is valid, False otherwise.
        """
        if url is None or original_price is None:
            return False

        if not isinstance(original_price, (float, int)):
            return False

        price_limit = PRODUCT_URL_DETAILS[category]["max_price"]

        if original_price < price_limit:
            if redis.is_url_cached(url):
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def url_shorter(url: str, website_name: Websites) -> str | None:
        """
        Generate a short URL with the affiliate code based on the website.

        Args:
            url (str): The original URL to shorten.

        Returns:
            str: The short URL with the affiliate code.
        """
        # URL shortening and affiliate code addition logic
        formatted_url = None

        if website_name == Websites.AMAZON:
            return DataProcessingHelper.parse_amazon_url(url)

        elif website_name == Websites.FLIPKART:
            return DataProcessingHelper.parse_flipkart_url(url)

        elif website_name == Websites.MYNTRA:
            formatted_url = f"https://www.myntra.com/{url}"

        return unquote(formatted_url, encoding="utf-8") if formatted_url is not None else formatted_url

    @staticmethod
    def parse_amazon_url(url: str) -> str | None:
        click_pattern = r'/sspa/click'  # Url with click href
        url_pattern = r'/dp/([a-zA-Z0-9]{10})'  # Url with dp/product_id href

        # Decode the url
        decoded_url = unquote(url)

        # Parsed_url
        parsed_url = urlparse(decoded_url)
        formatted_url = parsed_url.scheme + "://" + parsed_url.netloc

        # Search /dp/product_id
        if search(url_pattern, decoded_url):
            try:
                parse_query_url = urlparse(parse_qs(urlparse(url).query)['url'][0]).path if search(
                    click_pattern, decoded_url) else parsed_url.path

                # Remove /ref=....
                clean_url = sub(r"/ref=[^/]+", "", parse_query_url)

                # Concat clean url into formatted_url
                formatted_url += clean_url
            except KeyError as k:
                return None

        return formatted_url

    @staticmethod
    def parse_flipkart_url(url: str) -> str | None:
        encoded_url = unquote(url)

        # Parse url
        parsed_url = urlparse(encoded_url)

        # Return parsed url
        return parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    @staticmethod
    def extract_product_detail(card: WebElement, selector: str):
        try:
            element = card.find_element(By.CSS_SELECTOR, selector)

            if element is not None:
                return element

        except Exception:
            return None
