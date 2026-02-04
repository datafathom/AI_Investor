"""
==============================================================================
FILE: web/api/marketplace_api.py
ROLE: Marketplace API Endpoints (FastAPI)
PURPOSE: REST endpoints for extension marketplace.
==============================================================================
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from pydantic import BaseModel
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/marketplace", tags=["Marketplace"])


class CreateExtensionRequest(BaseModel):
    developer_id: str
    extension_name: str
    description: str
    version: str
    category: str


class InstallRequest(BaseModel):
    user_id: str


class ReviewRequest(BaseModel):
    user_id: str
    rating: int
    comment: Optional[str] = None


# Mock extension data
MOCK_EXTENSIONS = [
    {
        "id": "ext_001",
        "name": "Advanced Charts Pro",
        "description": "Professional charting with 50+ indicators",
        "version": "2.1.0",
        "category": "charting",
        "author": "TradingTools Inc",
        "rating": 4.8,
        "installs": 15420,
        "price": 0
    },
    {
        "id": "ext_002",
        "name": "AI Signal Generator",
        "description": "ML-powered trading signals",
        "version": "1.5.2",
        "category": "analytics",
        "author": "QuantAI Labs",
        "rating": 4.5,
        "installs": 8750,
        "price": 29.99
    },
    {
        "id": "ext_003",
        "name": "Portfolio Optimizer",
        "description": "Automatic portfolio rebalancing",
        "version": "3.0.1",
        "category": "portfolio",
        "author": "OptimizeX",
        "rating": 4.6,
        "installs": 12300,
        "price": 0
    }
]

MOCK_INSTALLED = [
    {"extension_id": "ext_001", "installed_at": "2026-01-15T10:00:00Z", "enabled": True},
    {"extension_id": "ext_003", "installed_at": "2026-01-20T14:30:00Z", "enabled": True}
]


@router.get("/extensions")
async def get_extensions(category: Optional[str] = Query(None)):
    """Get available extensions."""
    extensions = MOCK_EXTENSIONS
    if category:
        extensions = [e for e in extensions if e["category"] == category]
    
    return {
        "success": True,
        "data": extensions
    }


@router.get("/installed")
async def get_installed_extensions(user_id: str = Query("user_1")):
    """Get user's installed extensions."""
    # Enrich installed extensions with full details
    installed = []
    for inst in MOCK_INSTALLED:
        ext = next((e for e in MOCK_EXTENSIONS if e["id"] == inst["extension_id"]), None)
        if ext:
            installed.append({**ext, **inst})
    
    return {
        "success": True,
        "data": installed
    }


@router.get("/extension/{extension_id}")
async def get_extension_details(extension_id: str):
    """Get extension details."""
    ext = next((e for e in MOCK_EXTENSIONS if e["id"] == extension_id), None)
    if not ext:
        return JSONResponse(status_code=404, content={"success": False, "detail": "Extension not found"})
    
    return {
        "success": True,
        "data": ext
    }


@router.post("/extension/create")
async def create_extension(request: CreateExtensionRequest):
    """Create extension."""
    extension_id = f"ext_{uuid.uuid4().hex[:6]}"
    
    return {
        "success": True,
        "data": {
            "id": extension_id,
            "name": request.extension_name,
            "description": request.description,
            "version": request.version,
            "category": request.category,
            "author": request.developer_id,
            "rating": 0,
            "installs": 0,
            "price": 0,
            "status": "pending_review"
        }
    }


@router.post("/extension/{extension_id}/install")
async def install_extension(extension_id: str, request: InstallRequest):
    """Install extension."""
    return {
        "success": True,
        "data": {
            "extension_id": extension_id,
            "user_id": request.user_id,
            "installed_at": "2026-02-03T10:00:00Z",
            "enabled": True
        }
    }


@router.post("/extension/{extension_id}/uninstall")
async def uninstall_extension(extension_id: str, request: InstallRequest):
    """Uninstall extension."""
    return {
        "success": True,
        "data": {
            "extension_id": extension_id,
            "user_id": request.user_id,
            "uninstalled_at": "2026-02-03T10:00:00Z"
        }
    }


@router.post("/extension/{extension_id}/review")
async def add_review(extension_id: str, request: ReviewRequest):
    """Add review for extension."""
    if request.rating < 1 or request.rating > 5:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Rating must be between 1 and 5"})
    
    return {
        "success": True,
        "data": {
            "review_id": f"rev_{uuid.uuid4().hex[:8]}",
            "extension_id": extension_id,
            "user_id": request.user_id,
            "rating": request.rating,
            "comment": request.comment,
            "created_at": "2026-02-03T10:00:00Z"
        }
    }
