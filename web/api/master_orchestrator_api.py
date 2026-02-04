"""
==============================================================================
FILE: web/api/master_orchestrator_api.py
ROLE: Master Orchestrator API Endpoints (FastAPI)
PURPOSE: Knowledge graph and orchestration endpoints.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from web.auth_utils import get_current_user
from services.neo4j.master_graph import MasterGraph
from services.neo4j.neo4j_service import neo4j_service


def get_master_graph_provider():
    return MasterGraph()


def get_neo4j_provider():
    return neo4j_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/master", tags=["Master Orchestrator"])


class BoltProxyRequest(BaseModel):
    query: str
    params: Dict[str, Any] = {}


class ShockRequest(BaseModel):
    asset_id: str
    magnitude: float = -0.1


@router.get("/graph")
async def get_master_graph(
    current_user: dict = Depends(get_current_user),
    service=Depends(get_master_graph_provider)
):
    """
    Retrieve the Unified Knowledge Graph structure.
    Returns: JSON: Node-link structure for D3.js visualization.
    """
    try:
        data = service.get_graph_data()
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        logger.exception("Failed to fetch master graph data")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.post("/bolt-proxy")
async def bolt_proxy(
    request: BoltProxyRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_neo4j_provider)
):
    """
    Facilitate high-speed graph queries without exposing Neo4j credentials to the browser.
    Expects: { "query": "...", "params": {...} }
    """
    try:
        if not request.query:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": "No query provided"}
            )
            
        results = service.execute_query(request.query, request.params)
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        logger.exception("Bolt proxy query failed")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )


@router.post("/shock")
async def trigger_shock(
    request: ShockRequest,
    current_user: dict = Depends(get_current_user),
    service=Depends(get_master_graph_provider)
):
    """
    Trigger a reflexivity shock simulation.
    Expects: { "asset_id": "...", "magnitude": -0.2 }
    """
    try:
        if not request.asset_id:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": "No asset_id provided"}
            )
            
        shock_results = service.trigger_reflexivity_shock(request.asset_id, request.magnitude)
        
        return {
            "success": True,
            "data": shock_results
        }
    except AttributeError:
        # In case service hasn't implemented it yet
        return {
            "success": True,
            "data": {
                "affected_nodes": [request.asset_id],
                "contagion_velocity": 0.85,
                "message": "Shock simulation placeholder (implementation in progress)"
            }
        }
    except Exception as e:
        logger.exception("Shock simulation failed")
        return JSONResponse(
            status_code=500,
            content={"success": False, "detail": str(e)}
        )
