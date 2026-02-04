"""
==============================================================================
FILE: web/api/evolution_api.py
ROLE: Generative Dispatcher (FastAPI)
PURPOSE: Expose the Strategy Distillery to the frontend.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Body, Path, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any

from services.analysis.genetic_distillery import get_genetic_distillery
from services.evolution.gene_logic import get_gene_splicer
from services.evolution.playback_service import get_playback_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/evolution", tags=["Evolution"])

# Global instance for demo (should ideally be handled via Dependency Injection or App State)
_distillery = None


class SpliceRequest(BaseModel):
    parent1_id: str
    parent2_id: str
    parent1_genes: Dict[str, Any]
    parent2_genes: Dict[str, Any]
    bounds: Optional[Dict[str, tuple]] = {
        "rsi_period": (7, 30),
        "rsi_buy": (15, 45),
        "rsi_sell": (55, 85),
        "stop_loss": (0.01, 0.10)
    }


class PlaybackRequest(BaseModel):
    genes: Dict[str, Any]
    price_data: List[Dict[str, Any]]


class PulseRequest(BaseModel):
    genes: Dict[str, Any]


@router.post("/start")
async def start_evolution():
    global _distillery
    bounds = {
        "rsi_period": (7, 30),
        "rsi_buy": (15, 45),
        "rsi_sell": (55, 85),
        "stop_loss": (0.01, 0.10)
    }
    _distillery = get_genetic_distillery(bounds)
    _distillery.initialize_population()
    
    # Run 5 generations immediately for demo
    def mock_fitness(genes):
        return (genes["rsi_period"] / 10.0) + (genes["rsi_buy"] / 20.0)
        
    for _ in range(5):
        _distillery.evolve(mock_fitness)
        
    return {
        "success": True,
        "data": {
            "status": "success",
            "message": "Evolution started",
            "current_generation": _distillery.current_generation,
            "history": _distillery.history
        }
    }


@router.get("/status")
async def get_status():
    global _distillery
    if not _distillery:
        return JSONResponse(status_code=400, content={"success": False, "detail": "Evolution not started"})
        
    return {
        "success": True,
        "data": {
            "current_generation": _distillery.current_generation,
            "best_performer": {
                "genes": _distillery.population[0].genes,
                "fitness": _distillery.population[0].fitness
            },
            "history": _distillery.history
        }
    }


@router.post("/splice")
async def splice_agents(request: SpliceRequest):
    """Splicing two agents into a new hybrid."""
    try:
        splicer = get_gene_splicer()
        child = splicer.splice_agents(
            request.parent1_id, 
            request.parent2_id, 
            request.parent1_genes, 
            request.parent2_genes, 
            request.bounds
        )

        return {
            "status": "success",
            "data": child
        }
    except Exception as e:
        logger.exception("Splicing failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/playback")
async def genomic_playback(request: PlaybackRequest):
    """Re-run historical data for a given genome."""
    try:
        service = get_playback_service()
        result = service.run_playback(request.genes, request.price_data)

        return {
            "success": True,
            "data": {
                "final_value": result.final_value,
                "total_return": result.total_return,
                "trades": result.trades_executed,
                "history": result.history
            }
        }
    except Exception as e:
        logger.exception("Playback failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/pulse/{agent_id}")
async def get_gene_pulse(
    agent_id: str = Path(...),
    request: PulseRequest = Body(...)
):
    """Sprint 6: Micro-view of gene activation and instability."""
    try:
        splicer = get_gene_splicer()
        pulse = splicer.get_gene_pulse(agent_id, request.genes)
        return {"success": True, "data": pulse}
    except Exception as e:
        logger.exception("Pulse fetch failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
