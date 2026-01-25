"""
Tests for Learning Management Service
Comprehensive test coverage for courses, enrollments, and progress tracking
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.education.learning_management_service import LearningManagementService
from models.education import Course, Enrollment, CourseStatus, Certificate


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.education.learning_management_service.get_cache_service'):
        return LearningManagementService()


@pytest.mark.asyncio
async def test_create_course(service):
    """Test course creation."""
    service._save_course = AsyncMock()
    
    result = await service.create_course(
        title="Introduction to Investing",
        description="Learn the basics of investing",
        instructor="John Doe",
        category="beginner",
        difficulty="beginner",
        duration_hours=5.0
    )
    
    assert result is not None
    assert isinstance(result, Course)
    assert result.title == "Introduction to Investing"
    assert result.difficulty == "beginner"


@pytest.mark.asyncio
async def test_enroll_in_course(service):
    """Test enrolling in a course."""
    course = Course(
        course_id="course_123",
        title="Test Course",
        description="Description",
        instructor="Instructor",
        category="category",
        difficulty="beginner",
        duration_hours=5.0,
        lessons=[],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_course = AsyncMock(return_value=course)
    service._save_enrollment = AsyncMock()
    
    result = await service.enroll_in_course(
        user_id="user_123",
        course_id="course_123"
    )
    
    assert result is not None
    assert isinstance(result, Enrollment)
    assert result.user_id == "user_123"
    assert result.course_id == "course_123"
    assert result.status == CourseStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_update_progress(service):
    """Test updating course progress."""
    enrollment = Enrollment(
        enrollment_id="enrollment_123",
        user_id="user_123",
        course_id="course_123",
        status=CourseStatus.IN_PROGRESS,
        progress_percentage=0.0,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_enrollment = AsyncMock(return_value=enrollment)
    service._save_enrollment = AsyncMock()
    
    result = await service.update_progress(
        enrollment_id="enrollment_123",
        progress_percentage=50.0
    )
    
    assert result is not None
    assert result.progress_percentage == 50.0


@pytest.mark.asyncio
async def test_get_user_courses(service):
    """Test getting user's enrolled courses."""
    service._get_enrollments = AsyncMock(return_value=[
        Enrollment(
            enrollment_id="enrollment_1",
            user_id="user_123",
            course_id="course_1",
            status=CourseStatus.IN_PROGRESS,
            progress_percentage=50.0,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
    ])
    
    result = await service.get_user_courses("user_123")
    
    assert result is not None
    assert len(result) == 1
