from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import logging
import os
from datetime import timezone, datetime
from agents.autocoder_agent import get_autocoder_agent
from services.blue_green_service import get_blue_green_service
from services.analytics.alpha_reporting import get_alpha_reporting_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dev", tags=["Developer"])

class CodeGenerateRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None

class CodeValidateRequest(BaseModel):
    code: str

class CodeDeployRequest(BaseModel):
    agent_id: str
    code: str
    file_path: str

@router.get("/status")
async def get_dev_status():
    """Get development environment status."""
    return {
        "success": True,
        "data": {
            "autocoder_active": True,
            "last_activity": datetime.now(timezone.utc).isoformat() + "Z",
            "pending_tasks": 0,
            "completed_tasks": 15,
            "system_health": {
                "cpu_usage": 35.5,
                "memory_usage": 62.3,
                "disk_usage": 48.1
            }
        }
    }

@router.post("/hotswap")
async def hotswap_agent_logic(request: CodeDeployRequest):
    """Zero-Downtime Hot-Swap deployment."""
    try:
        bg_service = get_blue_green_service()
        result = await bg_service.deploy_hot_swap(
            agent_id=request.agent_id,
            new_code=request.code,
            file_path=request.file_path
        )
        return result
    except Exception as e:
        logger.exception("Hot-Swap failed")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/traces")
async def get_replay_traces():
    """Fetch recent traces for log replay debugger."""
    # Mock trace feed for debugger
    return {
        "success": True,
        "data": [
            { "id": "tr_991", "agent": "scraper_01", "status": "FAILED", "input": "Search: SEC Filings", "error": "RateLimit" },
            { "id": "tr_992", "agent": "analyst_02", "status": "FAILED", "input": "Analyze: AAPL 10-K", "error": "ParsingError" },
            { "id": "tr_993", "agent": "trader_05", "status": "SUCCESS", "input": "Buy 100 TSLA", "error": None }
        ]
    }

@router.get("/report/eod")
async def get_eod_report(encrypt: bool = Query(True)):
    """Fetch the latest EOD Alpha Report."""
    try:
        reporting_svc = get_alpha_reporting_service()
        report = reporting_svc.generate_eod_report(encrypt=encrypt)
        return {"success": True, "data": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_code(request: CodeGenerateRequest):
    """Generate code using AutocoderAgent."""
    try:
        # Mock fallback for development if no API key is present
        if not os.getenv("OPENAI_API_KEY"):
            return {
                "success": True,
                "code": "def hello_investor():\n    \"\"\"Generated mock strategy\"\"\"\n    print('Analyzing market sentiment...')\n    return {'status': 'bullish', 'confidence': 0.85}\n\nresult = hello_investor()\nprint(f'Signal: {result}')",
                "model": "mock-gpt-4-sandbox"
            }
        
        agent = get_autocoder_agent()
        result = await agent.generate_code(request.task, context=request.context, execute=False)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return {
            "success": True,
            "code": result["code"],
            "model": result["model"]
        }
    except Exception as e:
        import traceback
        logger.exception("Autocoder generation failed")
        raise HTTPException(status_code=500, detail=f"DEBUG ERROR: {str(e)}\n{traceback.format_exc()}")

@router.post("/validate")
async def validate_code(request: CodeValidateRequest):
    """Validate generated code syntax and security."""
    try:
        agent = get_autocoder_agent()
        is_valid, error = agent.sandbox.validate_code(request.code)
        
        return {
            "success": True,
            "is_valid": is_valid,
            "error": error
        }
    except Exception as e:
        import traceback
        logger.exception("Autocoder validation failed")
        raise HTTPException(status_code=500, detail=f"DEBUG ERROR [validate]: {str(e)}\n{traceback.format_exc()}")

@router.post("/execute")
async def execute_code(request: CodeValidateRequest):
    """Execute code in the sandboxed environment."""
    try:
        agent = get_autocoder_agent()
        exec_result = await agent.sandbox.execute(request.code)
        
        return {
            "success": getattr(exec_result, 'success', False),
            "output": getattr(exec_result, 'output', ""),
            "error": getattr(exec_result, 'error', None),
            "execution_time_ms": getattr(exec_result, 'execution_time_ms', 0)
        }
    except Exception as e:
        import traceback
        logger.exception("Autocoder execution failed")
        raise HTTPException(status_code=500, detail=f"DEBUG ERROR [execute]: {str(e)}\n{traceback.format_exc()}")
