"""
Tests for Community Forum API Endpoints
Phase 20: Community Forums & Discussion
"""

import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.community_api import forum_bp, qa_bp


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(forum_bp)
    app.register_blueprint(qa_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_forum_service():
    """Mock ForumService."""
    with patch('web.api.community_api.get_forum_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_qa_service():
    """Mock ExpertQAService."""
    with patch('web.api.community_api.get_expert_qa_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.mark.asyncio
async def test_create_thread_success(client, mock_forum_service):
    """Test successful thread creation."""
    from models.community import ForumThread
    
    mock_thread = ForumThread(
        thread_id='thread_1',
        user_id='user_1',
        category='general',
        title='Test Thread',
        content='Test content'
    )
    mock_forum_service.create_thread.return_value = mock_thread
    
    response = client.post('/api/forum/thread/create',
                          json={
                              'user_id': 'user_1',
                              'category': 'general',
                              'title': 'Test Thread',
                              'content': 'Test content'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['title'] == 'Test Thread'


@pytest.mark.asyncio
async def test_create_thread_missing_params(client):
    """Test thread creation with missing parameters."""
    response = client.post('/api/forum/thread/create',
                          json={'user_id': 'user_1', 'title': 'Test'})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


@pytest.mark.asyncio
async def test_get_threads_success(client, mock_forum_service):
    """Test successful threads retrieval."""
    from models.community import ForumThread
    
    mock_threads = [
        ForumThread(
            thread_id='thread_1',
            user_id='user_1',
            category='general',
            title='Test Thread',
            content='Test content'
        )
    ]
    mock_forum_service.get_threads.return_value = mock_threads
    
    response = client.get('/api/forum/threads?limit=20')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1


@pytest.mark.asyncio
async def test_create_reply_success(client, mock_forum_service):
    """Test successful reply creation."""
    from models.community import Reply
    
    mock_reply = Reply(
        reply_id='reply_1',
        thread_id='thread_1',
        user_id='user_1',
        content='Test reply'
    )
    mock_forum_service.create_reply.return_value = mock_reply
    
    response = client.post('/api/forum/thread/thread_1/reply',
                          json={
                              'user_id': 'user_1',
                              'content': 'Test reply'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_upvote_thread_success(client, mock_forum_service):
    """Test successful thread upvote."""
    from models.community import ForumThread
    
    mock_thread = ForumThread(
        thread_id='thread_1',
        user_id='user_1',
        category='general',
        title='Test Thread',
        content='Test content',
        upvotes=1
    )
    mock_forum_service.upvote_thread.return_value = mock_thread
    
    response = client.post('/api/forum/thread/thread_1/upvote',
                          json={'user_id': 'user_1'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_create_question_success(client, mock_qa_service):
    """Test successful question creation."""
    from models.community import Question
    
    mock_question = Question(
        question_id='q_1',
        user_id='user_1',
        title='Test Question',
        content='Test question content',
        category='investment'
    )
    mock_qa_service.create_question.return_value = mock_question
    
    response = client.post('/api/qa/question/create',
                          json={
                              'user_id': 'user_1',
                              'title': 'Test Question',
                              'content': 'Test question content',
                              'category': 'investment'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


@pytest.mark.asyncio
async def test_mark_best_answer_success(client, mock_qa_service):
    """Test successful best answer marking."""
    from models.community import Question
    
    mock_question = Question(
        question_id='q_1',
        user_id='user_1',
        title='Test Question',
        content='Test question content',
        best_answer_id='answer_1'
    )
    mock_qa_service.mark_best_answer.return_value = mock_question
    
    response = client.post('/api/qa/question/q_1/best-answer',
                          json={'answer_id': 'answer_1'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
