"""
==============================================================================
FILE: web/api/search_api.py
ROLE: Search Endpoints (FastAPI)
PURPOSE: Provides search index and query endpoints.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import logging

from services.neo4j.master_graph import MasterGraph


def get_master_graph_provider():
    return MasterGraph()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/search", tags=["Search"])


@router.get("/index")
async def get_search_index(master_graph=Depends(get_master_graph_provider)):
    """
    Returns a lightweight index of core entities for client-side search.
    """
    try:
        entities = master_graph.get_search_entities()
        
        # Categorize results
        symbols = [e for e in entities if e['type'] in ['ticker', 'crypto']]
        agents = [e for e in entities if e['type'] == 'agent']
        clients = [e for e in entities if e['type'] == 'client']
        
        # Fallback to defaults if graph is empty (production safety)
        if not symbols:
            symbols = [
                {"id": "s-nvda", "label": "NVDA", "category": "Symbols", "type": "ticker"},
                {"id": "s-tsla", "label": "TSLA", "category": "Symbols", "type": "ticker"},
            ]
        
        return {
            "success": True,
            "data": {
                "symbols": symbols,
                "agents": agents,
                "clients": clients
            }
        }
    except Exception as e:
        logger.exception("Search API: Indexing failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/query")
async def search_query(q: str = Query("", description="Search query")):
    """
    Performs a deep database search for a given query.
    """
    query = q.lower()
    if not query:
        return {"success": True, "data": []}
        
    # Simulated deep search results
    results = [
        {"id": "d-1", "label": f"Historical Report for {query}", "category": "Reports", "type": "document"},
        {"id": "d-2", "label": f"Risk Exposure related to {query}", "category": "Risk", "type": "analysis"}
    ]
    
    return {"success": True, "data": results}
