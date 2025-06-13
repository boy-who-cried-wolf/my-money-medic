"""API router module."""

from fastapi import APIRouter

from .v1 import api_router as api_router_v1

# Create main API router
api_router = APIRouter()

# Include versioned routers
api_router.include_router(api_router_v1, prefix="/v1")
