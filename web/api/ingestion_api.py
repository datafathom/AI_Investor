from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from services.ingestion.pipeline_manager import PipelineManager, PipelineConfig, PipelineRun
from services.ingestion.quality_checker import QualityChecker, QualityIssue

router = APIRouter(prefix="/api/v1/ingestion", tags=["Ingestion"])

# --- Pipeline Endpoints ---

@router.get("/pipelines", response_model=List[PipelineConfig])
async def list_pipelines():
    mgr = PipelineManager()
    return mgr.list_pipelines()

@router.get("/pipelines/{id}", response_model=PipelineConfig)
async def get_pipeline_details(id: str):
    mgr = PipelineManager()
    pipeline = mgr.get_pipeline(id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline

@router.post("/pipelines/{id}/trigger")
async def trigger_pipeline(id: str):
    mgr = PipelineManager()
    try:
        run_id = await mgr.trigger_pipeline(id)
        return {"message": "Pipeline triggered", "run_id": run_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/pipelines/{id}/runs", response_model=List[PipelineRun])
async def get_pipeline_runs(id: str):
    mgr = PipelineManager()
    return mgr.get_pipeline_runs(id)

@router.patch("/pipelines/{id}")
async def update_pipeline_config(id: str, config: Dict):
    mgr = PipelineManager()
    try:
        updated = mgr.update_pipeline(id, config)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- Quality Endpoints ---

@router.get("/quality/summary")
async def get_quality_summary():
    checker = QualityChecker()
    return checker.get_summary()

@router.get("/quality/issues", response_model=List[QualityIssue])
async def list_quality_issues():
    checker = QualityChecker()
    return checker.list_issues()

@router.post("/quality/issues/{id}/resolve")
async def resolve_issue(id: str):
    checker = QualityChecker()
    success = checker.resolve_issue(id)
    if not success:
        raise HTTPException(status_code=404, detail="Issue not found")
    return {"message": "Issue resolved"}
