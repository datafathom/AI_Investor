import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from services.system.logging_service import get_logging_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/logs", tags=["Admin", "Infrastructure"])

@router.get("/search")
async def search_logs(
    query: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = 0
):
    """Search system logs with filters."""
    try:
        logging_svc = get_logging_service()
        results = logging_svc.search(query=query, level=level, limit=limit, offset=offset)
        return {
            "results": results,
            "count": len(results),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.exception("Error searching logs")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
async def list_log_files():
    """List available log files on disk."""
    try:
        logging_svc = get_logging_service()
        return logging_svc.list_log_files()
    except Exception as e:
        logger.exception("Error listing log files")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tail/{filename}")
async def tail_log_file(filename: str, lines: int = Query(50, le=500)):
    """Tail the last N lines of a specific log file."""
    try:
        logging_svc = get_logging_service()
        return logging_svc.tail_file(filename, lines)
    except Exception as e:
        logger.exception(f"Error tailing log file {filename}")
        raise HTTPException(status_code=500, detail=str(e))
