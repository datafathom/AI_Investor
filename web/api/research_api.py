from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel
import logging

from services.research.workspace import ResearchWorkspace

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/research", tags=["Research"])

# --- Models ---
class NotebookCreate(BaseModel):
    name: str

class CellExecute(BaseModel):
    code: str

# --- Endpoints ---

@router.get("/notebooks")
async def list_notebooks():
    service = ResearchWorkspace()
    return await service.list_notebooks()

@router.post("/notebooks")
async def create_notebook(req: NotebookCreate):
    service = ResearchWorkspace()
    return await service.create_notebook(req.name)

@router.get("/notebooks/{id}")
async def get_notebook(id: str):
    service = ResearchWorkspace()
    nb = await service.get_notebook(id)
    if not nb:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return nb

@router.put("/notebooks/{id}")
async def save_notebook(id: str, notebook: Dict):
    service = ResearchWorkspace()
    updated = await service.save_notebook(id, notebook)
    if not updated:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return updated

@router.post("/notebooks/{id}/execute")
async def execute_cell(id: str, req: CellExecute):
    service = ResearchWorkspace()
    return await service.execute_cell(id, req.code)

@router.post("/notebooks/{id}/restart")
async def restart_kernel(id: str):
    service = ResearchWorkspace()
    await service.restart_kernel(id)
    return {"status": "restarted"}
