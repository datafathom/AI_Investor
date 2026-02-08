import logging
from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from services.neo4j.neo4j_service import get_neo4j

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/graph", tags=["Admin", "Infrastructure"])

@router.get("/schema")
async def get_graph_schema():
    """Get the visual schema of the Neo4j graph (nodes and relationships)."""
    try:
        neo = get_neo4j()
        return neo.get_schema()
    except Exception as e:
        logger.exception("Error fetching graph schema")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def execute_cypher_query(query: str = Body(..., embed=True)):
    """Execute a raw Cypher query against Neo4j."""
    try:
        neo = get_neo4j()
        results = neo.execute_query(query)
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.exception("Error executing Cypher query")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/count")
async def get_node_counts():
    """Get counts of nodes grouped by label."""
    try:
        neo = get_neo4j()
        return neo.execute_query("MATCH (n) RETURN labels(n) as label, count(*) as count")
    except Exception as e:
        logger.exception("Error counting nodes")
        raise HTTPException(status_code=500, detail=str(e))
