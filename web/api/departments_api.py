from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from services.department_service import DepartmentService
from services.agent_orchestration_service import get_orchestration_service
from schemas.department import DepartmentRead, DepartmentUpdate

router = APIRouter(prefix="/api/v1/departments", tags=["Departments"])

@router.get("/", response_model=List[DepartmentRead])
async def get_all_departments():
    """
    Retreive all 18 Agent Departments with their current metrics and agents.
    """
    service = DepartmentService()
    return await service.get_all_departments()

@router.get("/{dept_id}", response_model=DepartmentRead)
async def get_department(dept_id: int):
    """
    Retrieve details for a specific Agent Department.
    """
    service = DepartmentService()
    dept = await service.get_department_by_id(dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail=f"Department {dept_id} not found")
    return dept

@router.post("/{dept_id}/metrics")
async def update_metric(dept_id: int, update: DepartmentUpdate):
    """
    Update the primary metric for a department.
    """
    if update.primary_metric_value is None:
        raise HTTPException(status_code=400, detail="primary_metric_value is required")
        
    service = DepartmentService()
    success = await service.update_department_metric(dept_id, update.primary_metric_value)
    if not success:
        raise HTTPException(status_code=404, detail=f"Department {dept_id} not found")
    return {"success": True}

@router.post("/{dept_id}/agents/{agent_id}/invoke")
async def invoke_specific_agent(dept_id: int, agent_id: str, payload: Dict[str, Any]):
    """
    Directly invoke a specialized agent within a department.
    """
    orch_service = get_orchestration_service()
    result = await orch_service.invoke_agent(agent_id, payload)
    if "error" in result:
        if result["error"] == "Agent Not Found":
            raise HTTPException(status_code=404, detail=result["error"])
        raise HTTPException(status_code=500, detail=result["error"])
    return result
