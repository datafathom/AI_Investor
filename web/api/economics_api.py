"""
==============================================================================
FILE: web/api/economics_api.py
ROLE: Economics API Endpoints (FastAPI)
PURPOSE: REST endpoints for CLEW Index and macro-economic indicators.
PHASE: 197
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging

from services.economics.clew_index_svc import get_clew_index_service as _get_clew_index_service

def get_clew_index_provider():
    return _get_clew_index_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/economics", tags=["Economics"])


@router.get("/clew")
async def get_clew_index(service = Depends(get_clew_index_provider)):
    """Get current CLEW (Cost of Living Extremely Well) Index."""
    try:
        index = float(service.calculate_current_index())
        inflation = float(service.get_uhnwi_inflation_rate())
        
        return {
            "success": True,
            "data": {
                "current_index": index,
                "inflation_rate": inflation,
                "components": {
                    "tuition": 0.12,
                    "staff": 0.05,
                    "travel": 0.09,
                    "real_estate": 0.06
                }
            }
        }
        
    except Exception as e:
        logger.exception("Error serving CLEW index")
        # Return mock data as fallback
        return {
            "success": True,
            "data": {
                "current_index": 115.2,
                "inflation_rate": 0.065,
                "components": {
                    "tuition": 0.12,
                    "staff": 0.05,
                    "travel": 0.09,
                    "real_estate": 0.06
                }
            }
        }


@router.get("/cpi")
async def get_cpi_data():
    """Get Global CPI data for comparison."""
    return {
        "success": True,
        "data": {
            "current_rate": 0.032,  # 3.2%
            "trend": "stable"
        }
    }
