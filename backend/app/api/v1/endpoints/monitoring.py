"""
Monitoring and Analytics API Endpoints

Provides endpoints for system monitoring, security analytics,
cache performance, and platform health checks.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.core.auth import get_current_user
from app.database.models.user import User, UserType
from app.core.redis_client import get_redis
from app.services.cached_financial_analysis_service import get_cache_performance
from app.core.security_middleware import audit_logger

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)):
    """Require admin role"""
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


@router.get("/health")
async def health_check():
    """
    System health check - available to all users
    """
    try:
        redis_client = get_redis()

        # Check Redis connection
        redis_health = redis_client.health_check()

        # Basic system status
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "api": {"status": "up", "response_time_ms": 0},
                "redis": redis_health,
                "database": {
                    "status": "up"
                },  # Would check DB connection in real implementation
            },
        }

        # Determine overall status
        if redis_health["status"] != "connected":
            health_status["status"] = "degraded"

        return health_status

    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
        }


@router.get("/cache-stats")
async def get_cache_statistics(current_user: User = Depends(require_admin)):
    """
    Get cache performance statistics

    Requires: Admin role
    """
    try:
        cache_stats = get_cache_performance()

        return {
            "success": True,
            "cache_performance": cache_stats,
            "retrieved_by": current_user.id,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving cache statistics: {str(e)}",
        )


@router.get("/analytics")
async def get_platform_analytics(
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    current_user: User = Depends(require_admin),
):
    """
    Get platform usage analytics

    Requires: Admin role
    """
    try:
        redis_client = get_redis()

        # Get analytics for various events
        events_to_analyze = [
            "api_request",
            "financial_analysis_request",
            "quiz_request",
            "auth_request",
            "successful_lead_analysis",
            "failed_lead_analysis",
            "cache_hit_lead_analysis",
            "cache_miss_lead_analysis",
        ]

        analytics = {}
        for event in events_to_analyze:
            analytics[event] = redis_client.get_analytics(event, days=days)

        # Calculate summary metrics
        total_requests = sum(
            day["count"] for day in analytics.get("api_request", {}).get("daily", [])
        )

        financial_requests = sum(
            day["count"]
            for day in analytics.get("financial_analysis_request", {}).get("daily", [])
        )

        cache_hits = sum(
            day["count"]
            for day in analytics.get("cache_hit_lead_analysis", {}).get("daily", [])
        )

        cache_misses = sum(
            day["count"]
            for day in analytics.get("cache_miss_lead_analysis", {}).get("daily", [])
        )

        cache_hit_rate = (
            (cache_hits / (cache_hits + cache_misses) * 100)
            if (cache_hits + cache_misses) > 0
            else 0
        )

        summary = {
            "total_api_requests": total_requests,
            "financial_analysis_requests": financial_requests,
            "cache_hit_rate_percentage": round(cache_hit_rate, 2),
            "analysis_period_days": days,
        }

        return {
            "success": True,
            "summary": summary,
            "detailed_analytics": analytics,
            "retrieved_by": current_user.id,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving analytics: {str(e)}",
        )


@router.get("/security-events")
async def get_security_events(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    days: int = Query(7, ge=1, le=30, description="Number of days to look back"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum events to return"),
    current_user: User = Depends(require_admin),
):
    """
    Get security audit events

    Requires: Admin role
    """
    try:
        redis_client = get_redis()

        # This is a simplified version - in production, you'd query audit logs more efficiently
        security_events = []

        # Get failed login attempts
        failed_logins = redis_client.get_analytics("failed_login", days=days)

        # Get financial data access events
        financial_access = redis_client.get_analytics(
            "financial_data_access", days=days
        )

        # Get admin actions
        admin_actions = redis_client.get_analytics("admin_action", days=days)

        summary = {
            "failed_login_attempts": sum(
                day["count"] for day in failed_logins.get("daily", [])
            ),
            "financial_data_accesses": sum(
                day["count"] for day in financial_access.get("daily", [])
            ),
            "admin_actions": sum(
                day["count"] for day in admin_actions.get("daily", [])
            ),
            "analysis_period_days": days,
        }

        return {
            "success": True,
            "security_summary": summary,
            "events": {
                "failed_logins": failed_logins,
                "financial_access": financial_access,
                "admin_actions": admin_actions,
            },
            "retrieved_by": current_user.id,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving security events: {str(e)}",
        )


@router.get("/performance-metrics")
async def get_performance_metrics(current_user: User = Depends(require_admin)):
    """
    Get system performance metrics

    Requires: Admin role
    """
    try:
        redis_client = get_redis()

        # Get Redis performance
        redis_health = redis_client.health_check()

        # Get cache performance
        cache_performance = get_cache_performance()

        # Get API performance metrics
        api_errors = redis_client.get_analytics("api_error", days=1)
        total_requests = redis_client.get_analytics("api_request", days=1)

        # Calculate error rate
        total_errors = sum(day["count"] for day in api_errors.get("daily", []))
        total_reqs = sum(day["count"] for day in total_requests.get("daily", []))
        error_rate = (total_errors / total_reqs * 100) if total_reqs > 0 else 0

        performance_metrics = {
            "redis": redis_health,
            "cache": cache_performance.get("cache_stats", {}),
            "api": {
                "error_rate_percentage": round(error_rate, 2),
                "total_requests_24h": total_reqs,
                "total_errors_24h": total_errors,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        return {
            "success": True,
            "performance_metrics": performance_metrics,
            "retrieved_by": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving performance metrics: {str(e)}",
        )


@router.post("/cache/invalidate")
async def invalidate_cache(
    cache_type: str = Query(..., description="Type of cache to invalidate"),
    identifier: Optional[str] = Query(
        None, description="Specific identifier (e.g., user_id)"
    ),
    current_user: User = Depends(require_admin),
):
    """
    Invalidate cache entries

    Requires: Admin role
    """
    try:
        from app.services.cached_financial_analysis_service import (
            cached_financial_service,
        )

        # Log admin action
        audit_logger.log_admin_action(
            admin_id=current_user.id,
            action="cache_invalidation",
            target=f"{cache_type}:{identifier or 'all'}",
            ip="unknown",  # Would get from request in real implementation
        )

        # Invalidate cache
        cached_financial_service.invalidate_cache(cache_type, identifier)

        return {
            "success": True,
            "message": f"Cache invalidated: {cache_type}",
            "cache_type": cache_type,
            "identifier": identifier,
            "invalidated_by": current_user.id,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error invalidating cache: {str(e)}",
        )


@router.get("/user-activity")
async def get_user_activity(
    user_id: Optional[str] = Query(None, description="Specific user ID"),
    days: int = Query(7, ge=1, le=30, description="Number of days to analyze"),
    current_user: User = Depends(require_admin),
):
    """
    Get user activity analytics

    Requires: Admin role
    """
    try:
        redis_client = get_redis()

        if user_id:
            # Get specific user activity
            user_events = {}
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                count = (
                    redis_client.get(f"user_events:{user_id}:{date}", parse_json=False)
                    or 0
                )
                user_events[date] = int(count)

            return {
                "success": True,
                "user_id": user_id,
                "activity": user_events,
                "total_events": sum(user_events.values()),
                "analysis_period_days": days,
                "retrieved_by": current_user.id,
            }
        else:
            # Get general user activity statistics
            total_users_active = 0  # Would calculate from actual data

            return {
                "success": True,
                "summary": {
                    "total_active_users": total_users_active,
                    "analysis_period_days": days,
                },
                "retrieved_by": current_user.id,
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user activity: {str(e)}",
        )


@router.get("/system-status")
async def get_system_status(current_user: User = Depends(require_admin)):
    """
    Get comprehensive system status

    Requires: Admin role
    """
    try:
        redis_client = get_redis()

        # Get various system metrics
        redis_health = redis_client.health_check()
        cache_stats = get_cache_performance()

        # Get recent activity
        recent_requests = redis_client.get_analytics("api_request", days=1)
        recent_errors = redis_client.get_analytics("api_error", days=1)

        # Calculate uptime and performance indicators
        total_requests_24h = sum(
            day["count"] for day in recent_requests.get("daily", [])
        )
        total_errors_24h = sum(day["count"] for day in recent_errors.get("daily", []))

        system_status = {
            "overall_status": "healthy",  # Would determine based on various factors
            "services": {
                "api": {
                    "status": "up",
                    "requests_24h": total_requests_24h,
                    "errors_24h": total_errors_24h,
                },
                "redis": redis_health,
                "cache": {
                    "status": "up" if redis_health["status"] == "connected" else "down",
                    "hit_rate": cache_stats.get("cache_stats", {}).get(
                        "hit_rate_percentage", 0
                    ),
                },
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        return {
            "success": True,
            "system_status": system_status,
            "retrieved_by": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving system status: {str(e)}",
        )


@router.post("/warm-cache/{user_id}")
async def warm_user_cache(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Warm cache for a specific user

    Requires: Admin role
    """
    try:
        from app.services.cached_financial_analysis_service import (
            cached_financial_service,
        )

        # Log admin action
        audit_logger.log_admin_action(
            admin_id=current_user.id,
            action="cache_warming",
            target=f"user:{user_id}",
            ip="unknown",
        )

        # Warm cache
        await cached_financial_service.warm_cache_for_user(user_id, db)

        return {
            "success": True,
            "message": f"Cache warmed for user: {user_id}",
            "user_id": user_id,
            "warmed_by": current_user.id,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error warming cache: {str(e)}",
        )
