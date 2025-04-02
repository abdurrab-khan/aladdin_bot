from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .helper_functions import HelperFunctions
from ..lib import ProductSearchResult, Websites


class SeleniumHelper:
    def __init__(self):
        """
        Initialize the WebDriver with Chrome options and navigate to the URL
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the WebDriver
        self.driver = Chrome(options=chrome_options)

    def get_products(self, url: str, website_name: Websites) -> ProductSearchResult | None:
        try:
            self.driver.get(url)
            sleep(2)
            html = self.driver.page_source

            if html is None:
                raise ("HTML is not found something goes wrong.")

            soup = BeautifulSoup(html, "html.parse")

            return self.extract_products_by_website(soup, website_name)
        except Exception as e:
            return None
        finally:
            self.driver.quit()

    def extract_products_by_website(self, soup: BeautifulSoup, website_name: Websites) -> ProductSearchResult | None:
        """
        Get products from a given URL and return a list of Product objects 
        """
        match website_name:
            case Websites.AMAZON:
                # Implementation for Amazon
                return []
            case Websites.FLIPKART:
                # Implementation for Flipkart
                return []
            case Websites.MYNTRA:
                # Implementation for Myntra
                return []
            case Websites.AJIO:
                # Implementation for Ajio
                return []
            case _:
                return None
