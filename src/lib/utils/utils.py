from typing import List, Optional
from helpers.helper_functions import retry
from helpers.selenium_helper import SeleniumHelper
from src.lib.types import Product, ProductSearchResult, Websites
from const import MAX_PRICE, MIN_PRICE 
from ml_model.predict_deal import predict_deal

class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(url:str,website_name:Websites) -> ProductSearchResult | None:
        """
        Get products from a given URL and return a list of Product objects 
        """

        max_retry = 3
        @retry(max_retry)
        def get_products(url:str,website_name:Websites) -> List[Product] | None:
            selenium_helper = SeleniumHelper()
            return selenium_helper.get_products(url, website_name)
        
        return get_products(url,website_name)

    @staticmethod
    def sort_products(product: Optional[List[Product]] = None) -> List[Product] | None:
        """
        Sort the products based on the discount price
        """
        pass
    
    # Send message to Telegram and Twitter
    @staticmethod
    def send_telegram_message(message: Optional[Product] = None) -> None:
        """
        Send a message to the Telegram channel
        """
        pass

    @staticmethod
    def send_twitter_message(message: Optional[Product] = None) -> None:
        """
        Send a message to the Twitter channel
        """
        pass