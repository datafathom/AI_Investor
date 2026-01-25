"""
Tests for Education API Endpoints
Phase 21: Education Platform & Learning Management
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.education_api import education_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(education_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_learning_management_service():
    """Mock LearningManagementService."""
    with patch('web.api.education_api.get_learning_management_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_content_management_service():
    """Mock ContentManagementService."""
    with patch('web.api.education_api.get_content_management_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_course_success(client, mock_learning_management_service):
    """Test successful course creation."""
    from models.education import Course
    
    mock_course = Course(
        course_id='course_1',
        title='Test Course',
        description='Test description',
        instructor='Test Instructor',
        category='investing',
        difficulty='beginner',
        duration_hours=10.0
    )
    mock_learning_management_service.create_course.return_value = mock_course
    
    response = client.post('/api/education/course/create',
                          json={
                              'title': 'Test Course',
                              'description': 'Test description',
                              'instructor': 'Test Instructor',
                              'category': 'investing',
                              'difficulty': 'beginner',
                              'duration_hours': 10.0
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['title'] == 'Test Course'


@pytest.mark.asyncio
async def test_create_course_missing_params(client):
    """Test course creation with missing parameters."""
    response = client.post('/api/education/course/create',
                          json={'title': 'Test Course'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_enroll_in_course_success(client, mock_learning_management_service):
    """Test successful course enrollment."""
    from models.education import Enrollment
    
    mock_enrollment = Enrollment(
        enrollment_id='enroll_1',
        user_id='user_1',
        course_id='course_1',
        progress_percent=0.0,
        status='active'
    )
    mock_learning_management_service.enroll_user.return_value = mock_enrollment
    
    response = client.post('/api/education/enroll',
                          json={
                              'user_id': 'user_1',
                              'course_id': 'course_1'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
