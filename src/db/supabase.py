from logging import error, warning
from time import sleep
from typing import List
from supabase import create_client, Client
from supabase.client import ClientOptions
from os import getenv

from ..lib.types import Product


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


class SupaBaseClient:
    def __init__(self) -> None:
        url = getenv("SUPABASE_URL")
        key = getenv("SUPABASE_KEY")

        if not all([key, url]):
            raise ValueError("Supabase url and Supabase key is required")

        self.supabase_url: str = url  # type: ignore
        self.supabase_key: str = key  # type: ignore

        self.MAIN_TABLE = "products"

    def connect(self):
        try:
            supabase_client: Client = create_client(
                self.supabase_url,
                self.supabase_key,
                options=ClientOptions(
                    postgrest_client_timeout=10,
                    storage_client_timeout=10,
                    schema="public"
                )
            )

            self.supabase = supabase_client

            return self
        except Exception as e:
            error(f"⛔ Unexpected error: {e}")
            return False

    @retry(3)
    def insert_products(self, products: List[Product]):
        res = self.supabase.rpc("insert_products", {
            "products": products
        }).execute()

        return res
