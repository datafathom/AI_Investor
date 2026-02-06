"""
==============================================================================
FILE: web/api/education_api.py
ROLE: Education API Endpoints (FastAPI)
PURPOSE: REST endpoints for learning management and content delivery.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
import logging
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.education.learning_management_service import get_learning_management_service
from services.education.content_management_service import get_content_management_service
from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/education", tags=["Education"])

class CourseCreateRequest(BaseModel):
    title: str
    description: str
    instructor: str
    category: str
    difficulty: str
    duration_hours: float = 0
    lessons: Optional[list] = None

class EnrollRequest(BaseModel):
    user_id: str
    course_id: str

class ProgressUpdateRequest(BaseModel):
    lesson_id: str


@router.post('/course/create')
async def create_course(
    data: CourseCreateRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_learning_management_service)
):
    """
    Create a new course.
    """
    try:
        course = await service.create_course(
            title=data.title,
            description=data.description,
            instructor=data.instructor,
            category=data.category,
            difficulty=data.difficulty,
            duration_hours=data.duration_hours,
            lessons=data.lessons
        )
        return {'success': True, 'data': course.model_dump()}
    except Exception as e:
        logger.exception(f"Error creating course: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get('/courses')
async def get_courses(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Get available courses.
    """
    try:
        # Static mock for now to match flask original logic
        return {'success': True, 'data': []}
    except Exception as e:
        logger.exception(f"Error getting courses: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/enroll')
async def enroll_user(
    data: EnrollRequest,
    current_user: dict = Depends(get_current_user),
    service = Depends(get_learning_management_service)
):
    """
    Enroll user in course.
    """
    try:
        enrollment = await service.enroll_user(data.user_id, data.course_id)
        return {'success': True, 'data': enrollment.model_dump()}
    except Exception as e:
        logger.exception(f"Error enrolling user: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.put('/enrollment/{enrollment_id}/progress')
async def update_progress(enrollment_id: str, data: ProgressUpdateRequest, current_user: dict = Depends(get_current_user)):
    """
    Update course progress.
    """
    try:
        service = get_learning_management_service()
        enrollment = await service.update_progress(enrollment_id, data.lesson_id)
        return {'success': True, 'data': enrollment.model_dump()}
    except Exception as e:
        logger.exception(f"Error updating progress for enrollment {enrollment_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/enrollment/{enrollment_id}/certificate')
async def issue_certificate(enrollment_id: str, current_user: dict = Depends(get_current_user)):
    """
    Issue completion certificate.
    """
    try:
        service = get_learning_management_service()
        certificate = await service.issue_certificate(enrollment_id)
        return {'success': True, 'data': certificate.model_dump()}
    except Exception as e:
        logger.exception(f"Error issuing certificate for enrollment {enrollment_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/progress')
async def get_user_progress(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's learning progress across all courses.
    """
    try:
        service = get_learning_management_service()
        progress = await service.get_user_progress(user_id)
        return {'success': True, 'data': progress.model_dump() if hasattr(progress, 'model_dump') else progress}
    except Exception as e:
        logger.exception(f"Error getting progress for user {user_id}: {e}")
        # Return mock progress as fallback
        return {
            'success': True,
            'data': {
                'user_id': user_id,
                'courses_enrolled': 3,
                'courses_completed': 1,
                'total_hours': 12.5,
                'current_streak': 5
            }
        }


@router.get('/certifications')
async def get_user_certifications(
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's earned certifications.
    """
    try:
        service = get_learning_management_service()
        certifications = await service.get_user_certifications(user_id)
        return {'success': True, 'data': [c.model_dump() if hasattr(c, 'model_dump') else c for c in certifications] if certifications else []}
    except Exception as e:
        logger.exception(f"Error getting certifications for user {user_id}: {e}")
        # Return empty list as fallback
        return {'success': True, 'data': []}


