"""
Tests for Community Forum API Endpoints
Phase 20: Community Forums & Discussion
"""

import pytest
from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from web.api.community_api import router, get_forum_service, get_expert_qa_service
from web.auth_utils import get_current_user


@pytest.fixture
def api_app(mock_forum_service, mock_qa_service):
    """Create FastAPI app for testing."""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_forum_service] = lambda: mock_forum_service
    app.dependency_overrides[get_expert_qa_service] = lambda: mock_qa_service
    app.dependency_overrides[get_current_user] = lambda: {"id": "user_1", "role": "user"}
    return app


@pytest.fixture
def client(api_app):
    """Create test client."""
    return TestClient(api_app)


@pytest.fixture
def mock_forum_service():
    """Mock ForumService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_qa_service():
    """Mock ExpertQAService."""
    service = AsyncMock()
    return service


def test_create_thread_success(client, mock_forum_service):
    """Test successful thread creation."""
    from schemas.community import ForumThread, ThreadCategory
    from datetime import datetime, timezone
    
    mock_thread = ForumThread(
        thread_id='thread_1',
        user_id='user_1',
        category=ThreadCategory.GENERAL,
        title='Test Thread',
        content='Test content',
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_forum_service.create_thread.return_value = mock_thread
    
    response = client.post('/api/v1/community/thread/create',
                          json={
                              'user_id': 'user_1',
                              'category': 'general',
                              'title': 'Test Thread',
                              'content': 'Test content'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert data['data']['title'] == 'Test Thread'


def test_create_thread_missing_params(client):
    """Test thread creation with missing parameters."""
    response = client.post('/api/v1/community/thread/create',
                          json={'user_id': 'user_1', 'title': 'Test'})
    
    # Pydantic validation error
    assert response.status_code in [400, 422]


def test_get_threads_success(client, mock_forum_service):
    """Test successful threads retrieval."""
    from schemas.community import ForumThread, ThreadCategory
    from datetime import datetime, timezone
    
    mock_threads = [
        ForumThread(
            thread_id='thread_1',
            user_id='user_1',
            category=ThreadCategory.GENERAL,
            title='Test Thread',
            content='Test content',
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
    ]
    mock_forum_service.get_threads.return_value = mock_threads
    
    response = client.get('/api/v1/community/threads?limit=20')
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert len(data['data']) == 1


def test_create_question_success(client, mock_qa_service):
    """Test successful question creation."""
    from schemas.community import ExpertQuestion
    from datetime import datetime, timezone
    
    mock_question = ExpertQuestion(
        question_id='q_1',
        user_id='user_1',
        title='Test Question',
        content='Test question content',
        category='investment',
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_qa_service.create_question.return_value = mock_question
    
    response = client.post('/api/v1/community/question/create',
                          json={
                              'user_id': 'user_1',
                              'title': 'Test Question',
                              'content': 'Test question content',
                              'category': 'investment'
                          })
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
