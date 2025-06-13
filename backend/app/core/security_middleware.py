"""
Security Middleware

Provides rate limiting, audit logging, CORS protection,
and other security features for the FastAPI application.
"""

import time
import logging
import json
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import hashlib

from app.core.redis_client import get_redis
from app.database.models.user import User

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for rate limiting and audit logging"""

    def __init__(self, app, redis_client=None):
        super().__init__(app)
        self.redis = redis_client or get_redis()

        # Rate limit configurations
        self.rate_limits = {
            # Authentication endpoints
            "/api/v1/auth/login": {
                "limit": 5,
                "window": 300,
            },  # 5 attempts per 5 minutes
            "/api/v1/auth/register": {
                "limit": 3,
                "window": 3600,
            },  # 3 registrations per hour
            "/api/v1/auth/reset-password": {"limit": 3, "window": 3600},
            # Financial analysis endpoints (expensive operations)
            "/api/v1/financial-analysis/analyze-lead": {"limit": 20, "window": 3600},
            "/api/v1/financial-analysis/market-trends": {"limit": 10, "window": 3600},
            "/api/v1/financial-analysis/batch-analyze": {"limit": 5, "window": 3600},
            # Quiz endpoints
            "/api/v1/adaptive-quiz/start": {"limit": 10, "window": 3600},
            "/api/v1/adaptive-quiz/respond": {"limit": 100, "window": 3600},
            # Default rate limit for all other endpoints
            "default": {"limit": 100, "window": 3600},  # 100 requests per hour
        }

        # Endpoints that require audit logging
        self.audit_endpoints = {
            "/api/v1/financial-analysis/",
            "/api/v1/auth/",
            "/api/v1/users/",
            "/api/v1/adaptive-quiz/",
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through security middleware"""
        start_time = time.time()

        # Get client identifier (IP + User ID if available)
        client_ip = self._get_client_ip(request)
        user_id = await self._get_user_id_from_request(request)
        identifier = f"{client_ip}:{user_id}" if user_id else client_ip

        # Check rate limits
        rate_limit_result = self._check_rate_limit(request, identifier)
        if not rate_limit_result["allowed"]:
            return self._rate_limit_response(rate_limit_result)

        # Process request
        try:
            response = await call_next(request)

            # Add security headers
            response = self._add_security_headers(response)

            # Add rate limit headers
            response = self._add_rate_limit_headers(response, rate_limit_result)

            # Audit logging for sensitive endpoints
            if self._should_audit(request):
                await self._audit_log(request, response, user_id, start_time)

            # Track analytics
            self._track_request(request, response, user_id)

            return response

        except Exception as e:
            logger.error(f"Security middleware error: {str(e)}")
            # Log security incident
            await self._audit_log(request, None, user_id, start_time, error=str(e))
            raise

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers (for load balancers/proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

    async def _get_user_id_from_request(self, request: Request) -> Optional[str]:
        """Extract user ID from JWT token if available"""
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None

            # This is a simplified version - in practice, you'd decode the JWT
            # For now, we'll return None and rely on IP-based rate limiting
            return None

        except Exception:
            return None

    def _check_rate_limit(self, request: Request, identifier: str) -> Dict[str, Any]:
        """Check if request is within rate limits"""
        path = request.url.path
        method = request.method

        # Get rate limit config for this endpoint
        rate_config = None
        for endpoint, config in self.rate_limits.items():
            if endpoint != "default" and path.startswith(endpoint):
                rate_config = config
                break

        if not rate_config:
            rate_config = self.rate_limits["default"]

        # Create unique key for this endpoint and method
        rate_key = f"{identifier}:{method}:{path}"

        return self.redis.rate_limit_check(
            rate_key, rate_config["limit"], rate_config["window"]
        )

    def _rate_limit_response(self, rate_limit_result: Dict[str, Any]) -> JSONResponse:
        """Return rate limit exceeded response"""
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later.",
                "retry_after": rate_limit_result.get("reset_time", 0),
            },
            headers={
                "Retry-After": str(rate_limit_result.get("reset_time", 60)),
                "X-RateLimit-Limit": str(rate_limit_result.get("limit", 0)),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(rate_limit_result.get("reset_time", 0)),
            },
        )

    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response"""
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

        for header, value in security_headers.items():
            response.headers[header] = value

        return response

    def _add_rate_limit_headers(
        self, response: Response, rate_limit_result: Dict[str, Any]
    ) -> Response:
        """Add rate limit headers to response"""
        if rate_limit_result:
            response.headers["X-RateLimit-Remaining"] = str(
                rate_limit_result.get("remaining", 0)
            )
            response.headers["X-RateLimit-Reset"] = str(
                rate_limit_result.get("reset_time", 0)
            )

        return response

    def _should_audit(self, request: Request) -> bool:
        """Check if request should be audited"""
        path = request.url.path
        return any(audit_path in path for audit_path in self.audit_endpoints)

    async def _audit_log(
        self,
        request: Request,
        response: Optional[Response],
        user_id: Optional[str],
        start_time: float,
        error: Optional[str] = None,
    ):
        """Log security-relevant events"""
        try:
            duration = time.time() - start_time

            audit_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": self._get_client_ip(request),
                "user_agent": request.headers.get("User-Agent", ""),
                "user_id": user_id,
                "duration_ms": round(duration * 1000, 2),
                "status_code": response.status_code if response else None,
                "error": error,
            }

            # Hash sensitive data
            if request.method in ["POST", "PUT", "PATCH"]:
                # Don't log actual request body, just a hash for integrity
                body_hash = hashlib.sha256(str(request.url.path).encode()).hexdigest()[
                    :16
                ]
                audit_data["request_hash"] = body_hash

            # Store in Redis with 30-day expiration
            audit_key = (
                f"audit:{datetime.utcnow().strftime('%Y-%m-%d')}:{int(time.time())}"
            )
            self.redis.set(audit_key, audit_data, expire=86400 * 30)

            # Also log to application logger for immediate monitoring
            logger.info(f"AUDIT: {audit_data}")

        except Exception as e:
            logger.error(f"Audit logging failed: {str(e)}")

    def _track_request(
        self, request: Request, response: Response, user_id: Optional[str]
    ):
        """Track request for analytics"""
        try:
            # Track general API usage
            self.redis.track_event("api_request", user_id)

            # Track specific endpoints
            path = request.url.path
            if "/financial-analysis/" in path:
                self.redis.track_event("financial_analysis_request", user_id)
            elif "/adaptive-quiz/" in path:
                self.redis.track_event("quiz_request", user_id)
            elif "/auth/" in path:
                self.redis.track_event("auth_request", user_id)

            # Track errors
            if response.status_code >= 400:
                self.redis.track_event(
                    "api_error", user_id, {"status_code": response.status_code}
                )

        except Exception as e:
            logger.error(f"Request tracking failed: {str(e)}")


class AuditLogger:
    """Dedicated audit logger for security events"""

    def __init__(self, redis_client=None):
        self.redis = redis_client or get_redis()

    def log_login_attempt(self, email: str, success: bool, ip: str, user_agent: str):
        """Log login attempts"""
        event_data = {
            "event_type": "login_attempt",
            "timestamp": datetime.utcnow().isoformat(),
            "email": email,
            "success": success,
            "ip": ip,
            "user_agent": user_agent,
        }

        self._store_audit_event(event_data)

        # Track failed login attempts for security monitoring
        if not success:
            self.redis.track_event("failed_login", metadata={"email": email, "ip": ip})

    def log_financial_access(self, user_id: str, action: str, resource: str, ip: str):
        """Log access to financial data"""
        event_data = {
            "event_type": "financial_access",
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "ip": ip,
        }

        self._store_audit_event(event_data)
        self.redis.track_event("financial_data_access", user_id)

    def log_admin_action(self, admin_id: str, action: str, target: str, ip: str):
        """Log administrative actions"""
        event_data = {
            "event_type": "admin_action",
            "timestamp": datetime.utcnow().isoformat(),
            "admin_id": admin_id,
            "action": action,
            "target": target,
            "ip": ip,
        }

        self._store_audit_event(event_data)
        self.redis.track_event("admin_action", admin_id)

    def _store_audit_event(self, event_data: Dict[str, Any]):
        """Store audit event in Redis"""
        try:
            audit_key = f"audit_event:{datetime.utcnow().strftime('%Y-%m-%d')}:{int(time.time())}"
            self.redis.set(audit_key, event_data, expire=86400 * 90)  # Keep for 90 days

            # Also log to file for compliance
            logger.info(f"SECURITY_AUDIT: {json.dumps(event_data)}")

        except Exception as e:
            logger.error(f"Failed to store audit event: {str(e)}")


# Global audit logger instance
audit_logger = AuditLogger()


def setup_cors_middleware(app):
    """Setup CORS middleware with secure defaults"""

    # Get allowed origins from environment
    import os

    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Reset"],
    )


def setup_security_middleware(app):
    """Setup security middleware"""
    app.add_middleware(SecurityMiddleware)


# Rate limiting decorator for specific endpoints
def rate_limit(limit: int, window: int):
    """Decorator for endpoint-specific rate limiting"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would be implemented with dependency injection
            # For now, it's a placeholder
            return await func(*args, **kwargs)

        return wrapper

    return decorator
