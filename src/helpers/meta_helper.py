from os import getenv
from typing import List
from logging import info,  warning
from dotenv import load_dotenv
from requests import get, post
from json import dumps
from enum import Enum

from ..db.redis import RedisDB
from ..helpers import retry

load_dotenv()


class MetaAppTypes(Enum):
    """
    Enum class for Meta application types.
    """
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"


class MetaHelper:
    def __init__(self):
        self.access_token = getenv("META_ACCESS_TOKEN")
        self.page_token = getenv("META_PAGE_TOKEN")
        self.ig_id = getenv("META_IG_ID")
        self.fb_page_id = getenv("META_FB_PAGE_ID")

        if not all([self.access_token, self.page_token, self.ig_id, self.fb_page_id]):
            raise ValueError(
                "⛔ Missing Meta API credentials in environment variables.")

        # self.get_days_until_token_expiration()

    def get_days_until_token_expiration(self) -> int:
        """
        Calculate the remaining days until the access token expires.

        Returns:
            int: Number of days remaining before token expiration.
        """
        url = f"https://graph.facebook.com/debug_token?input_token={self.access_token}&access_token={self.access_token}"
        response = get(url).json()

        if "data" in response and "expires_at" in response["data"]:
            pass
        else:
            raise ValueError("⛔ Failed to retrieve token expiration data.")

    def send_post(self, message: str, image_urls: str | List[str]) -> None:
        """
        Send a post to Meta (Facebook/Instagram) using the Graph API.

        args:
            message (str): The message to be sent.
            image_path (str): The path to the image to be sent.

        return:
            None
        """
        images_url = [image_urls] if isinstance(
            image_urls, str) else image_urls

        # Send to FB page.
        self.send_to_fb_page(message, images_url)

        # Send to IG.
        self.send_to_ig(message, images_url)

    def send_to_fb_page(self, message: str, image_urls: List[str]) -> None:
        """
        Send a post to the Facebook page.

        args:
            message (str): The message to be sent.
            image_path (str): The path to the image to be sent.

        return:
            None
        """
        attached_media = []
        for url in image_urls:
            image_id = self.upload_image_on_meta(url, MetaAppTypes.FACEBOOK)

            if image_id is not None:
                attached_media.append({"media_fbid": image_id})

        api = f"https://graph.facebook.com/v22.0/{self.fb_page_id}/feed"
        payload = {
            'message': message,
            'attached_media': dumps(attached_media),
            'access_token': self.page_token
        }
        response = post(api, params=payload)

        response.raise_for_status()
        response_data = response.json()
        if response.status_code < 202:
            info(f"✅ Post sent to Facebook page: {self.fb_page_id}")
        else:
            if "error" in response_data:
                if response_data["error"]["code"] == -1:
                    raise Exception("⛔ Failed to create carousel post.")
                else:
                    warning(
                        f"⛔ Failed to create carousel post: {response_data['error']['message']}")

    def send_to_ig(self, message: str, image_urls: str | List[str]) -> None:
        """
        Send a post to Instagram.

        args:
            message (str): The message to be sent.
            image_path (str): The path to the image to be sent.

        return:
            None
        """
        container_ids = []
        for url in image_urls:
            container_id = self.upload_image_on_meta(
                url, MetaAppTypes.INSTAGRAM)

            if container_id is not None:
                container_ids.append(container_id)
        carousel_id = self.create_carousel(message, container_ids)

        api = f"https://graph.facebook.com/v22.0/{self.ig_id}/media_publish"
        params = {
            "creation_id": carousel_id,
            "access_token": self.access_token
        }

        response = post(api, params=params)
        response.raise_for_status()
        response_data = response.json()

        if response.status_code < 202:
            info(f"✅ Post sent to Instagram: {self.ig_id}")
        else:
            warning(
                f"⛔ Failed to send post to Instagram: {response_data['error']['message']}")

    @retry(3)
    def create_carousel(self, message: str, container_id: List[str]) -> str:
        """
        Create a carousel post on Instagram.

        args:
            container_id (str): The ID of the post container.

        return:
            str: The ID of the created carousel post.
        """
        api = f"https://graph.facebook.com/v22.0/{self.ig_id}/media"
        params = {
            "creation_id": container_id,
            "media_type": "CAROUSEL",
            "caption": message,
            "children": " ,".join(container_id),
            "access_token": self.access_token
        }

        response = post(api, params=params)
        response.raise_for_status()

        response_data = response.json()
        if response.status_code < 202:
            return response_data["id"]
        else:
            if "error" in response_data:
                if response_data["error"]["code"] == -1:
                    raise Exception("⛔ Failed to create carousel post.")
                else:
                    warning(
                        f"⛔ Failed to create carousel post: {response_data['error']['message']}")

    @retry(3)
    def upload_image_on_meta(self, image_url: str, app: MetaAppTypes) -> str:
        """
        Upload an image to Meta (Facebook/Instagram) using the Graph API.

        args:
            image_path (str): The path to the image to be uploaded.
        return:
            str: The Id of the uploaded image.
        """
        if app == MetaAppTypes.INSTAGRAM:
            api = f"https://graph.facebook.com/v22.0/{self.ig_id}/media"
            data = {
                'image_url': image_url,
                'access_token': self.access_token
            }

        elif app == MetaAppTypes.FACEBOOK:
            api = f"https://graph.facebook.com/v22.0/{self.fb_page_id}/photos"
            data = {
                'url': image_url,
                'published': 'false',
                'access_token': self.page_token
            }

        response = post(api, params=data)

        print(f"Response: {response.status_code}")
        print(f"Text: {response.text}")

        response.raise_for_status()

        response_data = response.json()

        if response.status_code < 202:
            image_id = response_data["id"]
            return image_id
        else:
            if "error" in response_data:
                if response_data["error"]["code"] == -1:
                    raise Exception("⛔ Failed to create carousel post.")
                else:
                    warning(
                        f"⛔ Failed to create carousel post: {response_data['error']['message']}")
