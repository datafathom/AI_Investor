"""
AI Assistant API - FastAPI Router
REST endpoints for AI assistant conversations and recommendations.
"""

import logging
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from web.auth_utils import get_current_user
from services.ai_assistant.assistant_service import get_assistant_service
from services.ai_assistant.learning_service import get_learning_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai_assistant", tags=["AI Assistant"])

# --- Request Models ---

class ConversationCreateRequest(BaseModel):
    user_id: str
    title: Optional[str] = None

class MessageRequest(BaseModel):
    message: str

# --- Endpoints ---

@router.post('/conversation/create')
async def create_conversation(
    request_data: ConversationCreateRequest,
    service = Depends(get_assistant_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new conversation."""
    try:
        conversation = await service.create_conversation(request_data.user_id, request_data.title)
        
        return {
            'success': True,
            'data': conversation.model_dump()
        }
    except Exception as e:
        logger.error(f"Error creating/getting/sending: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/conversation/{conversation_id}')
async def get_conversation(
    conversation_id: str,
    service = Depends(get_assistant_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get conversation details."""
    try:
        conversation = await service._get_conversation(conversation_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            'success': True,
            'data': conversation.model_dump()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.post('/conversation/{conversation_id}/message')
async def send_message(
    conversation_id: str,
    request_data: MessageRequest,
    service = Depends(get_assistant_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Send message and get AI response."""
    try:
        response = await service.send_message(conversation_id, request_data.message)
        
        return {
            'success': True,
            'data': response.model_dump()
        }
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

@router.get('/recommendations/{user_id}')
async def get_recommendations(
    user_id: str,
    service = Depends(get_learning_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get personalized recommendations."""
    try:
        recommendations = await service.generate_recommendations(user_id)
        
        return {
            'success': True,
            'data': [r.model_dump() for r in recommendations]
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
