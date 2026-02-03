"""
==============================================================================
FILE: web/api/education_api.py
ROLE: Education API Endpoints
PURPOSE: REST endpoints for learning management and content delivery.

INTEGRATION POINTS:
    - LearningManagementService: Course management
    - ContentManagementService: Content delivery
    - FrontendEducation: Learning dashboard

ENDPOINTS:
    - POST /api/education/course/create
    - GET /api/education/courses
    - POST /api/education/enroll
    - PUT /api/education/enrollment/:enrollment_id/progress
    - POST /api/education/enrollment/:enrollment_id/certificate

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
import logging
from services.education.learning_management_service import get_learning_management_service
from services.education.content_management_service import get_content_management_service

logger = logging.getLogger(__name__)

education_bp = Blueprint('education', __name__, url_prefix='/api/v1/education')


@education_bp.route('/course/create', methods=['POST'])
async def create_course():
    """
    Create a new course.
    
    Request body:
        title: Course title
        description: Course description
        instructor: Instructor name
        category: Course category
        difficulty: Difficulty level
        duration_hours: Course duration
        lessons: Optional list of lessons
    """
    try:
        data = request.get_json() or {}
        title = data.get('title')
        description = data.get('description')
        instructor = data.get('instructor')
        category = data.get('category')
        difficulty = data.get('difficulty')
        duration_hours = float(data.get('duration_hours', 0))
        lessons = data.get('lessons')
        
        if not all([title, description, instructor, category, difficulty]):
            return jsonify({
                'success': False,
                'error': 'title, description, instructor, category, and difficulty are required'
            }), 400
        
        service = get_learning_management_service()
        course = await service.create_course(
            title=title,
            description=description,
            instructor=instructor,
            category=category,
            difficulty=difficulty,
            duration_hours=duration_hours,
            lessons=lessons
        )
        
        return jsonify({
            'success': True,
            'data': course.dict()
        })
        
    except Exception as e:
        logger.error(f"Error creating course: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@education_bp.route('/courses', methods=['GET'])
async def get_courses():
    """
    Get available courses.
    
    Query params:
        category: Optional category filter
        difficulty: Optional difficulty filter
    """
    try:
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        
        # In production, would query database
        return jsonify({
            'success': True,
            'data': []
        })
        
    except Exception as e:
        logger.error(f"Error getting courses: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@education_bp.route('/enroll', methods=['POST'])
async def enroll_user():
    """
    Enroll user in course.
    
    Request body:
        user_id: User identifier
        course_id: Course identifier
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        
        if not user_id or not course_id:
            return jsonify({
                'success': False,
                'error': 'user_id and course_id are required'
            }), 400
        
        service = get_learning_management_service()
        enrollment = await service.enroll_user(user_id, course_id)
        
        return jsonify({
            'success': True,
            'data': enrollment.dict()
        })
        
    except Exception as e:
        logger.error(f"Error enrolling user: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@education_bp.route('/enrollment/<enrollment_id>/progress', methods=['PUT'])
async def update_progress(enrollment_id: str):
    """
    Update course progress.
    
    Request body:
        lesson_id: Completed lesson identifier
    """
    try:
        data = request.get_json() or {}
        lesson_id = data.get('lesson_id')
        
        if not lesson_id:
            return jsonify({
                'success': False,
                'error': 'lesson_id is required'
            }), 400
        
        service = get_learning_management_service()
        enrollment = await service.update_progress(enrollment_id, lesson_id)
        
        return jsonify({
            'success': True,
            'data': enrollment.dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating progress: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@education_bp.route('/enrollment/<enrollment_id>/certificate', methods=['POST'])
async def issue_certificate(enrollment_id: str):
    """
    Issue completion certificate.
    """
    try:
        service = get_learning_management_service()
        certificate = await service.issue_certificate(enrollment_id)
        
        return jsonify({
            'success': True,
            'data': certificate.dict()
        })
        
    except Exception as e:
        logger.error(f"Error issuing certificate: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
