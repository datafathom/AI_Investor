import logging
from uuid import UUID
from typing import Dict, Any

logger = logging.getLogger(__name__)

class HeirGovernanceService:
    """
    Manages Family Office HR and Descendant Employment.
    Tracks nepotism roles and discretionary compensation overrides.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HeirGovernanceService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("HeirGovernanceService initialized")

    def evaluate_role_productivity(self, heir_id: UUID, role_title: str, salary: float, market_rate_avg: float) -> Dict[str, Any]:
        """
        Policy: If salary > market_rate * 1.5, flag as 'Discretionary Support' (Nepotism).
        """
        pay_ratio = salary / market_rate_avg if market_rate_avg > 0 else 1.0
        is_nepotism = pay_ratio > 1.5
        
        logger.info(f"HR_LOG: Heir role audit {role_title}. Pay Ratio: {pay_ratio:.2f}x. Nepotism: {is_nepotism}")
        
        return {
            "role": role_title,
            "pay_premium_pct": round((pay_ratio - 1) * 100, 2),
            "status": "CUSHY_JOB" if is_nepotism else "MARKET_ALIGNED",
            "social_maintenance_value": "HIGH" if is_nepotism else "STANDARD"
        }
