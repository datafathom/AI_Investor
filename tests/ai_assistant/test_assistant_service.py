"""
Tests for AI Assistant Service
Comprehensive test coverage for conversational AI and personalized responses
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.ai_assistant.assistant_service import AssistantService
from models.ai_assistant import Conversation, ConversationMessage, MessageRole


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.ai_assistant.assistant_service.get_learning_service'), \
         patch('services.ai_assistant.assistant_service.get_cache_service'):
        return AssistantService()


@pytest.mark.asyncio
async def test_create_conversation(service):
    """Test conversation creation."""
    service._save_conversation = AsyncMock()
    
    result = await service.create_conversation(
        user_id="user_123",
        title="Investment Advice"
    )
    
    assert result is not None
    assert isinstance(result, Conversation)
    assert result.user_id == "user_123"
    assert result.title == "Investment Advice"


@pytest.mark.asyncio
async def test_send_message(service):
    """Test sending message to assistant."""
    conversation = Conversation(
        conversation_id="conv_123",
        user_id="user_123",
        messages=[],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_conversation = AsyncMock(return_value=conversation)
    service._generate_response = AsyncMock(return_value="Here's some investment advice...")
    service._save_conversation = AsyncMock()
    
    result = await service.send_message(
        conversation_id="conv_123",
        user_message="What should I invest in?"
    )
    
    assert result is not None
    assert isinstance(result, ConversationMessage) or isinstance(result, dict)
    assert 'content' in str(result) or hasattr(result, 'content')


@pytest.mark.asyncio
async def test_get_conversation_history(service):
    """Test getting conversation history."""
    conversation = Conversation(
        conversation_id="conv_123",
        user_id="user_123",
        messages=[
            ConversationMessage(
                message_id="msg_1",
                role=MessageRole.USER,
                content="What should I invest in?",
                timestamp=datetime.utcnow()
            ),
            ConversationMessage(
                message_id="msg_2",
                role=MessageRole.ASSISTANT,
                content="Here's some advice...",
                timestamp=datetime.utcnow()
            )
        ],
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_conversation = AsyncMock(return_value=conversation)
    
    result = await service.get_conversation_history("conv_123")
    
    assert result is not None
    assert len(result.messages) == 2