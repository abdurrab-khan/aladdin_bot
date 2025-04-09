from time import sleep
from requests import get
from datetime import datetime
from urllib.parse import unquote
from typing import Optional, List
from random import uniform, choice
from os import path, makedirs, remove
from re import sub, IGNORECASE, search
from logging import warning, info, basicConfig, INFO, error
from ..constants.messages import MESSAGE_TEMPLATES
from ..constants.regex import COLORS, UNWANTED_CHARS
from ..lib.types import SendMessageTo, Product, ProductVariants
from ..constants.product import IMAGE_PATH


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
        return wrapper
    return decorator


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
        Also removes multiple spaces and leading/trailing spaces.

        args:
            product_name: str - The product name to normalize.

        return:
            str - The normalized product name.
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
    def generate_message(sendTo: SendMessageTo, product: Product | ProductVariants) -> str:
        """
        Generate a message based on the product details and the platform to send it to.
        The message is formatted using predefined templates.

        args:
            sendTo: SendMessageTo - The platform to send the message to.
            product: Product | ProductVariants - The product details. 

        return:
            str - The formatted message.
        """
        message = ""

        product_name = product.get(
            "product_name") or product.get("variant_name")
        product_price = product.get(
            "product_price") or product.get("variant_price")
        product_discount = product.get(
            "product_discount") or product.get("variant_discount")
        product_url = product.get("product_url") or " \n".join(
            product.get("variant_urls"))
        product_rating = product.get("product_rating")
        product_discount_percentage = int(
            (product_price - product_discount) / product_price * 100)

        message += MESSAGE_TEMPLATES[sendTo].format(
            product_name=product_name,
            product_price=product_price,
            product_discount=product_discount,
            stars=int(product_rating or 0) * '⭐',
            product_rating=product_rating,
            product_discount_percentage=product_discount_percentage,
            product_url=product_url
        )

        return message

    @staticmethod
    def delete_images(image_paths: str | List[str]):
        """
        Delete images from the given paths.

        args:
            image_paths: str | List[str] - The paths of the images to delete.

        return:
            None
        """
        images = [image_paths] if isinstance(image_paths, str) else image_paths

        for path in images:
            try:
                if path.exists(image_paths):
                    remove(image_paths)
                    info(f"Deleted file: {image_paths}")
                else:
                    warning(f"File not found: {image_paths}")
            except OSError as e:
                error(f"Error deleting file {image_paths}: {e}")

    @staticmethod
    @retry(3)
    def download_image(image_url: str) -> str | None:
        """
        Download an image from a URL with error handling and retries.

        args:
            image_url: str - The URL of the image to download.

        return:
            str | None - The path to the downloaded image or None if the download failed.
        """
        makedirs(IMAGE_PATH, exist_ok=True)
        current_time = int(datetime.timestamp(datetime.now()))
        save_path = f"{IMAGE_PATH}/{current_time}.jpg"

        headers = [
            {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'
            },
        ]

        response = get(
            image_url, headers=choice(headers), timeout=10, stream=True)

        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            warning(
                f"URL does not contain an image (Content-Type: {content_type})")
            return None

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        sleep(1.5)

        image_size = path.getsize(save_path)
        info(
            f"Successfully downloaded {image_url} ({image_size} bytes) to {save_path}")

        return save_path
