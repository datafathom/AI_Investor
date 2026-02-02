"""
Tests for AI Assistant Learning Service
Comprehensive test coverage for preference learning and recommendation engine
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.ai_assistant.learning_service import LearningService
from models.ai_assistant import UserPreference, Recommendation


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.ai_assistant.learning_service.get_cache_service'):
        return LearningService()


@pytest.mark.asyncio
async def test_update_user_preferences(service):
    """Test updating user preferences."""
    service._save_preferences = AsyncMock()
    
    preferences = {
        'risk_tolerance': 'moderate',
        'investment_style': 'growth'
    }
    
    result = await service.update_user_preferences(
        user_id="user_123",
        preferences=preferences
    )
    
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], UserPreference)


@pytest.mark.asyncio
async def test_get_recommendations(service):
    """Test getting personalized recommendations."""
    # service.get_recommendations calls generate_recommendations
    # which is already partially implemented with mocks in the service
    
    result = await service.get_recommendations("user_123")
    
    assert result is not None
    assert len(result) > 0
    assert isinstance(result[0], Recommendation)