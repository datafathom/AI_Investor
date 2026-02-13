from fastapi import APIRouter, HTTPException
from typing import List, Dict
from services.external.external_data_service import ExternalDataService

router = APIRouter(prefix="/api/v1/external-data", tags=["External Data"])

@router.get("/sources")
async def list_sources():
    service = ExternalDataService()
    return await service.list_sources()

@router.post("/sources/{id}/toggle")
async def toggle_source(id: str):
    service = ExternalDataService()
    result = await service.toggle_source(id)
    if not result:
        raise HTTPException(status_code=404, detail="Source not found")
    return result

@router.get("/stats")
async def get_stats():
    service = ExternalDataService()
    return await service.get_usage_stats()
