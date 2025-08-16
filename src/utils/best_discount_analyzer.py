import numpy as np
import math

from ..lib.types import Product


class BestDiscountAnalyzer:
    """
    Optimized discount analyzer using mathematical optimization
    and weighted scoring for accurate predictions
    """

    def __init__(self,
                 discount_weight: float = 0.4,
                 rating_weight: float = 0.3,
                 popularity_weight: float = 0.2,
                 price_range_weight: float = 0.1):
        """
        Initialize with configurable weights for different factors

        Args:
            discount_weight: Weight for discount percentage (0-1)
            rating_weight: Weight for product rating (0-1)  
            popularity_weight: Weight for rating count/popularity (0-1)
            price_range_weight: Weight for price range consideration (0-1)
        """
        # Normalize weights to ensure they sum to 1
        total = discount_weight + rating_weight + \
            popularity_weight + price_range_weight
        self.weights = np.array([
            discount_weight / total,
            rating_weight / total,
            popularity_weight / total,
            price_range_weight / total
        ])

        # Pre-computed constants for speed
        self.ln_10 = math.log(10)
        self.rating_normalizer = 1.0 / 4.0  # For (rating - 1) / 4
        self.discount_normalizer = 1.0 / 80.0  # For discount / 80

        # Cache for expensive calculations
        self._price_cache = {}
        self._popularity_cache = {}

    def _calculate_discount_percentage(self, actual_price: float, discount_price: float) -> float:
        """Fast discount percentage calculation with validation"""
        # Early return for invalid inputs
        if actual_price <= 0 or discount_price < 0 or discount_price >= actual_price:
            return 0.0

        return ((actual_price - discount_price) / actual_price) * 100

    def _calculate_popularity_score(self, rating_count: int) -> float:
        """Cached logarithmic popularity score for better scaling"""
        if rating_count <= 0:
            return 0.0

        # Use cache for repeated calculations
        if rating_count in self._popularity_cache:
            return self._popularity_cache[rating_count]

        # Use logarithmic scaling for rating count (diminishing returns)
        score = min(1.0, math.log(rating_count + 1) / self.ln_10)

        # Cache the result (limit cache size to prevent memory issues)
        if len(self._popularity_cache) < 1000:
            self._popularity_cache[rating_count] = score

        return score

    def _calculate_price_attractiveness(self, actual_price: float) -> float:
        """Cached price range attractiveness score"""
        if actual_price <= 0:
            return 0.0

        # Round price for better caching
        price_key = round(actual_price, 2)
        if price_key in self._price_cache:
            return self._price_cache[price_key]

        # Sweet spot pricing (products in mid-range often have better value)
        log_price = math.log(actual_price + 1)

        # Optimized scoring with fewer conditionals
        if log_price <= 4:  # ~$50
            score = log_price * 0.25  # log_price / 4
        elif log_price <= 5.3:  # ~$200
            score = 1.0
        else:
            score = max(0.1, 1.0 - (log_price - 5.3) / 3)

        # Cache the result
        if len(self._price_cache) < 1000:
            self._price_cache[price_key] = score

        return score

    def is_best_discount(self, product: Product,
                         min_discount_threshold: float = 15.0,
                         min_rating_threshold: float = 3.5,
                         min_rating_count: int = 5) -> bool:
        """
        Ultra-fast best discount prediction using weighted scoring

        Args:
            product: Product object with price and rating data
            min_discount_threshold: Minimum discount % to consider
            min_rating_threshold: Minimum rating to consider
            min_rating_count: Minimum number of ratings to consider

        Returns:
            bool: True if product has best discount, False otherwise
        """

        # Quick elimination checks for speed
        discount_pct = self._calculate_discount_percentage(
            product.get("price", 0), product.get("discount_price", 0))

        # Fast early elimination
        if (discount_pct < min_discount_threshold or
            product.get("rating", 0) < min_rating_threshold or
                product.get("rating_count", 0) < min_rating_count):
            return False

        # Calculate weighted score using optimized operations
        discount_score = min(1.0, discount_pct * self.discount_normalizer)
        rating_score = (product.get("rating", 0) - 1.0) * \
            self.rating_normalizer
        popularity_score = self._calculate_popularity_score(
            product.get("rating_count", 0))
        price_score = self._calculate_price_attractiveness(
            product.get("price", 0))

        # Vectorized final score calculation
        scores = np.array([discount_score, rating_score,
                          popularity_score, price_score])
        final_score = np.dot(scores, self.weights)

        # Optimized threshold selection
        if discount_pct >= 50:
            return final_score >= 0.6
        elif discount_pct >= 30:
            return final_score >= 0.7
        else:
            return final_score >= 0.75

    def clear_cache(self):
        """Clear internal caches to free memory"""
        self._price_cache.clear()
        self._popularity_cache.clear()
