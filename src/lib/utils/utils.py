from typing import List
from src.lib.types import Product

class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(url:str) -> List[Product]:
        """
        Get products from a given URL and return a list of Product objects 
        """
        pass

    @staticmethod
    def parse_html(html:str) -> List[Product]:
        """
        Parse the HTML content with checking all fields are present or not and return a list of Product objects
        """
        pass

    @staticmethod
    def filter_products(products:List[Product], min_price:float, max_price:float) -> List[Product]:
        """
        Filter the products based on the price range and return a list of Product objects
        """
        pass

    @staticmethod
    def sort_products(products:List[Product]) -> List[Product]:
        """
        Sort the products based on the actual price, discount, rating using random forest regressor and return a list of Product objects
        """
        pass

    @staticmethod
    def short_url_with_affiliate_code(url:str) -> str:
        """
        Shorten the URL and add affiliate code to the URL
        """
        pass
    
    # Send message to Telegram and Twitter
    @staticmethod
    def send_telegram_message(message:str) -> None:
        """
        Send a message to the Telegram channel
        """
        pass

    @staticmethod
    def send_twitter_message(message:str) -> None:
        """
        Send a message to the Twitter channel
        """
        pass