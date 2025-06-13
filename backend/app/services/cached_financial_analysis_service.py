"""
Cached Financial Analysis Service

Enhanced version of FinancialAnalysisService with Redis caching
for improved performance and reduced API calls.
"""

import logging
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.financial_analysis_service import FinancialAnalysisService
from app.core.redis_client import get_redis
from app.core.security_middleware import audit_logger

logger = logging.getLogger(__name__)


class CachedFinancialAnalysisService(FinancialAnalysisService):
    """
    Enhanced Financial Analysis Service with Redis caching
    """

    def __init__(self):
        """Initialize the cached financial analysis service"""
        super().__init__()
        self.redis = get_redis()

        # Cache expiration times (in seconds)
        self.cache_expiry = {
            "lead_analysis": 3600,  # 1 hour - financial analysis
            "market_trends": 21600,  # 6 hours - market trends change slowly
            "broker_matches": 86400,  # 24 hours - broker matches
            "effi_leads": 1800,  # 30 minutes - lead data
            "ai_insights": 7200,  # 2 hours - AI insights
        }

    def _generate_cache_key(self, prefix: str, data: Any) -> str:
        """Generate a consistent cache key from data"""
        if isinstance(data, dict):
            # Sort dict keys for consistent hashing
            sorted_data = str(sorted(data.items()))
        else:
            sorted_data = str(data)

        data_hash = hashlib.md5(sorted_data.encode()).hexdigest()[:16]
        return f"{prefix}:{data_hash}"

    async def analyze_lead_financial_profile(
        self, lead_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze lead with caching
        """
        # Generate cache key
        cache_key = self._generate_cache_key("lead_analysis", lead_data)

        # Try to get from cache
        cached_result = self.redis.cache_get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for lead analysis: {cache_key}")
            # Track cache hit
            self.redis.track_event("cache_hit_lead_analysis")
            return cached_result

        logger.info(f"Cache MISS for lead analysis: {cache_key}")

        # Generate new analysis
        analysis = await super().analyze_lead_financial_profile(lead_data)

        # Cache the result if successful
        if "error" not in analysis:
            self.redis.cache_set(
                cache_key, analysis, self.cache_expiry["lead_analysis"]
            )
            logger.info(f"Cached lead analysis: {cache_key}")

        # Track cache miss
        self.redis.track_event("cache_miss_lead_analysis")

        return analysis

    async def analyze_market_trends(
        self, location: str = None, days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze market trends with caching
        """
        # Generate cache key
        cache_data = {"location": location, "days_back": days_back}
        cache_key = self._generate_cache_key("market_trends", cache_data)

        # Try to get from cache
        cached_result = self.redis.cache_get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for market trends: {cache_key}")
            self.redis.track_event("cache_hit_market_trends")
            return cached_result

        logger.info(f"Cache MISS for market trends: {cache_key}")

        # Generate new analysis
        trends = await super().analyze_market_trends(location, days_back)

        # Cache the result if successful
        if "error" not in trends:
            self.redis.cache_set(cache_key, trends, self.cache_expiry["market_trends"])
            logger.info(f"Cached market trends: {cache_key}")

        self.redis.track_event("cache_miss_market_trends")

        return trends

    async def enhance_broker_matching(
        self, user_id: str, db: Session
    ) -> Dict[str, Any]:
        """
        Enhanced broker matching with caching
        """
        # Generate cache key
        cache_key = f"enhanced_matches:{user_id}"

        # Try to get from cache
        cached_result = self.redis.cache_get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for enhanced matching: {cache_key}")
            self.redis.track_event("cache_hit_enhanced_matching")
            return cached_result

        logger.info(f"Cache MISS for enhanced matching: {cache_key}")

        # Generate new matches
        enhanced_matches = await super().enhance_broker_matching(user_id, db)

        # Cache the result if successful
        if "error" not in enhanced_matches:
            self.redis.cache_set(
                cache_key, enhanced_matches, self.cache_expiry["broker_matches"]
            )
            logger.info(f"Cached enhanced matches: {cache_key}")

        self.redis.track_event("cache_miss_enhanced_matching")

        return enhanced_matches

    def get_cached_effi_leads(
        self, search_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached Effi leads search results
        """
        cache_key = self._generate_cache_key("effi_leads", search_params)

        cached_result = self.redis.cache_get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for Effi leads: {cache_key}")
            self.redis.track_event("cache_hit_effi_leads")
            return cached_result

        return None

    def cache_effi_leads(
        self, search_params: Dict[str, Any], leads_data: Dict[str, Any]
    ):
        """
        Cache Effi leads search results
        """
        cache_key = self._generate_cache_key("effi_leads", search_params)
        self.redis.cache_set(cache_key, leads_data, self.cache_expiry["effi_leads"])
        logger.info(f"Cached Effi leads: {cache_key}")

    async def get_cached_ai_insights(
        self, financial_indicators: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached AI insights
        """
        cache_key = self._generate_cache_key("ai_insights", financial_indicators)

        cached_result = self.redis.cache_get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for AI insights: {cache_key}")
            self.redis.track_event("cache_hit_ai_insights")
            return cached_result

        return None

    async def cache_ai_insights(
        self, financial_indicators: Dict[str, Any], insights: Dict[str, Any]
    ):
        """
        Cache AI insights
        """
        cache_key = self._generate_cache_key("ai_insights", financial_indicators)
        self.redis.cache_set(cache_key, insights, self.cache_expiry["ai_insights"])
        logger.info(f"Cached AI insights: {cache_key}")

    async def _generate_financial_insights(
        self, financial_indicators: Dict[str, Any], lead_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Override to add caching for AI insights
        """
        # Check cache first
        cached_insights = await self.get_cached_ai_insights(financial_indicators)
        if cached_insights:
            return cached_insights

        # Generate new insights
        insights = await super()._generate_financial_insights(
            financial_indicators, lead_data
        )

        # Cache the result
        if insights and "error" not in insights:
            await self.cache_ai_insights(financial_indicators, insights)

        return insights

    def invalidate_cache(self, cache_type: str, identifier: str = None):
        """
        Invalidate specific cache entries

        Args:
            cache_type: Type of cache to invalidate
            identifier: Specific identifier (e.g., user_id)
        """
        try:
            if cache_type == "user_matches" and identifier:
                # Invalidate user's broker matches
                cache_key = f"enhanced_matches:{identifier}"
                self.redis.cache_delete(cache_key)
                logger.info(f"Invalidated cache for user matches: {identifier}")

            elif cache_type == "market_trends":
                # This would require pattern matching - simplified for now
                logger.info("Market trends cache invalidation requested")

            elif cache_type == "all":
                # This would clear all cache - use with caution
                logger.warning("Full cache invalidation requested")

            # Track cache invalidation
            self.redis.track_event("cache_invalidation", metadata={"type": cache_type})

        except Exception as e:
            logger.error(f"Cache invalidation failed: {str(e)}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics
        """
        try:
            # Get analytics for cache events
            cache_hits = self.redis.get_analytics("cache_hit_lead_analysis", days=7)
            cache_misses = self.redis.get_analytics("cache_miss_lead_analysis", days=7)

            # Calculate hit rate
            total_hits = sum(day["count"] for day in cache_hits.get("daily", []))
            total_misses = sum(day["count"] for day in cache_misses.get("daily", []))
            total_requests = total_hits + total_misses

            hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0

            return {
                "hit_rate_percentage": round(hit_rate, 2),
                "total_hits": total_hits,
                "total_misses": total_misses,
                "total_requests": total_requests,
                "redis_health": self.redis.health_check(),
                "cache_types": {
                    "lead_analysis": {"expiry": self.cache_expiry["lead_analysis"]},
                    "market_trends": {"expiry": self.cache_expiry["market_trends"]},
                    "broker_matches": {"expiry": self.cache_expiry["broker_matches"]},
                    "ai_insights": {"expiry": self.cache_expiry["ai_insights"]},
                },
            }

        except Exception as e:
            logger.error(f"Failed to get cache stats: {str(e)}")
            return {"error": str(e)}

    async def warm_cache_for_user(self, user_id: str, db: Session):
        """
        Pre-populate cache for a user (useful after quiz completion)
        """
        try:
            logger.info(f"Warming cache for user: {user_id}")

            # Pre-generate enhanced matches
            await self.enhance_broker_matching(user_id, db)

            # Track cache warming
            self.redis.track_event("cache_warming", user_id)

            logger.info(f"Cache warming completed for user: {user_id}")

        except Exception as e:
            logger.error(f"Cache warming failed for user {user_id}: {str(e)}")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the service
        """
        try:
            # Get various analytics
            analytics = {}

            events = [
                "financial_analysis_request",
                "cache_hit_lead_analysis",
                "cache_miss_lead_analysis",
                "cache_hit_market_trends",
                "cache_miss_market_trends",
            ]

            for event in events:
                analytics[event] = self.redis.get_analytics(event, days=7)

            return {
                "analytics": analytics,
                "cache_stats": self.get_cache_stats(),
                "redis_health": self.redis.health_check(),
            }

        except Exception as e:
            logger.error(f"Failed to get performance metrics: {str(e)}")
            return {"error": str(e)}


# Enhanced service with security logging
class SecureFinancialAnalysisService(CachedFinancialAnalysisService):
    """
    Financial Analysis Service with security features
    """

    async def analyze_lead_financial_profile(
        self, lead_data: Dict[str, Any], user_id: str = None, ip: str = None
    ) -> Dict[str, Any]:
        """
        Analyze lead with security logging
        """
        # Log financial data access
        if user_id and ip:
            audit_logger.log_financial_access(
                user_id=user_id,
                action="analyze_lead",
                resource=f"lead:{lead_data.get('Id', 'unknown')}",
                ip=ip,
            )

        # Perform analysis
        result = await super().analyze_lead_financial_profile(lead_data)

        # Track successful analysis
        if "error" not in result:
            self.redis.track_event("successful_lead_analysis", user_id)
        else:
            self.redis.track_event("failed_lead_analysis", user_id)

        return result

    async def analyze_market_trends(
        self,
        location: str = None,
        days_back: int = 30,
        user_id: str = None,
        ip: str = None,
    ) -> Dict[str, Any]:
        """
        Analyze market trends with security logging
        """
        # Log market data access
        if user_id and ip:
            audit_logger.log_financial_access(
                user_id=user_id,
                action="analyze_market_trends",
                resource=f"market:{location or 'all'}",
                ip=ip,
            )

        # Perform analysis
        result = await super().analyze_market_trends(location, days_back)

        # Track analysis
        if "error" not in result:
            self.redis.track_event("successful_market_analysis", user_id)
        else:
            self.redis.track_event("failed_market_analysis", user_id)

        return result


# Global instances
cached_financial_service = CachedFinancialAnalysisService()
secure_financial_service = SecureFinancialAnalysisService()


# Convenience functions
async def get_cached_lead_analysis(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Get cached lead analysis"""
    return await cached_financial_service.analyze_lead_financial_profile(lead_data)


async def get_cached_market_trends(
    location: str = None, days_back: int = 30
) -> Dict[str, Any]:
    """Get cached market trends"""
    return await cached_financial_service.analyze_market_trends(location, days_back)


def get_cache_performance() -> Dict[str, Any]:
    """Get cache performance metrics"""
    return cached_financial_service.get_performance_metrics()
