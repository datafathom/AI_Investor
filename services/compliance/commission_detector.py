import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class CommissionDetector:
    """Detects commissions and proprietary product kickbacks in revenue streams."""
    
    def analyze_revenue(self, transactions: List[Dict[str, Any]]) -> Dict[str, float]:
        total_revenue = sum(t.get("amount", 0) for t in transactions)
        commission_revenue = sum(t.get("amount", 0) for t in transactions if t.get("is_commission", False))
        kickback_revenue = sum(t.get("amount", 0) for t in transactions if t.get("is_proprietary_kickback", False))
        
        if total_revenue == 0:
            return {"commission_pct": 0.0, "kickback_pct": 0.0}

        return {
            "commission_pct": round(commission_revenue / total_revenue, 4),
            "kickback_pct": round(kickback_revenue / total_revenue, 4)
        }

    def detect_churn(self, trades: List[Dict[str, Any]], advisor_id: str) -> float:
        """Detects high-frequency trading intended to generate commissions."""
        # Mock churn calculation based on turnover ratio
        logger.info(f"COIS_LOG: Analyzing trade churn for advisor {advisor_id}")
        return 0.05 # 5% excess volume
