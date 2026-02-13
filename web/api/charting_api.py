from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from services.charting.chart_engine import ChartEngine
from services.charting.charting_service import ChartingService, get_charting_service

router = APIRouter(prefix="/api/v1/charting", tags=["Charting"])

class DrawingRequest(BaseModel):
    drawings: List[Dict[str, Any]]

class LayoutRequest(BaseModel):
    name: str
    config: Dict[str, Any]

# --- Data Endpoints (Delegating to ChartingService) ---

@router.get("/candles/{ticker}")
async def get_candles(
    ticker: str, 
    timeframe: str = "1day", 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    service: ChartingService = Depends(get_charting_service)
):
    # Convert dates if needed, service handles logic
    return await service.get_chart_data(symbol=ticker, timeframe=timeframe)

# --- Advanced Features (ChartEngine) ---

@router.get("/drawings/{chart_id}")
async def get_drawings(chart_id: str):
    engine = ChartEngine()
    return await engine.get_drawings(chart_id)

@router.post("/drawings/{chart_id}")
async def save_drawings(chart_id: str, req: DrawingRequest):
    engine = ChartEngine()
    return await engine.save_drawings(chart_id, req.drawings)

@router.get("/layouts")
async def get_layouts():
    engine = ChartEngine()
    return await engine.get_layouts()

@router.post("/layouts")
async def save_layout(req: LayoutRequest):
    engine = ChartEngine()
    return await engine.save_layout(req.name, req.config)

# --- MTF Analysis ---
from services.charting.mtf_analyzer import MultiTimeframeAnalyzer

@router.get("/mtf/{ticker}")
async def get_mtf_analysis(ticker: str):
    analyzer = MultiTimeframeAnalyzer()
    return await analyzer.analyze_trend_alignment(ticker)

# --- Heatmap ---
from services.charting.heatmap_generator import HeatmapGenerator

@router.get("/heatmaps/correlation")
async def get_correlation_heatmap():
    generator = HeatmapGenerator()
    return await generator.get_correlation_heatmap()

@router.get("/heatmaps/sector")
async def get_sector_heatmap():
    generator = HeatmapGenerator()
    return await generator.get_sector_heatmap()

# --- Export & Share ---

class ExportRequest(BaseModel):
    chart_id: Optional[str] = None
    format: str = "png"
    # In a real app, you'd pass the actual image data or state here
    
@router.post("/export")
async def export_chart(req: ExportRequest):
    # Mock export
    return {"url": f"https://mock-storage.com/charts/{uuid.uuid4()}.{req.format}", "status": "ready"}

@router.post("/share")
async def create_share_link(req: ExportRequest):
    # Mock share link
    link_id = uuid.uuid4()
    return {"link": f"https://ai-investor.com/c/{link_id}", "expires_in": "7days"}
