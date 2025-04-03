from time import sleep
from typing import Optional
from os import path, makedirs
from ..ml_model.predict_deal import predict_deal
from ..lib import MSG_TEMPLATE_BY_NAME, IMAGE_PATH, ProductVariants, SendMessageTo, Product, COLORS, UNWANTED_CHARS, Websites, AMAZON_AFFILIATE_ID, FLIPKART_AFFILIATE_ID, MYNTRA_AFFILIATE_ID, AJIO_AFFILIATE_ID
from re import sub, IGNORECASE, search
from requests import get
from datetime import datetime
from logging import warning, info, error, basicConfig, INFO
from urllib.parse import unquote

basicConfig(
    level=INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Decorators


def retry(max_retries: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for retry_count in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry_count < max_retries - 1:
                        wait_time = 2 ** retry_count
                        warning(
                            f"Attempt {retry_count + 1}/{max_retries} failed: {str(e)}. Retrying in {wait_time} seconds...")
                        sleep(wait_time)
                    else:
                        raise
        return wrapper
    return decorator


def format_message(sendTo: SendMessageTo, product_name: str, product_price: str, product_discount: str, product_rating: str, product_url: str, product_discount_percentage: str) -> str:
    message = MSG_TEMPLATE_BY_NAME[sendTo].format(
        product_name=product_name,
        product_price=product_price,
        product_discount=product_discount,
        stars=product_rating * '⭐',
        product_rating=product_rating,
        product_discount_percentage=product_discount_percentage,
        product_url=product_url
    )

    return message


def extract_amazon_product_id(url):
    decoded_url = unquote(url)
    pattern = r'/dp/([a-zA-Z0-9]{10})'

    match = search(pattern, decoded_url)

    if match:
        return match.group(1)
    else:
        raise (f"Invalid Amazon URL: {url}")


class HelperFunctions:
    @staticmethod
    def normalize_name(product_name) -> str:
        """
        Normalize the product name by removing colors, numbers, and unwanted characters.
        """
        colors = rf"\b({COLORS})\b"
        numbers = r"\d+"

        # Remove Colors from product name (with word boundaries)
        product_name = sub(colors, " ", product_name, flags=IGNORECASE)

        # Remove Numbers from product name
        product_name = sub(numbers, " ", product_name)

        # Remove unwanted_characters from product name
        product_name = sub(UNWANTED_CHARS, " ", product_name)

        # Remove Multiple Spaces
        product_name = sub(r"\s+", " ", product_name)

        return product_name.strip()

    @staticmethod
    def get_product_color(product_name) -> str | None:
        """
        Get the color of the product from the product name.
        """
        colors = rF"\b({COLORS}\d+)\b"

        color_match = search(colors, product_name, flags=IGNORECASE)

        if color_match:
            matched_color = color_match.group(0).strip()

            return matched_color.lower()
        else:
            return None

    @staticmethod
    def short_url_with_affiliate_code(url: str, website: Websites) -> str:
        """
        Shorten the URL and add affiliate code to the URL
        """
        match website:
            case Websites.AMAZON:
                product_id = extract_amazon_product_id(url)
                short_url = f"https://www.amazon.in/dp/{product_id}/{AMAZON_AFFILIATE_ID}"
                return short_url
            case Websites.FLIPKART:
                short_url = f"https://www.flipkart.com{url.split("?")[0]}/{FLIPKART_AFFILIATE_ID}"
                return short_url
            case Websites.MYNTRA:
                return f"https://www.myntra.com{url}/{MYNTRA_AFFILIATE_ID}"
            case Websites.AJIO:
                pass
            case _:
                raise ValueError("Invalid website specified")

    @staticmethod
    def evaluate_products_with_ml(product: Optional[Product] = None) -> Optional[Product]:
        """
        Check if a product is a good deal using a machine learning model.
        Returns the product if it's a good deal, None otherwise.
        """
        if product is None:
            return None

        prediction_result = predict_deal(product)

        if prediction_result['prediction'] == 'Best Deal':
            return product

        return None

    @staticmethod
    def generate_message(sendTo: SendMessageTo, product: Product | ProductVariants) -> str:
        """
        Generate a message for the product
        """
        message = ""

        if isinstance(product, Product):
            product_name = product['product_name']
            product_price = product['product_price']
            product_discount = product['product_discount']
            product_rating = product['product_rating']
            product_url = product['product_url']
            product_discount_percentage = (
                product_price - product_discount) / product_price * 100

            message += format_message(
                sendTo,
                product_name,
                product_price,
                product_discount,
                product_rating,
                product_url,
                product_discount_percentage
            )

        elif isinstance(product, ProductVariants):
            product_name = product['base_product_name']
            product_price = product['variants'][0]['product_price']
            product_discount = product['variants'][0]['product_discount']
            product_discount_percentage = (
                product_price - product_discount) / product_price * 100
            product_average_rating = 0
            product_urls = ""

            for varient in product['variants']:
                product_average_rating += varient['product_rating']
                product_urls += f"{varient.get('product_color', "")} {varient['product_url']}\n"

            product_average_rating = product_average_rating / \
                len(product['variants'])

            message += format_message(
                sendTo,
                product_name,
                product_price,
                product_discount,
                product_average_rating,
                product_urls,
                product_discount_percentage
            )

        return message

    @staticmethod
    def download_image(image_url: str) -> str | None:
        """
        Download an image from a URL with error handling and retries.

        Returns:
            str: Path to downloaded image, or empty string if download failed
        """
        makedirs(path.dirname(IMAGE_PATH), exist_ok=True)
        current_time = int(datetime.timestamp(datetime.now()))
        SAVE_PATH = f"{IMAGE_PATH}/{current_time}.jpg"

        @retry(4)
        def download():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like    Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Make the request with timeout
            response = get(
                image_url, headers=headers, timeout=10, stream=True)

            # Check if response is successful
            response.raise_for_status()

            # Verify content type is an image
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                warning(
                    f"URL does not contain an image (Content-Type: {content_type})")
                return False

            # Save the image
            with open(SAVE_PATH, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            image_size = path.getsize(SAVE_PATH)
            info(
                f"Successfully downloaded {image_url} ({image_size} bytes) to {SAVE_PATH}")
            return True

        try:
            success = download()
            if success:
                return SAVE_PATH
            else:
                return None
        except Exception as e:
            error(f"Failed to download image after multiple attempts: {e}")
            return None
