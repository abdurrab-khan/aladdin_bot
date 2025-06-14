from time import sleep
from logging import warning

from ..lib.types import Websites


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
                        return None
        return wrapper
    return decorator


def convert_to_number(value_str: str) -> int:
    """
    Convert strings like '18.4k', '1.5m', '2.3b' to actual numbers.

    Args:
        value_str (str): String with number and suffix (k, m, b)

    Returns:
        float: The actual numeric value
    """
    if not isinstance(value_str, str):
        return int(value_str)

    value_str = value_str.lower().replace("|", "").strip()

    if value_str[-1].isdigit():
        return int(value_str)

    suffix = value_str[-1]
    number = float(value_str[:-1])

    multipliers = {
        'k': 1_000,
        'm': 1_000_000,
        'b': 1_000_000_000,
        't': 1_000_000_000_000
    }

    return int(number * multipliers.get(suffix, 1))


class HelperFunctions:
    """A collection of helper functions for various tasks."""

    @staticmethod
    def format_price(price: str, website_name: Websites) -> float:
        if website_name == Websites.AMAZON or website_name == Websites.FLIPKART:
            return float(price.replace("₹", "").replace(",", "").strip())

        elif website_name == Websites.MYNTRA:
            return float(price.replace("Rs.", "").replace(",", "").strip())

        return float(price)

    @staticmethod
    def format_rating(rating: str, website_name: Websites) -> float:
        if website_name == Websites.AMAZON:
            return float(rating.split(" ")[0])

        elif website_name == Websites.FLIPKART or website_name == Websites.MYNTRA:
            return float(rating)

        return float(rating)

    @staticmethod
    def format_rating_count(rating_count: str, website_name: Websites) -> int:
        if website_name == Websites.AMAZON:
            return int(rating_count.replace(",", "").replace(".", ""))

        elif website_name == Websites.FLIPKART:
            return int(rating_count.split(" ")[0].replace(",", "").replace(".", ""))

        elif website_name == Websites.MYNTRA:
            return convert_to_number(rating_count)
