from re import search
from time import sleep
from bs4 import BeautifulSoup, Tag
from logging import info, error, warning
from urllib.parse import unquote
from random import choice, uniform
from selenium.webdriver import Chrome
from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ..utils.best_discount_analyzer import BestDiscountAnalyzer

from ..constants.const import ASSOCIATED_APP, USER_ID
from ..constants.url import PLATFORM_IDS

from ..db.redis import RedisDB
from .helper_functions import HelperFunctions, retry
from ..lib.types import Websites, ProductCategories, ProductKey, Product
from ..constants.css_selectors import NEXT_BUTTON, PRODUCT_CONTAINER, PRODUCT_DETAILS, PRODUCT_CARDS
from ..constants.product import PRICE_LIMITS, MAX_PRODUCTS_PER_WEBSITE


class WebDriverUtility:
    """
        Handles the initialization and basic operations of the WebDriver.
        This class is responsible for browser-specific operations.
    """

    def __init__(self):
        """Initialize the WebDriver with Chrome options"""
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Set up the Chrome WebDriver with appropriate options"""

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"
        ]
        chrome_options.add_argument(f"user-agent={choice(user_agents)}")

        self.driver = Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)

    def navigate_to(self, url: str):
        """Navigate to the specified URL"""
        if self.driver:
            self.driver.get(url)

    def safe_find_element(self, selectors: List[str] | str, timeout: int = 5) -> Optional[List[WebElement]]:
        """
        Safely find an element using a selector.

        Args:
            selector (str): The CSS selector to find the element.
            timeout (int): The maximum time to wait in seconds.

        Returns:
            WebElement | None: The found element or None if not found.
        """
        def any_element_present(driver):
            list_selectors = selectors if isinstance(
                selectors, list) else [selectors]

            for selector in list_selectors:
                element = driver.find_elements(
                    By.CSS_SELECTOR, selector)

                if element:
                    return element

                return None

        return self._webdriver_wait(any_element_present, timeout)

    def _webdriver_wait(self, callback, timeout: int = 10):
        """
        Wait for a specific condition to be met.

        Args:
            callback (function): The condition to wait for.
            timeout (int): The maximum time to wait in seconds.

        Returns:
            any: The result of the callback function if successful, None otherwise.
        """
        try:
            return WebDriverWait(self.driver, timeout).until(callback)
        except TimeoutException:
            error("⌛ Timeout waiting for condition to be met")
            return None

    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
        else:
            warning("⚠️ Driver is already closed or not initialized")


class DataProcessingHelper:
    """
    Handles data processing, formatting, and validation operations.
    This class contains helper methods for processing scraped data.
    """

    @staticmethod
    def get_product_details(soup: Tag, website_name: Websites, category: ProductCategories) -> Optional[Product]:
        """
        Extract product details from the BeautifulSoup object.

        Args:
            soup (Tag): The BeautifulSoup object containing product data.
            website_name (Website): Name of the website
            category (ProductCategories): Category of the product

        Returns:
            Optional[Product]: A dictionary containing product details.
        """
        product_details: Product = {}

        for key, selectors in PRODUCT_DETAILS[website_name].items():
            try:
                element = soup.select_one(", ".join(selectors))
                formatted_data = DataProcessingHelper.format_extracted_data(
                    key, element, website_name)

                if formatted_data is None and not (website_name == Websites.FLIPKART and key == "product_url"):
                    return None

                product_details[key] = formatted_data
            except Exception as e:
                error(f"Error extracting {key}: {str(e)}")
                return None

        if product_details:
            product_details["user_id"] = USER_ID
            product_details["platform_id"] = PLATFORM_IDS[website_name.value]
            product_details["category"] = category.value
            product_details["associated_app"] = ASSOCIATED_APP

        return product_details

    @staticmethod
    def format_extracted_data(key: ProductKey, element_data: Tag | None, website_name: Websites):
        """
        Format the extracted data based on the selector type.

        Args:
            key (ProductKey): The type of data to format.
            element_data (BeautifulSoup | None): The extracted data to format.

        Returns:
            Union[float, int, str, None]: The formatted data.
        """
        if element_data is None:
            return None

        if key == "product_image" or key == "product_url":
            attr = "href" if key == "product_url" else "src"
            element = element_data[attr]

            if element is None:
                return None

            return element if key == "product_image" else DataProcessingHelper.url_shorter(str(element), website_name)
        else:
            element = element_data.get_text(strip=True)

        # Format the give data by website_name
        if key == "price" or key == "discount_price":
            return HelperFunctions.format_price(element, website_name)

        elif key == "rating":
            return HelperFunctions.format_rating(element, website_name)

        elif key == "rating_count":
            return HelperFunctions.format_rating_count(element, website_name)

        return element

    @staticmethod
    def is_product_valid(url: str | None, discount_price: float | None, price_limit: int, rating_count: int | None, redis: RedisDB) -> bool:
        """
        Validate if a product has the necessary information.

        Args:
            price (BeautifulSoup): The price element.
            url (BeautifulSoup): The URL element.

        Returns:
            bool: True if the product is valid, False otherwise.
        """
        if url is None or discount_price is None:
            return False

        if rating_count is not None and rating_count >= 10:
            return False

        if discount_price < price_limit:
            if redis.is_url_cached(url):
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def url_shorter(url: str, website_name: Websites) -> str | None:
        """
        Generate a short URL with the affiliate code based on the website.

        Args:
            url (str): The original URL to shorten.

        Returns:
            str: The short URL with the affiliate code.
        """
        # URL shortening and affiliate code addition logic
        formatted_url = None

        if website_name == Websites.AMAZON:
            product_id = DataProcessingHelper.extract_amazon_product_id(url)
            formatted_url = f"https://www.amazon.in/dp/{product_id}" if product_id is not None else None

        elif website_name == Websites.FLIPKART:
            formatted_url = f"https://www.flipkart.com{url.split('?')[0]}"

        elif website_name == Websites.MYNTRA:
            formatted_url = f"https://www.myntra.com/{url}"

        return unquote(formatted_url, encoding="utf-8") if formatted_url is not None else formatted_url

    @staticmethod
    def extract_amazon_product_id(url) -> str | None:
        """
        Extract the product id of Amazon from product url.
        Args:
            url (str): The original URL.

        Returns:
            str: The product id
        """
        decoded_url = unquote(url)
        pattern = r'/dp/([a-zA-Z0-9]{10})'

        match = search(pattern, decoded_url)

        if match:
            return match.group(1)
        else:
            return None


class WebsiteScraperFactory:
    """
     Factory class to create website-specific scrapers based on the website name.
    """

    @staticmethod
    def get_scraper(website: Websites, category: ProductCategories, driver_utility: WebDriverUtility, redis_client: RedisDB, discount_analyzer: BestDiscountAnalyzer):
        """
        Get the appropriate scraper for the specified website.

        Args:
            website (Websites): The website to scrape.
            driver_utility (WebDriverUtility): The WebDriver utility instance.
            redis_client (RedisDB): The Redis client instance.

        Returns:
            WebsiteScraper: The website-specific scraper.
        """

        if website == Websites.AMAZON:
            return AmazonScraper(category, driver_utility, redis_client, discount_analyzer)
        elif website == Websites.FLIPKART:
            return FlipkartScraper(category, driver_utility, redis_client, discount_analyzer)
        elif website == Websites.MYNTRA:
            return MyntraScraper(category, driver_utility, redis_client, discount_analyzer)
        else:
            raise ValueError(f"Unsupported website: {website}")


class WebsiteScraper:
    """
    Base class for website-specific scrapers.
    """

    def __init__(self, category: ProductCategories, driver_utility: WebDriverUtility, redis_client: RedisDB, discount_analyzer: BestDiscountAnalyzer):
        """
        Initialize the website scraper.

        Args:
            driver_utility (WebDriverUtility): The WebDriver utility instance.
            redis_client (RedisDB): The Redis client instance.
        """
        self.processed_product_urls = set()
        self.category = category
        self.driver_utility = driver_utility
        self.redis_client = redis_client
        self.discount_analyzer = discount_analyzer
        self.data_helper = DataProcessingHelper()

    def get_product_container(self, website_name: Websites, url: str | None = None) -> Tag | None:
        """
        Get the main container element containing product cards.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        if url:
            self.driver_utility.navigate_to(url)

        isLoaded = self._wait_for_page_load(website_name)
        if not isLoaded:
            error(f"⌛ Timeout waiting for {website_name.value} page to load")
            return None

        if self.driver_utility.driver is None:
            error("⛔ WebDriver is not initialized.")
            return None

        html = self.driver_utility.driver.page_source
        if html is None:
            error("⛔ Failed to retrieve HTML page content.")
            return None

        soup = BeautifulSoup(html, 'html.parser')
        main_container = soup.select_one(PRODUCT_CONTAINER[website_name])

        if main_container is None:
            error("⛔ Failed to find the main container for Amazon products.")
            return None

        return main_container

    def extract_products(self, container: Tag, website_name: Websites) -> List[Product] | None:
        """
        Extract products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        products: List[Product] = []
        products_soup = container.select(PRODUCT_CARDS[website_name])

        if not products_soup:
            return None

        for soup in products_soup:
            product_details: Product | None = DataProcessingHelper.get_product_details(
                soup, website_name, self.category)

            if product_details is None:
                continue

            # Checking -- Whether product is valid or not
            # >> Check Whether product is recently sended.
            # >> Product price is more that max price.
            # >> Discount price is more that max discount price.
            # >> Review count should be greater than 10.
            if not DataProcessingHelper.is_product_valid(product_details.get("product_url"), product_details.get("price"), PRICE_LIMITS[self.category], product_details.get("rating_count"), self.redis_client):
                continue

            # Check -- Whether product is valid or not
            # >> Check by using some ml algorithms.
            # >> Check whether already fetched or not.
            if not (self.discount_analyzer.is_best_discount(product_details)) or self.processed_product_urls.__contains__(product_details["product_url"]):
                continue

            products.append(product_details)
            self.processed_product_urls.add(product_details["product_url"])

            info(
                f"✅ Best Deal found! 🛍️  {product_details['name']} | 💰 Price: ₹{product_details['discount_price']} | ⭐ Rating: {product_details['rating']} | {website_name.value}")

        return products

    def has_next_page(self, website_name: Websites) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        try:
            next_page_btn = self.driver_utility.safe_find_element(
                NEXT_BUTTON[website_name])

            if next_page_btn is None:
                return False

            next_page_btn = next_page_btn[0]

            return next_page_btn.is_enabled() and next_page_btn.is_displayed() or next_page_btn.get_attribute("aria_disabled") == "false"
        except NoSuchElementException:
            return False

    def go_to_next_page(self):
        """
        Navigate to the next page of results.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _wait_for_page_load(self, website_name: Websites) -> bool:
        """
        Wait for the page to load completely.
        """
        attempt = 0
        max_retry = 2
        while attempt < max_retry:
            try:
                WebDriverWait(self.driver_utility.driver, 8).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, PRODUCT_CONTAINER[website_name]))
                )
                sleep(uniform(1.5, 3))

                return True
            except TimeoutException:
                attempt += 1
                base_url_before_ref = self.driver_utility.driver.current_url
                self.driver_utility.driver.refresh()

                if base_url_before_ref != self.driver_utility.driver.current_url:
                    return False

                sleep(uniform(1, 3))

        return False


