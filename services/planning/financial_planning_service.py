"""
==============================================================================
FILE: services/planning/financial_planning_service.py
ROLE: Financial Planning Engine
PURPOSE: Provides goal-based asset allocation, contribution recommendations,
         and timeline projections for financial goals.

INTEGRATION POINTS:
    - GoalTrackingService: Goal progress and status
    - PortfolioService: Current portfolio state
    - MarketDataService: Expected returns and risk
    - FinancialPlanningAPI: Planning endpoints
    - FrontendPlanning: Planning dashboard

FEATURES:
    - Goal-based asset allocation
    - Contribution recommendations
    - Timeline projections
    - Multi-goal optimization

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
from models.financial_planning import (
    FinancialGoal, GoalProjection, AssetAllocationRecommendation,
    FinancialPlan, GoalType, GoalStatus
)
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class FinancialPlanningService:
    """
    Service for financial planning and goal-based recommendations.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.risk_free_rate = 0.02  # 2% risk-free rate
        
    async def create_financial_plan(
        self,
        user_id: str,
        goals: List[Dict],
        monthly_contribution_capacity: float
    ) -> FinancialPlan:
        """
        Create comprehensive financial plan for user.
        
        Args:
            user_id: User identifier
            goals: List of goal dictionaries
            monthly_contribution_capacity: Total monthly contribution capacity
            
        Returns:
            FinancialPlan with recommendations
        """
        logger.info(f"Creating financial plan for user {user_id}")
        
        # Convert goals to FinancialGoal objects
        financial_goals = []
        for goal_data in goals:
            goal = FinancialGoal(
                goal_id=f"goal_{user_id}_{datetime.utcnow().timestamp()}",
                user_id=user_id,
                created_date=datetime.utcnow(),
                updated_date=datetime.utcnow(),
                **goal_data
            )
            financial_goals.append(goal)
        
        # Calculate total amounts
        total_target = sum(g.target_amount for g in financial_goals)
        total_current = sum(g.current_amount for g in financial_goals)
        
        # Generate asset allocation recommendations for each goal
        recommended_allocations = {}
        for goal in financial_goals:
            allocation = await self._recommend_asset_allocation(goal)
            recommended_allocations[goal.goal_id] = allocation
        
        plan = FinancialPlan(
            plan_id=f"plan_{user_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            goals=financial_goals,
            total_target_amount=total_target,
            total_current_amount=total_current,
            monthly_contribution_capacity=monthly_contribution_capacity,
            recommended_allocations=recommended_allocations,
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        
        # Cache plan
        cache_key = f"financial_plan:{user_id}"
        self.cache_service.set(cache_key, plan.dict(), ttl=86400)
        
        return plan
    
    async def project_goal_timeline(
        self,
        goal: FinancialGoal,
        expected_return: Optional[float] = None,
        monthly_contribution: Optional[float] = None
    ) -> GoalProjection:
        """
        Project goal timeline and required contributions.
        
        Args:
            goal: Financial goal
            expected_return: Expected annual return (if None, uses recommendation)
            monthly_contribution: Monthly contribution (if None, calculates required)
            
        Returns:
            GoalProjection with timeline analysis
        """
        logger.info(f"Projecting timeline for goal {goal.goal_id}")
        
        # Get expected return from allocation recommendation
        if expected_return is None:
            allocation = await self._recommend_asset_allocation(goal)
            expected_return = allocation.expected_return
        
        # Calculate required monthly contribution if not provided
        if monthly_contribution is None:
            monthly_contribution = await self._calculate_required_contribution(
                goal, expected_return
            )
        
        # Project future value
        months_to_target = (goal.target_date - datetime.utcnow()).days / 30.0
        monthly_return = expected_return / 12.0
        
        # Future value of current amount
        fv_current = goal.current_amount * ((1 + monthly_return) ** months_to_target)
        
        # Future value of contributions (annuity)
        if monthly_return > 0:
            fv_contributions = monthly_contribution * (
                ((1 + monthly_return) ** months_to_target - 1) / monthly_return
            )
        else:
            fv_contributions = monthly_contribution * months_to_target
        
        projected_amount = fv_current + fv_contributions
        
        # Calculate projected completion date
        if projected_amount >= goal.target_amount:
            # Goal will be achieved on time or early
            projected_date = goal.target_date
            months_to_completion = int(months_to_target)
            on_track = True
        else:
            # Calculate how many months needed
            required_months = await self._calculate_months_to_completion(
                goal, monthly_contribution, expected_return
            )
            projected_date = datetime.utcnow() + timedelta(days=required_months * 30)
            months_to_completion = required_months
            on_track = False
        
        # Calculate confidence level (simplified)
        confidence_level = 0.7 if on_track else 0.5
        
        return GoalProjection(
            goal_id=goal.goal_id,
            current_amount=goal.current_amount,
            target_amount=goal.target_amount,
            projected_amount=projected_amount,
            projected_date=projected_date,
            months_to_completion=months_to_completion,
            required_monthly_contribution=monthly_contribution,
            on_track=on_track,
            confidence_level=confidence_level
        )
    
    async def optimize_goal_contributions(
        self,
        plan: FinancialPlan
    ) -> Dict[str, float]:
        """
        Optimize monthly contributions across multiple goals.
        
        Args:
            plan: Financial plan with multiple goals
            
        Returns:
            Dictionary of {goal_id: recommended_monthly_contribution}
        """
        logger.info(f"Optimizing contributions for plan {plan.plan_id}")
        
        total_capacity = plan.monthly_contribution_capacity
        goals = plan.goals
        
        # Calculate required contributions for each goal
        required_contributions = {}
        for goal in goals:
            allocation = plan.recommended_allocations.get(goal.goal_id)
            expected_return = allocation.expected_return if allocation else 0.07
            
            required = await self._calculate_required_contribution(goal, expected_return)
            required_contributions[goal.goal_id] = required
        
        total_required = sum(required_contributions.values())
        
        # If total required exceeds capacity, prioritize by priority and urgency
        if total_required > total_capacity:
            # Sort goals by priority and urgency
            sorted_goals = sorted(
                goals,
                key=lambda g: (
                    g.priority,
                    (g.target_date - datetime.utcnow()).days
                ),
                reverse=True
            )
            
            # Allocate capacity proportionally based on priority
            optimized = {}
            remaining_capacity = total_capacity
            
            for goal in sorted_goals:
                required = required_contributions[goal.goal_id]
                priority_weight = goal.priority / 10.0
                
                allocated = min(required, remaining_capacity * priority_weight)
                optimized[goal.goal_id] = allocated
                remaining_capacity -= allocated
        else:
            # Can meet all requirements
            optimized = required_contributions
        
        return optimized
    
    async def _recommend_asset_allocation(
        self,
        goal: FinancialGoal
    ) -> AssetAllocationRecommendation:
        """Recommend asset allocation based on goal characteristics."""
        # Determine risk level based on goal type and timeline
        months_to_goal = (goal.target_date - datetime.utcnow()).days / 30.0
        years_to_goal = months_to_goal / 12.0
        
        if years_to_goal < 2:
            risk_level = "conservative"
            allocation = {"Equity": 0.20, "Fixed Income": 0.60, "Cash": 0.20}
            expected_return = 0.04
            expected_volatility = 0.08
        elif years_to_goal < 5:
            risk_level = "moderate"
            allocation = {"Equity": 0.50, "Fixed Income": 0.40, "Cash": 0.10}
            expected_return = 0.06
            expected_volatility = 0.12
        else:
            risk_level = "aggressive"
            allocation = {"Equity": 0.80, "Fixed Income": 0.15, "Cash": 0.05}
            expected_return = 0.08
            expected_volatility = 0.18
        
        rationale = f"Recommended {risk_level} allocation based on {years_to_goal:.1f} year timeline"
        
        return AssetAllocationRecommendation(
            goal_id=goal.goal_id,
            recommended_allocation=allocation,
            risk_level=risk_level,
            expected_return=expected_return,
            expected_volatility=expected_volatility,
            rationale=rationale
        )
    
    async def _calculate_required_contribution(
        self,
        goal: FinancialGoal,
        expected_return: float
    ) -> float:
        """Calculate required monthly contribution to reach goal."""
        months_to_goal = (goal.target_date - datetime.utcnow()).days / 30.0
        monthly_return = expected_return / 12.0
        
        remaining = goal.target_amount - goal.current_amount
        
        if months_to_goal <= 0:
            return remaining / 1.0  # Immediate
        
        # Future value of current amount
        fv_current = goal.current_amount * ((1 + monthly_return) ** months_to_goal)
        remaining_after_growth = goal.target_amount - fv_current
        
        if remaining_after_growth <= 0:
            return 0.0  # Already on track
        
        # Calculate required monthly contribution (PMT)
        if monthly_return > 0:
            required = remaining_after_growth * (
                monthly_return / ((1 + monthly_return) ** months_to_goal - 1)
            )
        else:
            required = remaining_after_growth / months_to_goal
        
        return max(0.0, required)
    
    async def _calculate_months_to_completion(
        self,
        goal: FinancialGoal,
        monthly_contribution: float,
        expected_return: float
    ) -> int:
        """Calculate months needed to reach goal with given contribution."""
        monthly_return = expected_return / 12.0
        remaining = goal.target_amount - goal.current_amount
        
        if monthly_contribution <= 0:
            return 999  # Never
        
        # Iterative calculation (simplified)
        current = goal.current_amount
        months = 0
        max_months = 600  # 50 years max
        
        while current < goal.target_amount and months < max_months:
            current = current * (1 + monthly_return) + monthly_contribution
            months += 1
        
        return months


# Singleton instance
_financial_planning_service: Optional[FinancialPlanningService] = None


def get_financial_planning_service() -> FinancialPlanningService:
    """Get singleton financial planning service instance."""
    global _financial_planning_service
    if _financial_planning_service is None:
        _financial_planning_service = FinancialPlanningService()
    return _financial_planning_service
