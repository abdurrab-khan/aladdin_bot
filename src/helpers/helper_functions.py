from time import sleep
from bs4 import BeautifulSoup
from lib.types import Websites, Product
from ml_model.predict_deal import predict_deal
from typing import Optional, List
from selenium.webdriver import Chrome

# Decorators
def retry(max_retry: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for retry_count in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retry_count < max_retry - 1:
                        sleep(1)
                        continue
                    raise  # Re-raise the last exception
            return None  # This line is actually unreachable
        return wrapper
    return decorator

class HelperFunctions: 
    @staticmethod
    def short_url_with_affiliate_code(url: str) -> str:
        """
        Shorten the URL and add affiliate code to the URL
        """
        # Implementation for URL shortening
        return url

    @staticmethod
    def evaluate_products_with_ml(product: Optional[Product] = None) -> Optional[Product]:
        """
        Check if a product is a good deal using a machine learning model.
        Returns the product if it's a good deal, None otherwise.
        """
        if product is None:
            return None
        
        prediction_result = predict_deal(product)

        if prediction_result['prediction'] == 'Best Deal':
            return product
        
        return None