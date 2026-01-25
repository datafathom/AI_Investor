"""
==============================================================================
FILE: web/api/ai_autocoder_api.py
ROLE: AI Autocoder REST API
PURPOSE: RESTful endpoints for OpenAI-powered code generation and execution.
         Integrates with AutocoderAgent for natural language to Python code.

INTEGRATION POINTS:
    - AutocoderAgent: Code generation and execution
    - OpenAIClient: GPT-4 completions
    - CommandChat.jsx: Frontend chat interface

ENDPOINTS:
    POST /api/v1/ai/autocoder/generate - Generate code from prompt
    POST /api/v1/ai/autocoder/execute - Execute generated code
    GET /api/v1/ai/autocoder/status - Agent health status

AUTHENTICATION: JWT Bearer token recommended
RATE LIMITING: Inherits from APIGovernor (OPENAI limits)

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

ai_autocoder_bp = Blueprint('ai_autocoder', __name__, url_prefix='/api/v1/ai/autocoder')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _get_autocoder_agent():
    """Lazy-load Autocoder agent."""
    from agents.autocoder_agent import get_autocoder_agent
    return get_autocoder_agent()


def _build_response(data: Any, meta: Optional[Dict] = None) -> Dict[str, Any]:
    """Build standardized API response."""
    return {
        "data": data,
        "meta": meta or {
            "timestamp": asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0,
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


# =============================================================================
# Generate Code Endpoint
# =============================================================================

@ai_autocoder_bp.route('/generate', methods=['POST'])
def generate_code():
    """
    Generate Python code from natural language prompt.
    
    Request Body:
        {
            "prompt": "Calculate moving average of AAPL prices",
            "context": {"symbol": "AAPL"},  # Optional
            "execute": false  # Whether to execute immediately
        }
    
    Returns:
        JSON with generated code and optional execution result
    """
    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        context = data.get('context', {})
        execute = data.get('execute', False)
        
        if not prompt:
            return jsonify(_build_error_response(
                "MISSING_PROMPT",
                "Prompt is required"
            )), 400
        
        agent = _get_autocoder_agent()
        result = _run_async(agent.generate_code(prompt, context, execute))
        
        if result.get('error'):
            return jsonify(_build_error_response(
                "GENERATION_FAILED",
                result['error']
            )), 500
        
        return jsonify(_build_response({
            "code": result.get('code'),
            "model": result.get('model'),
            "tokens_used": result.get('tokens_used'),
            "execution_result": result.get('execution_result')
        }))
        
    except Exception as e:
        logger.error(f"Code generation failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "INTERNAL_ERROR",
            f"Failed to generate code: {str(e)}"
        )), 500


# =============================================================================
# Execute Code Endpoint
# =============================================================================

@ai_autocoder_bp.route('/execute', methods=['POST'])
def execute_code():
    """
    Execute Python code in sandboxed environment.
    
    Request Body:
        {
            "code": "print('Hello, World!')",
            "context": {}  # Optional context variables
        }
    
    Returns:
        JSON with execution result (output, error, execution_time)
    """
    try:
        data = request.json or {}
        code = data.get('code', '').strip()
        context = data.get('context', {})
        
        if not code:
            return jsonify(_build_error_response(
                "MISSING_CODE",
                "Code is required"
            )), 400
        
        agent = _get_autocoder_agent()
        exec_result = _run_async(agent.sandbox.execute(code, context))
        
        return jsonify(_build_response({
            "success": exec_result.success,
            "output": exec_result.output,
            "error": exec_result.error,
            "execution_time_ms": exec_result.execution_time_ms
        }))
        
    except Exception as e:
        logger.error(f"Code execution failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "EXECUTION_ERROR",
            f"Failed to execute code: {str(e)}"
        )), 500


# =============================================================================
# Status Endpoint
# =============================================================================

@ai_autocoder_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get Autocoder agent health status.
    
    Returns:
        JSON with agent status and capabilities
    """
    try:
        agent = _get_autocoder_agent()
        health = agent.health_check()
        
        return jsonify(_build_response({
            "agent": health['agent'],
            "active": health['active'],
            "provider": agent.model_config.provider.value,
            "model": agent.model_config.model_id,
            "sandbox_timeout": agent.sandbox.timeout,
            "capabilities": [
                "code_generation",
                "code_execution",
                "ast_validation",
                "sandboxed_execution"
            ]
        }))
        
    except Exception as e:
        logger.error(f"Status check failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "STATUS_ERROR",
            f"Failed to get status: {str(e)}"
        )), 500
