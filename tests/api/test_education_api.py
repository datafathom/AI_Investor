"""
Tests for Education API Endpoints
Phase 21: Education Platform & Learning Management
"""

import pytest
from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.education_api import router, get_learning_management_service, get_content_management_service
from web.auth_utils import get_current_user


@pytest.fixture
def api_app(mock_learning_management_service, mock_content_management_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_learning_management_service] = lambda: mock_learning_management_service
    app.dependency_overrides[get_content_management_service] = lambda: mock_content_management_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_learning_management_service():
    """Mock LearningManagementService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_content_management_service():
    """Mock ContentManagementService."""
    service = AsyncMock()
    return service


def test_create_course_success(client, mock_learning_management_service):
    """Test successful course creation."""
    from datetime import datetime, timezone
    from schemas.education import Course
    
    mock_course = Course(
        course_id='course_1',
        title='Test Course',
        description='Test description',
        instructor='Test Instructor',
        category='investing',
        difficulty='beginner',
        duration_hours=10.0,
        lessons=[],
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_learning_management_service.create_course.return_value = mock_course
    
    response = client.post('/api/v1/education/course/create',
                          json={
                              'title': 'Test Course',
                              'description': 'Test description',
                              'instructor': 'Test Instructor',
                              'category': 'investing',
                              'difficulty': 'beginner',
                              'duration_hours': 10.0
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['title'] == 'Test Course'


def test_create_course_missing_params(client):
    """Test course creation with missing parameters."""
    response = client.post('/api/v1/education/course/create',
                          json={'title': 'Test Course'})
    
    # Pydantic validation error
    assert response.status_code in [400, 422]


def test_enroll_in_course_success(client, mock_learning_management_service):
    """Test successful course enrollment."""
    from schemas.education import Enrollment, CourseStatus
    
    mock_enrollment = Enrollment(
        enrollment_id='enroll_1',
        user_id='user_1',
        course_id='course_1',
        progress_percentage=0.0,
        status=CourseStatus.IN_PROGRESS
    )
    mock_learning_management_service.enroll_user.return_value = mock_enrollment
    
    response = client.post('/api/v1/education/enroll',
                          json={
                              'user_id': 'user_1',
                              'course_id': 'course_1'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
