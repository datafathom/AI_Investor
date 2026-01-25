"""
Tests for Credit Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.credit import (
    CreditFactor,
    CreditScore,
    CreditRecommendation,
    CreditProjection
)


class TestCreditFactorEnum:
    """Tests for CreditFactor enum."""
    
    def test_credit_factor_enum(self):
        """Test credit factor enum values."""
        assert CreditFactor.PAYMENT_HISTORY == "payment_history"
        assert CreditFactor.CREDIT_UTILIZATION == "credit_utilization"
        assert CreditFactor.LENGTH_OF_HISTORY == "length_of_history"


class TestCreditScore:
    """Tests for CreditScore model."""
    
    def test_valid_credit_score(self):
        """Test valid credit score creation."""
        score = CreditScore(
            score_id='score_1',
            user_id='user_1',
            score=750,
            score_type='fico',
            factors={'payment_history': 0.9, 'credit_utilization': 0.8},
            report_date=datetime.now(),
            trend='increasing'
        )
        assert score.score_id == 'score_1'
        assert score.score == 750
        assert score.trend == 'increasing'
    
    def test_credit_score_range_validation(self):
        """Test credit score range validation."""
        # Should fail if score < 300
        with pytest.raises(ValidationError):
            CreditScore(
                score_id='score_1',
                user_id='user_1',
                score=250,
                score_type='fico',
                report_date=datetime.now()
            )
        
        # Should fail if score > 850
        with pytest.raises(ValidationError):
            CreditScore(
                score_id='score_1',
                user_id='user_1',
                score=900,
                score_type='fico',
                report_date=datetime.now()
            )


class TestCreditRecommendation:
    """Tests for CreditRecommendation model."""
    
    def test_valid_credit_recommendation(self):
        """Test valid credit recommendation creation."""
        recommendation = CreditRecommendation(
            recommendation_id='rec_1',
            factor=CreditFactor.CREDIT_UTILIZATION,
            title='Reduce Credit Utilization',
            description='Pay down credit card balances',
            impact_score=20,
            difficulty='medium',
            estimated_time='3 months',
            action_items=['Pay $500/month', 'Keep utilization below 30%']
        )
        assert recommendation.recommendation_id == 'rec_1'
        assert recommendation.impact_score == 20
        assert recommendation.factor == CreditFactor.CREDIT_UTILIZATION


class TestCreditProjection:
    """Tests for CreditProjection model."""
    
    def test_valid_credit_projection(self):
        """Test valid credit projection creation."""
        projection = CreditProjection(
            projection_id='proj_1',
            current_score=720,
            projected_score=750,
            projected_date=datetime(2025, 6, 1),
            assumptions={'pay_down_debt': True},
            confidence_level=0.85
        )
        assert projection.projection_id == 'proj_1'
        assert projection.current_score == 720
        assert projection.projected_score == 750
        assert projection.confidence_level == 0.85
