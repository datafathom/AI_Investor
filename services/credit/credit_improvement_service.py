"""
==============================================================================
FILE: services/credit/credit_improvement_service.py
ROLE: Credit Improvement Engine
PURPOSE: Provides actionable recommendations, score simulation, and improvement
         tracking for credit score enhancement.

INTEGRATION POINTS:
    - CreditMonitoringService: Current credit score
    - CreditReportService: Credit report data
    - CreditImprovementAPI: Improvement endpoints
    - FrontendCredit: Improvement dashboard

FEATURES:
    - Actionable recommendations
    - Score simulation
    - Improvement tracking
    - Personalized advice

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from models.credit import (
    CreditScore, CreditRecommendation, CreditProjection, CreditFactor
)
from services.credit.credit_monitoring_service import get_credit_monitoring_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class CreditImprovementService:
    """
    Service for credit improvement recommendations and projections.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.credit_monitoring = get_credit_monitoring_service()
        self.cache_service = get_cache_service()
        
    async def generate_recommendations(
        self,
        user_id: str
    ) -> List[CreditRecommendation]:
        """
        Generate credit improvement recommendations.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of CreditRecommendation objects
        """
        logger.info(f"Generating credit recommendations for user {user_id}")
        
        # Get current score and factors
        score = await self.credit_monitoring._get_latest_score(user_id)
        if not score:
            score = CreditScore(
                score_id="default",
                user_id=user_id,
                score=650,  # Default
                report_date=datetime.now(timezone.utc)
            )
        
        factors = await self.credit_monitoring.analyze_credit_factors(user_id)
        
        recommendations = []
        
        # Payment history recommendations
        if score.score < 700:
            recommendations.append(CreditRecommendation(
                recommendation_id=f"rec_{user_id}_payment",
                factor=CreditFactor.PAYMENT_HISTORY,
                title="Improve Payment History",
                description="Make all payments on time. Set up automatic payments to avoid missed payments.",
                impact_score=20,
                difficulty="easy",
                estimated_time="3 months",
                action_items=[
                    "Set up automatic payments for all bills",
                    "Pay at least minimum balance on time",
                    "Contact creditors if you miss a payment"
                ]
            ))
        
        # Credit utilization recommendations
        if factors.get(CreditFactor.CREDIT_UTILIZATION.value, 0) > 0.3:
            recommendations.append(CreditRecommendation(
                recommendation_id=f"rec_{user_id}_utilization",
                factor=CreditFactor.CREDIT_UTILIZATION,
                title="Reduce Credit Utilization",
                description="Keep credit utilization below 30%. Pay down balances or request credit limit increases.",
                impact_score=15,
                difficulty="medium",
                estimated_time="2 months",
                action_items=[
                    "Pay down credit card balances",
                    "Request credit limit increases",
                    "Avoid maxing out credit cards"
                ]
            ))
        
        # Length of history recommendations
        if factors.get(CreditFactor.LENGTH_OF_HISTORY.value, 0) < 0.1:
            recommendations.append(CreditRecommendation(
                recommendation_id=f"rec_{user_id}_history",
                factor=CreditFactor.LENGTH_OF_HISTORY,
                title="Build Credit History",
                description="Keep old accounts open and use credit responsibly over time.",
                impact_score=10,
                difficulty="hard",
                estimated_time="12+ months",
                action_items=[
                    "Keep oldest credit accounts open",
                    "Use credit cards regularly and pay in full",
                    "Avoid closing old accounts"
                ]
            ))
        
        return recommendations
    
    async def simulate_score_improvement(
        self,
        user_id: str,
        recommendations: List[CreditRecommendation]
    ) -> CreditProjection:
        """
        Simulate credit score improvement based on recommendations.
        
        Args:
            user_id: User identifier
            recommendations: List of recommendations to apply
            
        Returns:
            CreditProjection with projected score
        """
        logger.info(f"Simulating score improvement for user {user_id}")
        
        # Get current score
        score = await self.credit_monitoring._get_latest_score(user_id)
        if not score:
            score = CreditScore(
                score_id="default",
                user_id=user_id,
                score=650,
                report_date=datetime.now(timezone.utc)
            )
        
        # Calculate projected improvement
        total_impact = sum(r.impact_score for r in recommendations)
        projected_score = min(850, score.score + total_impact)
        
        # Estimate time to improvement (use longest recommendation time)
        max_time = max(
            (r.estimated_time for r in recommendations),
            key=lambda x: int(x.split()[0]) if x.split()[0].isdigit() else 0
        ) if recommendations else "3 months"
        
        # Projected date
        months = int(max_time.split()[0]) if max_time.split()[0].isdigit() else 3
        projected_date = datetime.now(timezone.utc) + timedelta(days=months * 30)
        
        return CreditProjection(
            projection_id=f"proj_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            current_score=score.score,
            projected_score=projected_score,
            projected_date=projected_date,
            assumptions={
                'recommendations_applied': len(recommendations),
                'total_impact': total_impact,
                'timeframe': max_time
            },
            confidence_level=0.75
        )


# Singleton instance
_credit_improvement_service: Optional[CreditImprovementService] = None


def get_credit_improvement_service() -> CreditImprovementService:
    """Get singleton credit improvement service instance."""
    global _credit_improvement_service
    if _credit_improvement_service is None:
        _credit_improvement_service = CreditImprovementService()
    return _credit_improvement_service
