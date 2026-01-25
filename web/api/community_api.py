"""
==============================================================================
FILE: web/api/community_api.py
ROLE: Community Forum API Endpoints
PURPOSE: REST endpoints for forums and expert Q&A.

INTEGRATION POINTS:
    - ForumService: Thread management
    - ExpertQAService: Q&A system
    - FrontendCommunity: Forum widgets

ENDPOINTS:
    - POST /api/forum/thread/create
    - GET /api/forum/threads
    - POST /api/forum/thread/:thread_id/reply
    - POST /api/forum/thread/:thread_id/upvote
    - POST /api/qa/question/create
    - POST /api/qa/question/:question_id/best-answer

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.community.forum_service import get_forum_service
from services.community.expert_qa_service import get_expert_qa_service

logger = logging.getLogger(__name__)

forum_bp = Blueprint('forum', __name__, url_prefix='/api/forum')
qa_bp = Blueprint('qa', __name__, url_prefix='/api/qa')


@forum_bp.route('/thread/create', methods=['POST'])
async def create_thread():
    """
    Create a new forum thread.
    
    Request body:
        user_id: User identifier
        category: Thread category
        title: Thread title
        content: Thread content
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        category = data.get('category')
        title = data.get('title')
        content = data.get('content')
        
        if not user_id or not category or not title or not content:
            return jsonify({
                'success': False,
                'error': 'user_id, category, title, and content are required'
            }), 400
        
        service = get_forum_service()
        thread = await service.create_thread(
            user_id=user_id,
            category=category,
            title=title,
            content=content
        )
        
        return jsonify({
            'success': True,
            'data': thread.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating thread: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@forum_bp.route('/threads', methods=['GET'])
async def get_threads():
    """
    Get forum threads.
    
    Query params:
        category: Optional category filter
        limit: Maximum number of threads (default: 50)
        sort_by: Sort method (default: recent)
    """
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 50))
        sort_by = request.args.get('sort_by', 'recent')
        
        service = get_forum_service()
        threads = await service.get_threads(category, limit, sort_by)
        
        return jsonify({
            'success': True,
            'data': [t.dict() for t in threads]
        })
        
    except Exception as e:
        logger.error(f"Error getting threads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@forum_bp.route('/thread/<thread_id>/reply', methods=['POST'])
async def add_reply(thread_id: str):
    """
    Add reply to thread.
    
    Request body:
        user_id: User identifier
        content: Reply content
        parent_reply_id: Optional parent reply for nesting
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        content = data.get('content')
        parent_reply_id = data.get('parent_reply_id')
        
        if not user_id or not content:
            return jsonify({
                'success': False,
                'error': 'user_id and content are required'
            }), 400
        
        service = get_forum_service()
        reply = await service.add_reply(
            thread_id=thread_id,
            user_id=user_id,
            content=content,
            parent_reply_id=parent_reply_id
        )
        
        return jsonify({
            'success': True,
            'data': reply.dict()
        })
        
    except Exception as e:
        logger.error(f"Error adding reply: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@forum_bp.route('/thread/<thread_id>/upvote', methods=['POST'])
async def upvote_thread(thread_id: str):
    """
    Upvote a thread.
    """
    try:
        service = get_forum_service()
        thread = await service.upvote_thread(thread_id)
        
        return jsonify({
            'success': True,
            'data': thread.dict()
        })
        
    except Exception as e:
        logger.error(f"Error upvoting thread: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@qa_bp.route('/question/create', methods=['POST'])
async def create_question():
    """
    Create an expert question.
    
    Request body:
        user_id: User identifier
        title: Question title
        content: Question content
        category: Question category
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        title = data.get('title')
        content = data.get('content')
        category = data.get('category')
        
        if not user_id or not title or not content or not category:
            return jsonify({
                'success': False,
                'error': 'user_id, title, content, and category are required'
            }), 400
        
        service = get_expert_qa_service()
        question = await service.create_question(
            user_id=user_id,
            title=title,
            content=content,
            category=category
        )
        
        return jsonify({
            'success': True,
            'data': question.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating question: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@qa_bp.route('/question/<question_id>/best-answer', methods=['POST'])
async def mark_best_answer(question_id: str):
    """
    Mark best answer for question.
    
    Request body:
        answer_id: Answer identifier
    """
    try:
        data = request.get_json() or {}
        answer_id = data.get('answer_id')
        
        if not answer_id:
            return jsonify({
                'success': False,
                'error': 'answer_id is required'
            }), 400
        
        service = get_expert_qa_service()
        question = await service.mark_best_answer(question_id, answer_id)
        
        return jsonify({
            'success': True,
            'data': question.dict()
        })
        
    except Exception as e:
        logger.error(f"Error marking best answer: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