class AmazonScraper(WebsiteScraper):
    """
    Amazon-specific scraper implementation.
    """

    @retry(3)
    def get_product_container(self, url=None) -> Tag | None:
        """
        Get the main container for Amazon products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(Websites.AMAZON, url)

    def extract_products(self, container: Tag) -> List[Product] | None:
        """
        Extract Amazon products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        return super().extract_products(container, Websites.AMAZON)

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return super().has_next_page(Websites.AMAZON)

    def go_to_next_page(self):
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        if self.driver_utility.driver is None or self.driver_utility is None:
            return False

        current_url = self.driver_utility.driver.current_url
        next_button_elements = self.driver_utility.safe_find_element(
            NEXT_BUTTON[Websites.AMAZON])

        if next_button_elements is None or len(next_button_elements) == 0:
            return False

        next_button_elements[0].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url)

        sleep(uniform(1, 3))


class FlipkartScraper(WebsiteScraper):
    """
    Flipkart-specific scraper implementation.
    """

    def get_product_container(self, url=None) -> Tag | None:
        """
        Get the main container for Flipkart products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(Websites.FLIPKART, url)

    def extract_products(self, container: Tag) -> List[Product] | None:
        """
        Extract Flipkart products from the container.

        Args:
            container (Tag): The container element.

        Returns:
            List[Product] | None: List of extracted products.
        """
        products: List[Product] = []
        products_soup = container.select(PRODUCT_CARDS[Websites.FLIPKART])

        for soup in products_soup:
            url = soup.select_one(
                " ,".join(PRODUCT_DETAILS[Websites.FLIPKART]["product_url"]))
            price = DataProcessingHelper.format_extracted_data(
                "price",
                soup.select_one(
                    " ,".join(PRODUCT_DETAILS[Websites.FLIPKART]["price"])),
                Websites.FLIPKART
            )
            formatted_url = DataProcessingHelper.format_extracted_data(
                "product_url", url, Websites.FLIPKART)

            # Checking --- Whether Product is Valid or None
            if not DataProcessingHelper.is_product_valid(str(formatted_url), price, PRICE_LIMITS[self.category], None, self.redis_client):
                continue

            # Check --- Whether give product is already there
            if self.processed_product_urls.__contains__(formatted_url):
                continue

            url_href = str(url.get("href")) if url is not None else None

            product_details: Product | None = self.__get_product_details(
                url_href)

            # Checking -- Whether product is None
            if product_details is None:
                continue

            products.append(product_details)
            self.processed_product_urls.add(product_details["product_url"])

            info(
                f"✅ Best Deal found! 🛍️  {product_details['name']} | 💰 Price: ₹{product_details['discount_price']} | ⭐ Rating: {product_details['rating']} | flipkart")

        return products

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        try:
            next_page_btn = self.driver_utility.safe_find_element(
                NEXT_BUTTON[Websites.FLIPKART])

            if next_page_btn is None:
                return False

            if len(next_page_btn) == 1:
                if next_page_btn[0].find_element(
                        By.CSS_SELECTOR, "span").get_property("innerHTML") == "Previous":
                    return False

                next_page_btn = next_page_btn[0]
            else:
                next_page_btn = next_page_btn[1]

            return next_page_btn.is_enabled() and next_page_btn.is_displayed() or next_page_btn.get_attribute("aria_disabled") == "false"
        except NoSuchElementException:
            return False

    def go_to_next_page(self):
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        current_url = self.driver_utility.driver.current_url
        next_page_btn = self.driver_utility.safe_find_element(
            NEXT_BUTTON[Websites.FLIPKART])

        if len(next_page_btn) == 1:
            next_page_btn[0].click()
        else:
            next_page_btn[1].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url)

        sleep(uniform(1, 3))

    def __get_product_details(self, url: str | None) -> Optional[Product]:
        """
        Extract product details from the given URL.

        Args:
            url (str): The URL to scrape product details from.

        Returns:
            Product: A dictionary containing product details.
        """
        if url is None:
            return None

        product_url = f"https://www.flipkart.com{url.split('?')[0]}"

        container = self.get_product_container(product_url)

        if container is None:
            return None

        product_details: Product | None = DataProcessingHelper.get_product_details(
            container, Websites.FLIPKART, self.category)

        if product_details is not None:
            if product_details.get("rating_count", None) is None:
                return None

            product_details["product_url"] = product_url

        return product_details


class MyntraScraper(WebsiteScraper):
    """
    Myntra-specific scraper implementation.
    """

    def get_product_container(self, url=None) -> Tag | None:
        """
        Get the main container for Myntra products.

        Args:
            url (str): The URL to scrape products from.

        Returns:
            BeautifulSoup: The main container element.
        """
        return super().get_product_container(Websites.MYNTRA, url)

    def extract_products(self, container: Tag) -> List[Product] | None:
        """
        Extract Myntra products from the container.

        Args:
            container (BeautifulSoup): The container element.

        Returns:
            List[Product]: List of extracted products.
        """
        return super().extract_products(container, Websites.MYNTRA)

    def has_next_page(self) -> bool:
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return super().has_next_page(Websites.MYNTRA)

    def go_to_next_page(self):
        """
        Check if there is a next page available.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        current_url = self.driver_utility.driver.current_url
        old_product = set(self.driver_utility.safe_find_element(
            PRODUCT_CARDS[Websites.MYNTRA]))

        self.driver_utility.safe_find_element(
            NEXT_BUTTON[Websites.MYNTRA])[0].click()

        self.driver_utility._webdriver_wait(
            lambda d: d.current_url != current_url or set(d.find_elements(
                By.CSS_SELECTOR, PRODUCT_CARDS[Websites.MYNTRA])) != old_product)

        sleep(uniform(1, 3))


