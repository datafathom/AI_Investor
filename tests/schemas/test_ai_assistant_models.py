"""
Tests for AI Assistant Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.ai_assistant import (
    MessageRole,
    ConversationMessage,
    Conversation,
    UserPreference,
    Recommendation
)


class TestMessageRoleEnum:
    """Tests for MessageRole enum."""
    
    def test_message_role_enum(self):
        """Test message role enum values."""
        assert MessageRole.USER == "user"
        assert MessageRole.ASSISTANT == "assistant"
        assert MessageRole.SYSTEM == "system"


class TestConversationMessage:
    """Tests for ConversationMessage model."""
    
    def test_valid_conversation_message(self):
        """Test valid conversation message creation."""
        message = ConversationMessage(
            message_id='msg_1',
            conversation_id='conv_1',
            role=MessageRole.USER,
            content='Hello, assistant!',
            timestamp=datetime.now(),
            metadata={}
        )
        assert message.message_id == 'msg_1'
        assert message.role == MessageRole.USER
        assert message.content == 'Hello, assistant!'


class TestConversation:
    """Tests for Conversation model."""
    
    def test_valid_conversation(self):
        """Test valid conversation creation."""
        conversation = Conversation(
            conversation_id='conv_1',
            user_id='user_1',
            title='Test Conversation',
            messages=[],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert conversation.conversation_id == 'conv_1'
        assert conversation.title == 'Test Conversation'
        assert len(conversation.messages) == 0
    
    def test_conversation_with_messages(self):
        """Test conversation with messages."""
        messages = [
            ConversationMessage(
                message_id='msg_1',
                conversation_id='conv_1',
                role=MessageRole.USER,
                content='Hello',
                timestamp=datetime.now()
            )
        ]
        conversation = Conversation(
            conversation_id='conv_1',
            user_id='user_1',
            messages=messages,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert len(conversation.messages) == 1


class TestUserPreference:
    """Tests for UserPreference model."""
    
    def test_valid_user_preference(self):
        """Test valid user preference creation."""
        preference = UserPreference(
            preference_id='pref_1',
            user_id='user_1',
            category='risk_tolerance',
            value='moderate',
            confidence=0.85,
            learned_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert preference.preference_id == 'pref_1'
        assert preference.confidence == 0.85
    
    def test_user_preference_confidence_validation(self):
        """Test user preference confidence validation."""
        # Should fail if confidence > 1
        with pytest.raises(ValidationError):
            UserPreference(
                preference_id='pref_1',
                user_id='user_1',
                category='risk_tolerance',
                value='moderate',
                confidence=1.5,
                learned_date=datetime.now(),
                updated_date=datetime.now()
            )


class TestRecommendation:
    """Tests for Recommendation model."""
    
    def test_valid_recommendation(self):
        """Test valid recommendation creation."""
        recommendation = Recommendation(
            recommendation_id='rec_1',
            user_id='user_1',
            recommendation_type='investment',
            title='Consider Rebalancing',
            description='Your portfolio is overweight in tech stocks',
            confidence=0.8,
            reasoning='Based on current market conditions',
            created_date=datetime.now()
        )
        assert recommendation.recommendation_id == 'rec_1'
        assert recommendation.confidence == 0.8
        assert recommendation.recommendation_type == 'investment'
