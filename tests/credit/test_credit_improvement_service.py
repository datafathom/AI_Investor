"""
Tests for Credit Improvement Service
Comprehensive test coverage for credit improvement recommendations
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.credit.credit_improvement_service import CreditImprovementService
from models.credit import CreditRecommendation, CreditProjection


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.credit.credit_improvement_service.get_credit_monitoring_service'), \
         patch('services.credit.credit_improvement_service.get_cache_service'):
        return CreditImprovementService()


@pytest.mark.asyncio
async def test_generate_recommendations(service):
    """Test generating credit improvement recommendations."""
    service.credit_monitoring.get_credit_history = AsyncMock(return_value=[])
    service._analyze_credit_factors = AsyncMock(return_value={
        'payment_history': 'needs_improvement',
        'credit_utilization': 'high',
        'credit_age': 'good'
    })
    service._generate_recommendations_from_factors = AsyncMock(return_value=[
        CreditRecommendation(
            recommendation_id="rec_1",
            user_id="user_123",
            category="payment_history",
            action="Pay all bills on time",
            estimated_impact=20,
            priority=1
        )
    ])
    
    result = await service.generate_recommendations("user_123")
    
    assert result is not None
    assert len(result) > 0
    assert isinstance(result[0], CreditRecommendation)


@pytest.mark.asyncio
async def test_simulate_score_impact(service):
    """Test simulating credit score impact."""
    service._calculate_score_impact = AsyncMock(return_value={
        'current_score': 720,
        'projected_score': 750,
        'improvement': 30
    })
    
    result = await service.simulate_score_impact(
        user_id="user_123",
        actions=['pay_bills_on_time', 'reduce_utilization']
    )
    
    assert result is not None
    assert 'projected_score' in result or hasattr(result, 'projected_score')
