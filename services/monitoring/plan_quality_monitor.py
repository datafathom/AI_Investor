import logging
from typing import List, Dict, Any
from uuid import UUID

logger = logging.getLogger(__name__)

class PlanQualityMonitor:
    """Monitors the quality and accuracy of AI-generated financial plans."""
    
    def __init__(self):
        self.satisfaction_scores = [] # List of scores 1-5

    def track_quality_metric(self, plan_id: UUID, satisfaction: int, advisor_override: bool):
        """
        Records quality metrics for a plan.
        - satisfaction: Client rating (1-5)
        - advisor_override: True if a human advisor changed AI recommendations
        """
        metric = {
            "plan_id": plan_id,
            "satisfaction": satisfaction,
            "override": advisor_override
        }
        self.satisfaction_scores.append(satisfaction)
        
        if advisor_override:
            logger.warning(f"QUALITY_LOG: Plan {plan_id} required human override. Accuracy drift possible.")
        
        if satisfaction < 3:
            logger.error(f"QUALITY_LOG: Low satisfaction ({satisfaction}) for plan {plan_id}!")
            
        return metric

    def get_aggregate_health(self) -> float:
        if not self.satisfaction_scores: return 100.0
        avg = sum(self.satisfaction_scores) / len(self.satisfaction_scores)
        # Convert 1-5 scale to 0-100 percentage
        return round((avg / 5) * 100, 2)
