from typing import List
from .helper_functions import retry


class TelegramHelper:
    def __init__(self):
        pass

    @retry(3)
    def send_message(self, message, image_url: str | List[str]):
        if isinstance(image_url, list):
            return self.send_product_with_multiple_image(message, image_url)

        return self.send_product_with_single_image(message, image_url)

    def send_product_with_single_image(self, message, image_url: str):
        print(f"TELEGRAM:- {message}")

    def send_product_with_multiple_image(self, message, image_urls: List[str]):
        print(f"TELEGRAM:- {message}")
