from os import getenv
from typing import List
from logging import info
from telegram import Bot
from telegram import InputMediaPhoto
from telegram.request import HTTPXRequest
from os import path

from .helper_functions import retry


class TelegramHelper:
    def __init__(self):
        self.token = getenv("TELEGRAM_TOKEN")
        self.chat_id = getenv("TELEGRAM_CHAT_ID")

        if not all([self.token, self.chat_id]):
            raise ValueError(
                "⛔ Missing Telegram credentials in environment variables.")

        request = HTTPXRequest(
            connection_pool_size=20, connect_timeout=20, read_timeout=20
        )
        self.bot = Bot(token=self.token, request=request)

    @retry(3)
    async def send_message(self, message, image_url: str | List[str]):
        """
        Send a message to the telegram bot with an image or multiple images.

        args:
            message: The message to send.
            image_url: The image url or list of image urls to send.

        return:
            None
        """
        if isinstance(image_url, list):
            await self.send_product_with_multiple_image(message, image_url)
        else:
            await self.send_product_with_single_image(message, image_url)

        info(f"✅ Message successfully sent to Telegram 📲")

    async def send_product_with_single_image(self, message, image_path: str):
        await self.bot.send_photo(
            chat_id=self.chat_id,
            photo=image_path,
            caption=message,
            parse_mode="HTML",
        )

    async def send_product_with_multiple_image(self, message, images_path: List[str]):
        media = [InputMediaPhoto(
            media=path, caption=message, parse_mode="HTML"
        ) for path in images_path]

        await self.bot.send_media_group(
            chat_id=self.chat_id,
            media=media,
        )
