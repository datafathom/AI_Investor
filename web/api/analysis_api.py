from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging

from services.analysis.fundamental_scanner import FundamentalScanner

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/analysis", tags=["Analysis"])

class ScanCriterion(BaseModel):
    metric: str
    operator: str
    value: float

class ScanRequest(BaseModel):
    criteria: List[ScanCriterion]

@router.get("/metrics")
async def list_metrics():
    service = FundamentalScanner()
    return await service.list_metrics()

@router.post("/scan")
async def run_scan(req: ScanRequest):
    service = FundamentalScanner()
    return await service.run_scan(req.criteria)

@router.get("/companies/{ticker}")
async def get_company(ticker: str):
    service = FundamentalScanner()
    company = await service.get_company_details(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
