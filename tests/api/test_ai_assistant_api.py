import pytest
from unittest.mock import AsyncMock, patch
from flask import Flask
from web.api.ai_assistant_api import ai_assistant_bp
from datetime import datetime, timezone


@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(ai_assistant_bp)
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_assistant_service():
    """Mock AssistantService."""
    with patch('web.api.ai_assistant_api.get_assistant_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


@pytest.fixture
def mock_learning_service():
    """Mock LearningService."""
    with patch('web.api.ai_assistant_api.get_learning_service') as mock:
        service = AsyncMock()
        mock.return_value = service
        yield service


def test_create_conversation_success(client, mock_assistant_service):
    """Test successful conversation creation."""
    from models.ai_assistant import Conversation
    from datetime import datetime
    mock_conversation = Conversation(
        conversation_id='conv_1',
        user_id='user_1',
        title='Test Conversation',
        messages=[],
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_assistant_service.create_conversation.return_value = mock_conversation
    
    response = client.post('/api/ai-assistant/conversation/create',
                          json={
                              'user_id': 'user_1',
                              'title': 'Test Conversation'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['conversation_id'] == 'conv_1'


def test_create_conversation_missing_user_id(client):
    """Test conversation creation without user_id."""
    response = client.post('/api/ai-assistant/conversation/create', json={})
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_get_conversation_success(client, mock_assistant_service):
    """Test successful conversation retrieval."""
    from models.ai_assistant import Conversation
    from datetime import datetime
    mock_conversation = Conversation(
        conversation_id='conv_1',
        user_id='user_1',
        title='Test Conversation',
        messages=[],
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    mock_assistant_service._get_conversation.return_value = mock_conversation
    
    response = client.get('/api/ai-assistant/conversation/conv_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_send_message_success(client, mock_assistant_service):
    """Test successful message sending."""
    from models.ai_assistant import ConversationMessage
    
    from datetime import datetime
    mock_message = ConversationMessage(
        message_id='msg_1',
        conversation_id='conv_1',
        role='user',
        content='Test message',
        timestamp=datetime.now(timezone.utc)
    )
    mock_assistant_service.send_message.return_value = mock_message
    
    response = client.post('/api/ai-assistant/conversation/conv_1/message',
                          json={
                              'message': 'Test message'
                          })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True


def test_get_recommendations_success(client, mock_learning_service):
    """Test successful recommendations retrieval."""
    from models.ai_assistant import Recommendation
    
    from datetime import datetime
    mock_recommendations = [
        Recommendation(
            recommendation_id='rec_1',
            user_id='user_1',
            recommendation_type='portfolio_optimization',
            title='Portfolio Optimization',
            description='Consider rebalancing your portfolio',
            confidence=0.9,
            reasoning='Markets are volatile',
            created_date=datetime.now(timezone.utc)
        )
    ]
    mock_learning_service.get_recommendations.return_value = mock_recommendations
    
    response = client.get('/api/ai-assistant/recommendations/user_1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
