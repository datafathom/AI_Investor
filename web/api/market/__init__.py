"""
Market API Package
Exposes routers for market analysis endpoints.
"""

from fastapi import APIRouter

from .regime_api import router as regime_router

router = APIRouter(prefix="/api/v1/market", tags=["Market"])

router.include_router(regime_router)
