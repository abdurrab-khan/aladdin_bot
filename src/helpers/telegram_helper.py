from typing import List
from os import getenv
from telegram import Bot
from logging import info
from telegram import InputMediaPhoto
from telegram.request import HTTPXRequest

from .helper_functions import retry


class TelegramHelper:
    def __init__(self):
        self.token = getenv("TELEGRAM_TOKEN")
        self.chat_id = getenv("TELEGRAM_CHAT_ID")
        request = HTTPXRequest(
            connection_pool_size=20, connect_timeout=20, read_timeout=20
        )
        self.bot = Bot(token=self.token, request=request)

    @retry(3)
    def send_message(self, message, image_url: str | List[str]):
        if isinstance(image_url, list):
            self.send_product_with_multiple_image(message, image_url)
        else:
            self.send_product_with_single_image(message, image_url)

        info(f"📩 Message sent to Telegram: {message} \n")

    def send_product_with_single_image(self, message, image_path: str):
        self.bot.send_photo(
            chat_id=self.chat_id,
            photo=image_path,
            caption=message,
            parse_mode="HTML",
        )

    def send_product_with_multiple_image(self, message, images_path: List[str]):
        media = [InputMediaPhoto(
            media=path, caption=message, parse_mode="HTML"
        ) for path in images_path]

        self.bot.send_media_group(
            chat_id=self.chat_id,
            media=media,
        )
