from ..amazon.amazon import AmazonScraper
from ..flipkart.flipkart import FlipkartScraper
from ..myntra.myntra import MyntraScraper

from ...db.redis import RedisDB
from ..utils.web_driver_utility import WebDriverUtility
from ...lib.types import Websites, ProductCategories
from ...utils.best_discount_analyzer import BestDiscountAnalyzer


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
            return AmazonScraper(category, driver_utility, redis_client, discount_analyzer, Websites.AMAZON)
        elif website == Websites.FLIPKART:
            return FlipkartScraper(category, driver_utility, redis_client, discount_analyzer, Websites.FLIPKART)
        elif website == Websites.MYNTRA:
            return MyntraScraper(category, driver_utility, redis_client, discount_analyzer, Websites.MYNTRA)
        else:
            raise ValueError(f"Unsupported website: {website}")
