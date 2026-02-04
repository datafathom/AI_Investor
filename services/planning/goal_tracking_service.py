"""
==============================================================================
FILE: services/planning/goal_tracking_service.py
ROLE: Goal Tracking Service
PURPOSE: Tracks goal progress, updates status, and provides milestone
         tracking and alerts.

INTEGRATION POINTS:
    - FinancialPlanningService: Goal definitions and projections
    - PortfolioService: Current portfolio value
    - NotificationService: Goal milestone alerts
    - GoalTrackingAPI: Tracking endpoints
    - FrontendPlanning: Goal dashboard

FEATURES:
    - Progress tracking
    - Status updates
    - Milestone detection
    - Progress alerts

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from schemas.financial_planning import (
    FinancialGoal, GoalStatus, GoalProjection
)
from services.planning.financial_planning_service import get_financial_planning_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class GoalTrackingService:
    """
    Service for tracking goal progress and status.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.planning_service = get_financial_planning_service()
        self.cache_service = get_cache_service()
        
    async def update_goal_progress(
        self,
        goal_id: str,
        current_amount: float
    ) -> FinancialGoal:
        """
        Update goal progress with current amount.
        
        Args:
            goal_id: Goal identifier
            current_amount: Current amount saved
            
        Returns:
            Updated FinancialGoal with new status
        """
        logger.info(f"Updating progress for goal {goal_id}")
        
        # Get goal from cache or database
        goal = await self._get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        
        # Update current amount
        goal.current_amount = current_amount
        goal.updated_date = datetime.now(timezone.utc)
        
        # Update status
        goal.status = await self._calculate_status(goal)
        
        # Save updated goal
        await self._save_goal(goal)
        
        return goal
    
    async def get_goal_progress(
        self,
        goal_id: str
    ) -> Dict:
        """
        Get comprehensive goal progress information.
        
        Args:
            goal_id: Goal identifier
            
        Returns:
            Progress information with projection and milestones
        """
        goal = await self._get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")
        
        # Get projection
        projection = await self.planning_service.project_goal_timeline(goal)
        
        # Calculate progress percentage
        progress_pct = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0.0
        
        # Get milestones
        milestones = await self._get_milestones(goal)
        
        return {
            'goal': goal.model_dump(),
            'projection': projection.model_dump(),
            'progress_percentage': progress_pct,
            'milestones': milestones,
            'status': goal.status.value
        }
    
    async def get_goals(self, user_id: str) -> List[FinancialGoal]:
        """
        Get all goals for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of FinancialGoals
        """
        # In a real implementation this would fetch from DB
        return await self._get_user_goals_from_db(user_id)

    async def _get_user_goals_from_db(self, user_id: str) -> List[FinancialGoal]:
        """Get user goals from storage."""
        # Mock/Placeholder implementation
        return []

    async def check_milestones(
        self,
        goal_id: str
    ) -> List[Dict]:
        """
        Check for milestone achievements.
        
        Args:
            goal_id: Goal identifier
            
        Returns:
            List of achieved milestones
        """
        goal = await self._get_goal(goal_id)
        if not goal:
            return []
        
        milestones = []
        progress_pct = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0.0
        
        # Check percentage milestones
        milestone_percentages = [25, 50, 75, 90, 100]
        for pct in milestone_percentages:
            if progress_pct >= pct:
                milestones.append({
                    'milestone': f"{pct}% Complete",
                    'achieved': True,
                    'achieved_date': goal.updated_date.isoformat()
                })
        
        # Check amount milestones
        milestone_amounts = [
            goal.target_amount * 0.25,
            goal.target_amount * 0.50,
            goal.target_amount * 0.75,
            goal.target_amount * 0.90
        ]
        for amount in milestone_amounts:
            if goal.current_amount >= amount:
                milestones.append({
                    'milestone': f"${amount:,.0f} Saved",
                    'achieved': True,
                    'achieved_date': goal.updated_date.isoformat()
                })
        
        return milestones
    
    async def _calculate_status(self, goal: FinancialGoal) -> GoalStatus:
        """Calculate goal status based on progress and timeline."""
        progress_pct = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0.0
        days_remaining = (goal.target_date - datetime.now(timezone.utc)).days
        days_total = (goal.target_date - goal.created_date).days
        progress_days = days_total - days_remaining
        
        expected_progress = (progress_days / days_total * 100) if days_total > 0 else 0.0
        
        if progress_pct >= 100:
            return GoalStatus.COMPLETED
        elif progress_pct >= expected_progress * 0.9:  # Within 90% of expected
            return GoalStatus.ON_TRACK
        elif progress_pct >= expected_progress * 0.7:  # Within 70% of expected
            return GoalStatus.IN_PROGRESS
        elif progress_pct > 0:
            return GoalStatus.AT_RISK
        else:
            return GoalStatus.NOT_STARTED
    
    async def _get_goal(self, goal_id: str) -> Optional[FinancialGoal]:
        """Get goal from cache or database."""
        cache_key = f"goal:{goal_id}"
        goal_data = self.cache_service.get(cache_key)
        if goal_data:
            return FinancialGoal(**goal_data)
        return None
    
    async def _save_goal(self, goal: FinancialGoal):
        """Save goal to cache or database."""
        cache_key = f"goal:{goal.goal_id}"
        self.cache_service.set(cache_key, goal.model_dump(), ttl=86400 * 365)  # 1 year
    
    async def _get_milestones(self, goal: FinancialGoal) -> List[Dict]:
        """Get milestone information for goal."""
        return await self.check_milestones(goal.goal_id)


# Singleton instance
_goal_tracking_service: Optional[GoalTrackingService] = None


def get_goal_tracking_service() -> GoalTrackingService:
    """Get singleton goal tracking service instance."""
    global _goal_tracking_service
    if _goal_tracking_service is None:
        _goal_tracking_service = GoalTrackingService()
    return _goal_tracking_service
