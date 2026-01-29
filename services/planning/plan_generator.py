import logging
from typing import Dict, Any
from models.financial_plan import FinancialPlan
from services.planning.complexity_analyzer import ComplexityAnalyzer
from uuid import UUID

logger = logging.getLogger(__name__)

class PlanGenerator:
    """Generates standardized financial plans using AI-driven logic."""
    
    def __init__(self, analyzer: ComplexityAnalyzer):
        self.analyzer = analyzer

    def generate_plan(self, user_id: UUID, user_data: Dict[str, Any]) -> FinancialPlan:
        score = self.analyzer.analyze_complexity(user_data)
        human_needed = self.analyzer.requires_human(score)
        
        plan = FinancialPlan(
            user_id=user_id,
            complexity_score=score,
            requires_human_review=human_needed,
            status="REVIEW_REQUIRED" if human_needed else "COMPLETED"
        )
        
        if human_needed:
            logger.warning(f"PLANNING_ALERT: High complexity ({score}) for {user_id}. Human review queued.")
        else:
            logger.info(f"PLANNING_LOG: AI Plan completed for {user_id}.")
            
        return plan
