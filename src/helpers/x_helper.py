from os import path
from os import getenv
from typing import List
from requests import post
from logging import warning, info
from requests_oauthlib import OAuth1

from ..helpers.helper_functions import retry


class XHelper:
    def __init__(self):
        self.consumer_key = getenv("X_API_KEY")
        self.consumer_secret = getenv("X_API_SECRET_KEY")
        self.token = getenv("X_ACCESS_TOKEN")
        self.token_secret = getenv("X_ACCESS_TOKEN_SECRET")

        if not all([self.consumer_key, self.consumer_secret, self.token, self.token_secret]):
            raise ValueError(
                "⛔ Missing Twitter API credentials in environment variables.")

        self.auth = OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.token,
            resource_owner_secret=self.token_secret,
        )

        self.api_url = "https://api.twitter.com/2/tweets"
        self.media_url = "https://upload.twitter.com/1.1/media/upload.json"
        self.header = {
            "Content-Type": "application/json",
        }

    @retry(3)
    def send_message(self, message: str, image: List[str] | str = []) -> None:
        """
        Send a message to the Twitter API with an image or multiple images.

        args:
            message: The message to send.
            image: The image url or list of image urls to send.

        return:
            None
        """
        media_ids = []
        payload = {
            "text": message,
        }
        image = image if isinstance(image, list) else [image]

        for img_path in image:
            media_id = self.upload_media(img_path)
            if media_id:
                media_ids.append(media_id)

        if media_ids:
            payload["media"] = {
                "media_ids": media_ids,
            }

        response = post(
            self.api_url,
            json=payload,
            auth=self.auth,
            headers=self.header,
        )

        if response.status_code != 201:
            warning(f"⚠️ Failed to send message on X 🕊️: {response.text}")
        else:
            info(f"✅ Message successfully sended to X 🕊️")

    @retry(3)
    def upload_media(self, img_path: str) -> str:
        """
        Upload media to Twitter.

        args:
            img_path: The path to the image.

        return:
            media_id: The media id of the uploaded image.
        """
        if not path.exists(img_path):
            warning(f"⚠️ Image not found: {img_path}")
            return None

        with open(img_path, "rb") as file:
            files = {
                "media": file,
            }

            response = post(
                self.media_url, auth=self.auth, files=files
            )

            if response.status_code == 200:
                media_id = response.json().get("media_id_string")
                return media_id
            else:
                warning(f"⚠️ Failed to upload media: {response.text}")
                return None
