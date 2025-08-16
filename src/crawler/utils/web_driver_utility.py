from time import sleep
from typing import List
from logging import error, warning
from random import choice, uniform
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException


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
        chrome_options.add_argument('--memory-pressure-off')

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
            sleep(uniform(1, 3.5))

    def find_element_with_wait(self, selectors: List[str], timeout: int = 5) -> WebElement | None:
        """
        Find an element using CSS selectors with timeout wait.

        Args:
            selectors (List[str]): List of CSS selectors to find the element.
            type (Literal["single", "multiple"]): Whether to find single or multiple elements.
            timeout (int): The maximum time to wait in seconds.

        Returns:
            WebElement | List[WebElement] | None: The found element(s) or None if not found.
        """
        def any_element_present(driver):
            all_selectors = ", ".join(selectors)
            element = None

            try:
                element = driver.find_element(
                    By.CSS_SELECTOR, all_selectors)

                return element if element is not None else None
            except Exception:
                return None

        return self._webdriver_wait(any_element_present, timeout)

    def find_element_from_parent(self, parent: WebElement | WebDriver, selectors: List[str]) -> WebElement | None:
        """
        Find an element directly from a parent element without wait.

        Args:
            parent (WebElement): The parent element to search within.
            selectors (List[str]): List of CSS selectors to find the element.
            type (Literal["single", "multiple"]): Whether to find single or multiple elements.

        Returns:
            WebElement | List[WebElement] | None: The found element(s) or None if not found.
        """
        all_selectors = ", ".join(selectors)

        try:
            elem = parent.find_element(By.CSS_SELECTOR, all_selectors)

            if elem is not None:
                return elem
        except Exception:
            return None

    def find_elements_from_parent(self, parent: WebElement | WebDriver, selectors: List[str]) -> List[WebElement] | None:
        """
        Find an elements directly from a parent element without wait.

        Args:
            parent (WebElement): The parent element to search within.
            selectors (List[str]): List of CSS selectors to find the element.
            type (Literal["single", "multiple"]): Whether to find single or multiple elements.

        Returns:
            WebElement | List[WebElement] | None: The found element(s) or None if not found.
        """
        all_selectors = ", ".join(selectors)

        try:
            return parent.find_elements(By.CSS_SELECTOR, all_selectors)
        except Exception:
            return None

    def _webdriver_wait(self, callback, timeout: int = 10):
        """
        Wait for a specific condition to be met.

        Args:
            callback (function): The condition to wait for.
            timeout (int): The maximum time to wait in seconds.

        Returns:
            any: The result of the callback function if successful, None otherwise.
        """
        if self.driver is None:
            return

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
