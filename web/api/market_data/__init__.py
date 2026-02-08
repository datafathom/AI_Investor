"""
Market Data API Package
Exposes routers for market data endpoints.
"""

from fastapi import APIRouter

from .forced_sellers_api import router as forced_sellers_router
from .whale_flow_api import router as whale_flow_router
from .promo_api import router as promo_router

router = APIRouter(prefix="/market-data", tags=["Market Data"])

router.include_router(forced_sellers_router)
router.include_router(whale_flow_router)
router.include_router(promo_router)
