"""
==============================================================================
FILE: web/api/ai_assistant_api.py
ROLE: AI Assistant API Endpoints
PURPOSE: REST endpoints for AI assistant conversations and recommendations.

INTEGRATION POINTS:
    - AssistantService: Conversation management
    - LearningService: Recommendations
    - FrontendAI: Chat interface

ENDPOINTS:
    - POST /api/ai-assistant/conversation/create
    - GET /api/ai-assistant/conversation/:conversation_id
    - POST /api/ai-assistant/conversation/:conversation_id/message
    - GET /api/ai-assistant/recommendations/:user_id

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.ai_assistant.assistant_service import get_assistant_service
from services.ai_assistant.learning_service import get_learning_service

logger = logging.getLogger(__name__)

ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/api/ai-assistant')


@ai_assistant_bp.route('/conversation/create', methods=['POST'])
async def create_conversation():
    """
    Create a new conversation.
    
    Request body:
        user_id: User identifier
        title: Optional conversation title
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        title = data.get('title')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        service = get_assistant_service()
        conversation = await service.create_conversation(user_id, title)
        
        return jsonify({
            'success': True,
            'data': conversation.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_assistant_bp.route('/conversation/<conversation_id>', methods=['GET'])
async def get_conversation(conversation_id: str):
    """
    Get conversation details.
    """
    try:
        service = get_assistant_service()
        conversation = await service._get_conversation(conversation_id)
        
        if not conversation:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': conversation.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_assistant_bp.route('/conversation/<conversation_id>/message', methods=['POST'])
async def send_message(conversation_id: str):
    """
    Send message and get AI response.
    
    Request body:
        message: User message content
    """
    try:
        data = request.get_json() or {}
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'message is required'
            }), 400
        
        service = get_assistant_service()
        response = await service.send_message(conversation_id, user_message)
        
        return jsonify({
            'success': True,
            'data': response.model_dump()
        })
        
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_assistant_bp.route('/recommendations/<user_id>', methods=['GET'])
async def get_recommendations(user_id: str):
    """
    Get personalized recommendations.
    """
    try:
        service = get_learning_service()
        recommendations = await service.generate_recommendations(user_id)
        
        return jsonify({
            'success': True,
            'data': [r.model_dump() for r in recommendations]
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
