from enum import Enum
from os import getenv
from json import dumps
from typing import List
from dotenv import load_dotenv
from requests import get, post
from logging import info,  warning

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

    def send_post(self, message: List[str], image_url: str | List[str]) -> None:
        """
        Send a post to Meta (Facebook/Instagram) using the Graph API.

        args:
            message (str): The message to be sent.
            image_path (str): The path to the image to be sent.

        return:
            None
        """

        # Send to FB page.
        self.send_to_fb_page(message[0], image_url)

        # # Send to IG.
        self.send_to_ig(message[-1], image_url)

    def send_to_fb_page(self, message: str, image_urls: List[str]) -> None:
        """
        Send a post to the Facebook page.

        args:
            message (str): The message to be sent.
            image_path (str): The path to the image to be sent.

        return:
            None
        """
        try:
            attached_media = ""

            if isinstance(image_urls, str):
                image_id = self.upload_image_on_meta(
                    image_urls, MetaAppTypes.FACEBOOK, message)

                if image_id is not None:
                    attached_media = {"media_fbid": image_id}
            else:
                attached_media = []

                for url in image_urls:
                    image_id = self.upload_image_on_meta(
                        url, MetaAppTypes.FACEBOOK)

                    if image_id is not None:
                        attached_media.append({"media_fbid": image_id})

            self.send_post_req(message, dumps(
                attached_media), MetaAppTypes.FACEBOOK)
        except Exception as e:
            warning(f"⛔ Failed to send post to Facebook page: {e}")

    def send_to_ig(self, message: str, image_url: str | List[str]) -> None:
        """
        Send a post to Instagram.

        args:
            message (str): The message to be sent.
            image_path (str): The path to the image to be sent.

        return:
            None
        """
        try:
            creation_id = None

            if isinstance(image_url, str):
                image_id = self.upload_image_on_meta(
                    image_url, MetaAppTypes.INSTAGRAM, message)

                if image_id is not None:
                    creation_id = image_id
            else:
                container_ids = []

                for url in image_url:
                    image_id = self.upload_image_on_meta(
                        url, MetaAppTypes.INSTAGRAM)

                    if image_id is not None:
                        container_ids.append(image_id)

                if len(container_ids) > 1:
                    creation_id = self.create_carousel(message, container_ids)
                else:
                    creation_id = container_ids[0]

            self.send_post_req(message, creation_id, MetaAppTypes.INSTAGRAM)
        except Exception as e:
            warning(f"⛔ Failed to send post to Instagram: {e}")

    @retry(3)
    def send_post_req(self, message: str, send_data: str, app: MetaAppTypes) -> None:
        """
        Sends a POST request to the Meta Graph API to publish content on Instagram or Facebook.

        args:
            message (str): The message to be sent.
            send_data (str): The data to be sent in the request.
            app (MetaAppTypes): The application type (Instagram or Facebook).

        return:
            None
        """
        if send_data is None:
            return

        if app == MetaAppTypes.INSTAGRAM:
            api = f"https://graph.facebook.com/v22.0/{self.ig_id}/media_publish"
            params = {
                "creation_id": send_data,
                "access_token": self.access_token
            }
        elif app == MetaAppTypes.FACEBOOK:
            api = f"https://graph.facebook.com/v22.0/{self.fb_page_id}/feed"
            params = {
                'message': message,
                'attached_media': send_data,
                'access_token': self.page_token
            }

        response = post(api, params=params)
        response_data = response.json()

        if response.status_code < 202:
            if app == MetaAppTypes.INSTAGRAM:
                info(f"📸 Instagram post created: {response_data['id']}")
            else:
                info(f"📩 Facebook post created: {response_data['id']}")
        else:
            if "error" in response_data:
                if response_data["error"]["code"] == -1 and app == MetaAppTypes.INSTAGRAM:
                    raise Exception("⛔ Failed to create carousel post.")
                else:
                    warning(
                        f"⛔ Failed to create carousel post: {response_data['error']['message']}")

    @retry(3)
    def create_carousel(self, message: str, container_id: List[str]) -> str:
        """
        Create a carousel post on Instagram.

        args:
            container_id(str): The ID of the post container.

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
            info(f"➕ Carousel post created: {response_data['id']}")
            return response_data["id"]
        else:
            if "error" in response_data:
                if response_data["error"]["code"] == -1:
                    raise Exception("⛔ Failed to create carousel post.")
                else:
                    warning(
                        f"⛔ Failed to create carousel post: {response_data['error']['message']}")

    @retry(3)
    def upload_image_on_meta(self, image_url: str, app: MetaAppTypes, caption: str = None) -> str:
        """
        Upload an image to Meta(Facebook/Instagram) using the Graph API.

        args:
            image_path(str): The path to the image to be uploaded.
        return:
            str: The Id of the uploaded image.
        """
        if app == MetaAppTypes.INSTAGRAM:
            api = f"https://graph.facebook.com/v22.0/{self.ig_id}/media"
            params = {
                'image_url': image_url,
                'access_token': self.access_token
            }

            if caption:
                params['caption'] = caption

        elif app == MetaAppTypes.FACEBOOK:
            api = f"https://graph.facebook.com/v22.0/{self.fb_page_id}/photos"
            params = {
                'url': image_url,
                'published': 'false',
                'access_token': self.page_token
            }

        response = post(api, params=params)

        response_data = response.json()
        if response.status_code < 202:
            info(f"✅ Image uploaded: {response_data['id']}")
            image_id = response_data["id"]
            return image_id
        else:
            if "error" in response_data:
                if response_data["error"]["code"] == -1:
                    raise Exception("⛔ Failed to create carousel post.")
                else:
                    warning(
                        f"⛔ Failed to create carousel post: {response_data['error']['message']}")
