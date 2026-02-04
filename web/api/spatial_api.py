"""
==============================================================================
FILE: web/api/spatial_api.py
ROLE: The Spatial Navigator (FastAPI)
PURPOSE:
    Expose endpoints for 3D/Spatial data visualization.
    Converts graph entities into 3D coordinate-ready JSON.
==============================================================================
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import random
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/spatial", tags=["Spatial"])


@router.get("/portfolio")
async def get_spatial_portfolio():
    """
    Returns portfolio holdings with synthetic 3D coordinates.
    In a real Neo4j setup, these coords would be derived from relationship clustering.
    """
    tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "GOOGL", "NVDA", "BTC", "ETH"]
    nodes = []
    links = []

    for i, ticker in enumerate(tickers):
        nodes.append({
            "id": ticker,
            "label": ticker,
            "val": random.randint(10, 50),
            "color": "#3b82f6" if i % 2 == 0 else "#10b981",
            "x": random.uniform(-50, 50),
            "y": random.uniform(-50, 50),
            "z": random.uniform(-50, 50)
        })

    # Create synthetic links
    for i in range(len(nodes) - 1):
        links.append({
            "source": nodes[i]["id"],
            "target": nodes[i+1]["id"]
        })

    return {
        "success": True,
        "data": {
            "nodes": nodes,
            "links": links
        }
    }


@router.get("/status")
async def get_xr_status():
    """Returns XR engine status."""
    return {
        "success": True,
        "data": {
            "status": "ready",
            "mode": "WebXRv1",
            "engine": "Three.js"
        }
    }
