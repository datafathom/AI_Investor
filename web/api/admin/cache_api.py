import logging
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from services.infrastructure.cache_service import get_agent_cache
# from services.caching.performance_cache import get_performance_cache # I'll check if this exists

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cache", tags=["Admin", "Infrastructure"])

@router.get("/stats")
async def get_cache_stats():
    """Aggregate cache statistics."""
    try:
        from services.caching.performance_cache import get_cache
        eb_stats = get_agent_cache().get_stats()
        perf_stats = get_cache().get_stats()
        
        return {
            "agent_cache": eb_stats,
            "performance_cache": perf_stats
        }
    except Exception as e:
        logger.exception("Error fetching cache stats")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{cache_name}/invalidate")
async def invalidate_cache(cache_name: str, pattern: str = Query("*")):
    """Invalidate cache entries by pattern."""
    try:
        if cache_name == "agent_cache":
            count = get_agent_cache().invalidate_pattern(pattern)
            return {"status": "success", "message": f"Invalidated {count} entries in {cache_name}"}
        elif cache_name == "performance_cache":
            from services.caching.performance_cache import get_cache
            get_cache().invalidate_pattern(pattern)
            return {"status": "success", "message": f"Invalidated entries matching {pattern} in {cache_name}"}
        else:
            raise HTTPException(status_code=404, detail=f"Cache {cache_name} not found")
    except Exception as e:
        logger.exception(f"Error invalidating cache {cache_name}")
        raise HTTPException(status_code=500, detail=str(e))
