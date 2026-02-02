"""
==============================================================================
FILE: services/ai_assistant/assistant_service.py
ROLE: Personalized AI Assistant
PURPOSE: Provides conversational AI assistant with personalized investment
         advice, question answering, and preference learning.

INTEGRATION POINTS:
    - AIService: LLM access (OpenAI, Anthropic)
    - UserService: User preferences and history
    - PortfolioService: Portfolio context
    - ConversationService: Conversation history
    - AssistantAPI: Assistant endpoints

FEATURES:
    - Natural language understanding
    - Context-aware responses
    - Personalized recommendations
    - Learning from interactions

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.ai_assistant import Conversation, ConversationMessage, MessageRole
from services.ai_assistant.learning_service import get_learning_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class AssistantService:
    """
    Service for AI assistant conversations.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.learning_service = get_learning_service()
        self.cache_service = get_cache_service()
        
    async def create_conversation(
        self,
        user_id: str,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            user_id: User identifier
            title: Optional conversation title
            
        Returns:
            Conversation object
        """
        logger.info(f"Creating conversation for user {user_id}")
        
        conversation = Conversation(
            conversation_id=f"conv_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            title=title,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        
        # Save conversation
        await self._save_conversation(conversation)
        
        return conversation
    
    async def send_message(
        self,
        conversation_id: str,
        user_message: str
    ) -> ConversationMessage:
        """
        Send message and get AI response.
        
        Args:
            conversation_id: Conversation identifier
            user_message: User message content
            
        Returns:
            Assistant response message
        """
        logger.info(f"Sending message to conversation {conversation_id}")
        
        # Get conversation
        conversation = await self._get_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Add user message
        user_msg = ConversationMessage(
            message_id=f"msg_{conversation_id}_{datetime.utcnow().timestamp()}",
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=user_message,
            timestamp=datetime.utcnow()
        )
        conversation.messages.append(user_msg)
        
        # Get user preferences for context
        preferences = await self.learning_service.get_user_preferences(conversation.user_id)
        
        # Generate AI response (simplified - would use LLM)
        assistant_response = await self._generate_response(
            user_message,
            conversation,
            preferences
        )
        
        # Add assistant message
        assistant_msg = ConversationMessage(
            message_id=f"msg_{conversation_id}_{datetime.utcnow().timestamp()}",
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=assistant_response,
            timestamp=datetime.utcnow()
        )
        conversation.messages.append(assistant_msg)
        
        # Update conversation
        conversation.updated_date = datetime.utcnow()
        await self._save_conversation(conversation)
        
        # Learn from interaction
        await self.learning_service.learn_from_interaction(
            conversation.user_id,
            user_message,
            assistant_response
        )
        
        return assistant_msg
    
    async def get_conversation_history(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get conversation history.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation with all messages
        """
        logger.info(f"Getting history for conversation {conversation_id}")
        return await self._get_conversation(conversation_id)
    
    async def _generate_response(
        self,
        user_message: str,
        conversation: Conversation,
        preferences: List[Dict]
    ) -> str:
        """
        Generate AI response (simplified).
        
        In production, would use LLM (OpenAI, Anthropic) with:
        - Conversation history
        - User preferences
        - Portfolio context
        """
        # Simplified response generation
        response = f"I understand you're asking about: {user_message[:50]}... "
        response += "Based on your preferences and portfolio, I recommend reviewing your investment strategy."
        
        return response
    
    async def _get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation from cache."""
        cache_key = f"conversation:{conversation_id}"
        conv_data = self.cache_service.get(cache_key)
        if conv_data:
            return Conversation(**conv_data)
        return None
    
    async def _save_conversation(self, conversation: Conversation):
        """Save conversation to cache."""
        cache_key = f"conversation:{conversation.conversation_id}"
        self.cache_service.set(cache_key, conversation.dict(), ttl=86400 * 365)


# Singleton instance
_assistant_service: Optional[AssistantService] = None


def get_assistant_service() -> AssistantService:
    """Get singleton assistant service instance."""
    global _assistant_service
    if _assistant_service is None:
        _assistant_service = AssistantService()
    return _assistant_service