class SeleniumHelper:
    """
    Main class to coordinate the scraping operations across different websites.
    """

    def __init__(self, redis: RedisDB, discount_analyzer: BestDiscountAnalyzer):
        """
        Initialize the SeleniumHelper with necessary components.

        Args:
            redis (RedisDB): The Redis client instance.
        """
        self.redis_client = redis
        self.discount_analyzer = discount_analyzer
        self.driver_utility = WebDriverUtility()

    def get_product(self, website_name: Websites, category: ProductCategories, url: str) -> List[Product] | None:
        """
        Get products details from a given URL for a specific website and category.

        Args:
            website_name (Websites): The website to scrape from.
            category (ProductCategories): The product category.
            url (str): The URL to scrape products from.

        Returns:
            List[Product] | None: A list of Product objects or None if no products found.
        """
        scraper = WebsiteScraperFactory.get_scraper(
            website_name, category, self.driver_utility, self.redis_client, self.discount_analyzer)

        all_products = []
        page_counter = 1
        empty_page_count = 0

        try:
            while len(all_products) < MAX_PRODUCTS_PER_WEBSITE:
                url: str | None = url if page_counter == 1 else None
                container = scraper.get_product_container(url)

                if container is None:
                    return all_products if all_products else None

                page_products = scraper.extract_products(container)

                # Prevent infinite loop if no products are found
                if page_products is None or len(page_products) == 0:
                    empty_page_count += 1

                    if empty_page_count > 5:
                        warning(
                            f"⚠️ No products found on page {page_counter} for {website_name.value}. Stopping further scraping.")
                        break

                else:
                    if empty_page_count > 0:
                        empty_page_count = 0

                    # Add new product into the list
                    all_products.extend(page_products)

                if len(all_products) > MAX_PRODUCTS_PER_WEBSITE:
                    all_products = all_products[:MAX_PRODUCTS_PER_WEBSITE]
                    break

                if not scraper.has_next_page():
                    break

                go_next_page = scraper.go_to_next_page()

                if go_next_page == False:
                    break

                page_counter += 1
                sleep(1)

            return all_products
        except Exception as e:
            error(f"Error scraping {website_name} products: {str(e)}")
            return all_products if all_products else None

    def close(self):
        """
        Clean up resources.
        """
        self.driver_utility.close_driver()
