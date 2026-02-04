"""
==============================================================================
FILE: web/api/community_api.py
ROLE: Community Forum API Endpoints (FastAPI)
PURPOSE: REST endpoints for forums and expert Q&A.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.community.forum_service import get_forum_service
from services.community.expert_qa_service import get_expert_qa_service
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/community", tags=["Community"])

class ThreadCreateRequest(BaseModel):
    user_id: str
    category: str
    title: str
    content: str

class ReplyCreateRequest(BaseModel):
    user_id: str
    content: str
    parent_reply_id: Optional[str] = None

class QuestionCreateRequest(BaseModel):
    user_id: str
    title: str
    content: str
    category: str

class BestAnswerRequest(BaseModel):
    answer_id: str


@router.post('/thread/create')
async def create_thread(
    data: ThreadCreateRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_forum_service)
):
    """
    Create a new forum thread.
    """
    try:
        thread = await service.create_thread(
            user_id=data.user_id,
            category=data.category,
            title=data.title,
            content=data.content
        )
        return {'success': True, 'data': thread.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating thread: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get('/threads')
async def get_threads(
    category: Optional[str] = Query(None),
    limit: int = Query(50),
    sort_by: str = Query('recent'),
    current_user: dict = Depends(get_current_user),
    service = Depends(get_forum_service)
):
    """
    Get forum threads.
    """
    try:
        threads = await service.get_threads(category, limit, sort_by)
        return {'success': True, 'data': [t.model_dump() for t in threads]}
    except Exception as e:
        logger.exception(f"Error getting threads: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.post('/thread/{thread_id}/reply')
async def add_reply(thread_id: str, data: ReplyCreateRequest, current_user: dict = Depends(get_current_user)):
    """
    Add reply to thread.
    """
    try:
        service = get_forum_service()
        reply = await service.add_reply(
            thread_id=thread_id,
            user_id=data.user_id,
            content=data.content,
            parent_reply_id=data.parent_reply_id
        )
        return {'success': True, 'data': reply.model_dump()}
    except Exception as e:
        logger.exception(f"Error adding reply to thread {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/thread/{thread_id}/upvote')
async def upvote_thread(thread_id: str, current_user: dict = Depends(get_current_user)):
    """
    Upvote a thread.
    """
    try:
        service = get_forum_service()
        thread = await service.upvote_thread(thread_id)
        return {'success': True, 'data': thread.model_dump()}
    except Exception as e:
        logger.exception(f"Error upvoting thread {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/expert/questions')
async def get_expert_questions(
    user_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Get expert questions.
    """
    try:
        service = get_expert_qa_service()
        questions = await service.get_questions(user_id)
        return {'success': True, 'data': [q.model_dump() for q in questions]}
    except Exception as e:
        logger.exception(f"Error getting expert questions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/question/create')
async def create_question(
    data: QuestionCreateRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_expert_qa_service)
):
    # ... (same as before)
    """
    Create an expert question.
    """
    try:
        question = await service.create_question(
            user_id=data.user_id,
            title=data.title,
            content=data.content,
            category=data.category
        )
        return {'success': True, 'data': question.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating question: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.post('/qa/question/{question_id}/best-answer')
async def mark_best_answer(question_id: str, data: BestAnswerRequest, current_user: dict = Depends(get_current_user)):
    """
    Mark best answer for question.
    """
    try:
        service = get_expert_qa_service()
        question = await service.mark_best_answer(question_id, data.answer_id)
        return {'success': True, 'data': question.model_dump()}
    except Exception as e:
        logger.exception(f"Error marking best answer for question {question_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
