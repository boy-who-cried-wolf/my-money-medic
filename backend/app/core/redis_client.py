"""
Redis Client Service

Provides Redis connection management and common operations
for caching, session storage, and rate limiting.
"""

import redis
import json
import logging
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import os
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client with connection management and common operations"""

    def __init__(self):
        """Initialize Redis client"""
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.redis_db = int(os.getenv("REDIS_DB", "0"))
        self.redis_password = os.getenv("REDIS_PASSWORD")

        self._client = None
        self._connect()

    def _connect(self):
        """Establish Redis connection"""
        try:
            if self.redis_url.startswith("redis://"):
                # Use URL connection (for cloud Redis)
                self._client = redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True,
                )
            else:
                # Use host/port connection (for local Redis)
                self._client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    db=self.redis_db,
                    password=self.redis_password,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True,
                )

            # Test connection
            self._client.ping()
            logger.info("Redis connection established successfully")

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            self._client = None

    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self._client:
            return False
        try:
            self._client.ping()
            return True
        except:
            return False

    def reconnect(self):
        """Reconnect to Redis"""
        self._connect()

    # Basic Operations
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set a key-value pair with optional expiration"""
        try:
            if not self.is_connected():
                return False

            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            if expire:
                return self._client.setex(key, expire, value)
            else:
                return self._client.set(key, value)
        except Exception as e:
            logger.error(f"Redis SET error: {str(e)}")
            return False

    def get(self, key: str, parse_json: bool = True) -> Any:
        """Get value by key"""
        try:
            if not self.is_connected():
                return None

            value = self._client.get(key)
            if value is None:
                return None

            if parse_json:
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return value
        except Exception as e:
            logger.error(f"Redis GET error: {str(e)}")
            return None

    def delete(self, key: str) -> bool:
        """Delete a key"""
        try:
            if not self.is_connected():
                return False
            return bool(self._client.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            if not self.is_connected():
                return False
            return bool(self._client.exists(key))
        except Exception as e:
            logger.error(f"Redis EXISTS error: {str(e)}")
            return False

    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a key"""
        try:
            if not self.is_connected():
                return None
            return self._client.incr(key, amount)
        except Exception as e:
            logger.error(f"Redis INCR error: {str(e)}")
            return None

    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration for a key"""
        try:
            if not self.is_connected():
                return False
            return self._client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis EXPIRE error: {str(e)}")
            return False

    def ttl(self, key: str) -> int:
        """Get time to live for a key"""
        try:
            if not self.is_connected():
                return -1
            return self._client.ttl(key)
        except Exception as e:
            logger.error(f"Redis TTL error: {str(e)}")
            return -1

    # Cache Operations
    def cache_set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Cache a value with default 1-hour expiration"""
        return self.set(f"cache:{key}", value, expire)

    def cache_get(self, key: str) -> Any:
        """Get cached value"""
        return self.get(f"cache:{key}")

    def cache_delete(self, key: str) -> bool:
        """Delete cached value"""
        return self.delete(f"cache:{key}")

    # Session Operations
    def session_set(
        self, session_id: str, data: Dict[str, Any], expire: int = 86400
    ) -> bool:
        """Set session data with default 24-hour expiration"""
        return self.set(f"session:{session_id}", data, expire)

    def session_get(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        return self.get(f"session:{session_id}")

    def session_delete(self, session_id: str) -> bool:
        """Delete session"""
        return self.delete(f"session:{session_id}")

    def session_refresh(self, session_id: str, expire: int = 86400) -> bool:
        """Refresh session expiration"""
        return self.expire(f"session:{session_id}", expire)

    # Rate Limiting Operations
    def rate_limit_check(
        self, identifier: str, limit: int, window: int
    ) -> Dict[str, Any]:
        """
        Check rate limit for an identifier

        Args:
            identifier: Unique identifier (user_id, IP, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds

        Returns:
            Dict with allowed, remaining, reset_time
        """
        try:
            if not self.is_connected():
                return {"allowed": True, "remaining": limit, "reset_time": 0}

            key = f"rate_limit:{identifier}"
            current = self._client.get(key)

            if current is None:
                # First request
                self._client.setex(key, window, 1)
                return {
                    "allowed": True,
                    "remaining": limit - 1,
                    "reset_time": int(datetime.now().timestamp()) + window,
                }

            current_count = int(current)
            if current_count < limit:
                # Within limit
                self._client.incr(key)
                remaining = limit - current_count - 1
                reset_time = int(datetime.now().timestamp()) + self.ttl(key)
                return {
                    "allowed": True,
                    "remaining": remaining,
                    "reset_time": reset_time,
                }
            else:
                # Rate limit exceeded
                reset_time = int(datetime.now().timestamp()) + self.ttl(key)
                return {"allowed": False, "remaining": 0, "reset_time": reset_time}

        except Exception as e:
            logger.error(f"Rate limit check error: {str(e)}")
            # Fail open - allow request if Redis is down
            return {"allowed": True, "remaining": limit, "reset_time": 0}

    # Analytics Operations
    def track_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        """Track an event for analytics"""
        try:
            if not self.is_connected():
                return

            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            hour = now.strftime("%Y-%m-%d:%H")

            # Daily counters
            self.incr(f"events:{event_type}:{today}")
            self.incr(f"events:total:{today}")

            # Hourly counters
            self.incr(f"events:{event_type}:{hour}")
            self.expire(f"events:{event_type}:{hour}", 86400 * 7)  # Keep for 7 days

            # User-specific tracking
            if user_id:
                self.incr(f"user_events:{user_id}:{today}")
                self.expire(
                    f"user_events:{user_id}:{today}", 86400 * 30
                )  # Keep for 30 days

            # Live metrics (5-minute windows)
            live_key = f"live:{event_type}:{now.strftime('%Y-%m-%d:%H:%M')[:-1]}0"  # Round to 10-minute
            self.incr(live_key)
            self.expire(live_key, 600)  # 10-minute window

        except Exception as e:
            logger.error(f"Event tracking error: {str(e)}")

    def get_analytics(self, event_type: str, days: int = 7) -> Dict[str, Any]:
        """Get analytics for an event type"""
        try:
            if not self.is_connected():
                return {}

            analytics = {}

            # Daily data for the last N days
            daily_data = []
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                count = self.get(f"events:{event_type}:{date}", parse_json=False) or 0
                daily_data.append({"date": date, "count": int(count)})

            analytics["daily"] = list(reversed(daily_data))

            # Today's hourly data
            today = datetime.now().strftime("%Y-%m-%d")
            hourly_data = []
            for hour in range(24):
                hour_key = f"{today}:{hour:02d}"
                count = (
                    self.get(f"events:{event_type}:{hour_key}", parse_json=False) or 0
                )
                hourly_data.append({"hour": hour, "count": int(count)})

            analytics["hourly"] = hourly_data

            return analytics

        except Exception as e:
            logger.error(f"Analytics retrieval error: {str(e)}")
            return {}

    # Health Check
    def health_check(self) -> Dict[str, Any]:
        """Redis health check"""
        try:
            if not self._client:
                return {"status": "disconnected", "error": "No Redis client"}

            start_time = datetime.now()
            self._client.ping()
            response_time = (datetime.now() - start_time).total_seconds() * 1000

            info = self._client.info()

            return {
                "status": "connected",
                "response_time_ms": round(response_time, 2),
                "memory_usage": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "uptime_seconds": info.get("uptime_in_seconds", 0),
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}


# Global Redis client instance
redis_client = RedisClient()


# Convenience functions
def get_redis() -> RedisClient:
    """Get Redis client instance"""
    return redis_client


def cache_result(key: str, expire: int = 3600):
    """Decorator for caching function results"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Try to get from cache
            cached = redis_client.cache_get(key)
            if cached is not None:
                return cached

            # Execute function and cache result
            result = await func(*args, **kwargs)
            redis_client.cache_set(key, result, expire)
            return result

        return wrapper

    return decorator
