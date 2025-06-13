from json import dumps
from logging import error
from typing import List
from supabase import create_client, Client
from supabase.client import ClientOptions
from os import getenv

from ..helpers.helper_functions import retry
from ..lib.types import Product


class SupaBaseClient:
    def __init__(self) -> None:
        url = getenv("SUPABASE_URL")
        key = getenv("SUPABASE_KEY")

        if not all([key, url]):
            raise ValueError("Supabase url and Supabase key is required")

        self.supabase_url: str = url  # type: ignore
        self.supabase_key: str = key  # type: ignore

        self.MAIN_TABLE = "products"

    def __enter__(self):

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

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            error(
                f"⛔ An error occurred while disconnecting the db: {exc_value}")
            return False

        return True

    @retry(3)
    def insert_products(self, products: List[Product]):
        res = self.supabase.rpc("insert_products", {
            "products": products
        }).execute()

        return res
