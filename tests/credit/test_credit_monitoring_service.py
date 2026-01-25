"""
Tests for Credit Monitoring Service
Comprehensive test coverage for credit score tracking and analysis
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.credit.credit_monitoring_service import CreditMonitoringService
from models.credit import CreditScore


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.credit.credit_monitoring_service.get_cache_service'):
        return CreditMonitoringService()


@pytest.mark.asyncio
async def test_track_credit_score(service):
    """Test credit score tracking."""
    service._get_latest_score = AsyncMock(return_value=None)
    service._save_score = AsyncMock()
    
    result = await service.track_credit_score(
        user_id="user_123",
        score=750,
        score_type="fico"
    )
    
    assert result is not None
    assert isinstance(result, CreditScore)
    assert result.user_id == "user_123"
    assert result.score == 750


@pytest.mark.asyncio
async def test_track_credit_score_with_trend(service):
    """Test credit score tracking with trend calculation."""
    previous_score = CreditScore(
        score_id="score_1",
        user_id="user_123",
        score=720,
        score_type="fico",
        trend="stable",
        recorded_date=datetime(2024, 1, 1)
    )
    
    service._get_latest_score = AsyncMock(return_value=previous_score)
    service._save_score = AsyncMock()
    
    result = await service.track_credit_score(
        user_id="user_123",
        score=750,  # Increased
        score_type="fico"
    )
    
    assert result is not None
    assert result.trend == "increasing"


@pytest.mark.asyncio
async def test_get_credit_history(service):
    """Test getting credit score history."""
    service._get_scores_from_db = AsyncMock(return_value=[
        CreditScore(
            score_id="score_1",
            user_id="user_123",
            score=720,
            score_type="fico",
            trend="stable",
            recorded_date=datetime(2024, 1, 1)
        ),
        CreditScore(
            score_id="score_2",
            user_id="user_123",
            score=750,
            score_type="fico",
            trend="increasing",
            recorded_date=datetime(2024, 2, 1)
        ),
    ])
    
    result = await service.get_credit_history("user_123", limit=10)
    
    assert result is not None
    assert len(result) == 2


@pytest.mark.asyncio
async def test_track_credit_score_error_handling(service):
    """Test error handling in credit score tracking."""
    service._get_latest_score = AsyncMock(side_effect=Exception("Database error"))
    
    with pytest.raises(Exception):
        await service.track_credit_score(
            user_id="user_123",
            score=750
        )
