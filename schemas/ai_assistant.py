"""
==============================================================================
FILE: models/ai_assistant.py
ROLE: AI Assistant Data Models
PURPOSE: Pydantic models for AI assistant conversations, preferences, and
         recommendations.

INTEGRATION POINTS:
    - AssistantService: Conversation management
    - LearningService: Preference learning
    - AssistantAPI: Assistant endpoints
    - FrontendAI: Chat interface

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class MessageRole(str, Enum):
    """Message roles in conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationMessage(BaseModel):
    """Conversation message."""
    message_id: str
    conversation_id: str
    role: MessageRole
    content: str
    timestamp: datetime
    metadata: Dict = {}


class Conversation(BaseModel):
    """Conversation definition."""
    conversation_id: str
    user_id: str
    title: Optional[str] = None
    messages: List[ConversationMessage] = []
    created_date: datetime
    updated_date: datetime


class UserPreference(BaseModel):
    """User preference for personalization."""
    preference_id: str
    user_id: str
    category: str  # risk_tolerance, investment_style, goals, etc.
    value: str
    confidence: float = Field(..., ge=0, le=1)
    learned_date: datetime
    updated_date: datetime


class Recommendation(BaseModel):
    """Personalized recommendation."""
    recommendation_id: str
    user_id: str
    recommendation_type: str  # investment, strategy, education, etc.
    title: str
    description: str
    confidence: float
    reasoning: str
    created_date: datetime
