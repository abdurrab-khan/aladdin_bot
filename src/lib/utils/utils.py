from typing import List, Optional
from src.lib.types import Product

class Utils:
    # Utility functions
    @staticmethod
    def get_products_from_web(url:str, category:str) -> str | None:
        """
        Get products from a given URL and return a list of Product objects 
        """
        pass

    @staticmethod
    def parse_html(html: Optional[str] = None) -> Product | None:
        """
        Parse the HTML content with checking all fields are present or not and return a list of Product objects
        """
        pass

    @staticmethod
    def filter_products(products: Optional[Product], min_price:float, max_price:float) -> Product | None:
        """
        Filter the products based on the price range and return a list of Product objects
        """
        pass

    @staticmethod
    def evaluate_products_with_ml(product: Optional[Product] = None) -> Product | None:
        """
        Check the products based on the actual price, discount, rating using random forest regressor and return a list of Product objects
        """
        pass

    @staticmethod
    def sort_products(product: Optional[List[Product]] = None) -> List[Product] | None:
        """
        Sort the products based on the discount price
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