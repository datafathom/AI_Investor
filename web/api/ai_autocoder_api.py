"""
==============================================================================
FILE: web/api/ai_autocoder_api.py
ROLE: AI Autocoder REST API (FastAPI)
PURPOSE: RESTful endpoints for OpenAI-powered code generation and execution.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Body, Query, Depends
from pydantic import BaseModel
import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai/autocoder", tags=["AI Autocoder"])


class GenerateCodeRequest(BaseModel):
    prompt: str
    context: Dict[str, Any] = {}
    execute: bool = False


class ExecuteCodeRequest(BaseModel):
    code: str
    context: Dict[str, Any] = {}


def _get_autocoder_agent():
    """Lazy-load Autocoder agent."""
    from agents.autocoder_agent import get_autocoder_agent
    return get_autocoder_agent()


def _build_response(data: Any, meta: Optional[Dict] = None) -> Dict[str, Any]:
    """Build standardized API response."""
    return {
        "data": data,
        "meta": meta or {
            "timestamp": datetime.now().isoformat(),
            "source": "autocoder_agent"
        },
        "errors": []
    }


def _build_error_response(error_code: str, message: str) -> Dict[str, Any]:
    """Build standardized error response."""
    return {
        "data": None,
        "meta": {},
        "errors": [{
            "error_code": error_code,
            "message": message,
            "vendor": "openai"
        }]
    }


@router.post('/generate')
async def generate_code(
    request_data: GenerateCodeRequest,
    agent: Any = Depends(_get_autocoder_agent)
):
    """
    Generate Python code from natural language prompt.
    """
    try:
        if not request_data.prompt.strip():
            raise HTTPException(
                status_code=400,
                detail=_build_error_response("MISSING_PROMPT", "Prompt is required")
            )
        
        result = await agent.generate_code(request_data.prompt, request_data.context, request_data.execute)
        
        if result.get('error'):
            raise HTTPException(
                status_code=500,
                detail=_build_error_response("GENERATION_FAILED", result['error'])
            )
        
        return _build_response({
            "code": result.get('code'),
            "model": result.get('model'),
            "tokens_used": result.get('tokens_used'),
            "execution_result": result.get('execution_result')
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Code generation failed")
        raise HTTPException(
            status_code=500,
            detail=_build_error_response("INTERNAL_ERROR", f"Failed to generate code: {str(e)}")
        )


@router.post('/execute')
async def execute_code(
    request_data: ExecuteCodeRequest,
    agent: Any = Depends(_get_autocoder_agent)
):
    """
    Execute Python code in sandboxed environment.
    """
    try:
        if not request_data.code.strip():
            raise HTTPException(
                status_code=400,
                detail=_build_error_response("MISSING_CODE", "Code is required")
            )
        
        exec_result = await agent.sandbox.execute(request_data.code, request_data.context)
        
        return _build_response({
            "success": getattr(exec_result, 'success', False),
            "output": getattr(exec_result, 'output', ""),
            "error": getattr(exec_result, 'error', None),
            "execution_time_ms": getattr(exec_result, 'execution_time_ms', 0)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Code execution failed")
        raise HTTPException(
            status_code=500,
            detail=_build_error_response("EXECUTION_ERROR", f"Failed to execute code: {str(e)}")
        )


@router.get('/status')
async def get_status(agent: Any = Depends(_get_autocoder_agent)):
    """
    Get Autocoder agent health status.
    """
    try:
        health = agent.health_check()
        
        return _build_response({
            "agent": health.get('agent', 'unknown'),
            "active": health.get('active', False),
            "provider": getattr(agent.model_config.provider, 'value', str(agent.model_config.provider)),
            "model": agent.model_config.model_id,
            "sandbox_timeout": agent.sandbox.timeout,
            "capabilities": [
                "code_generation",
                "code_execution",
                "ast_validation",
                "sandboxed_execution"
            ]
        })
        
    except Exception as e:
        logger.exception("Status check failed")
        raise HTTPException(
            status_code=500,
            detail=_build_error_response("STATUS_ERROR", f"Failed to get status: {str(e)}")
        )
