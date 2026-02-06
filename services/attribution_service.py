from typing import Dict, Any, List
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class AttributionService:
    """
    Calculates and attributes alpha (profit/performance) to specific agents and departments.
    Uses a weighted model: 40% Intelligence (Signal), 60% Execution (Trade).
    """
    
    INTELLIGENCE_WEIGHT = Decimal("0.40")
    EXECUTION_WEIGHT = Decimal("0.60")

    def calculate_attribution(self, mission_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Splits the total P&L of a mission into attribution buckets for involved departments.
        
        Args:
            mission_result (dict): Contains 'total_pnl', 'participating_depts', 'gas_cost'
        
        Returns:
            dict: Attribution breakdown by department ID.
        """
        try:
            total_pnl = Decimal(str(mission_result.get("total_pnl", 0.0)))
            gas_cost = Decimal(str(mission_result.get("gas_cost", 0.0)))
            net_profit = total_pnl - gas_cost
            
            # Participating Depts (e.g., [1, 5]) 
            # 1=Strategist (Intel), 5=Trader (Exec)
            start_depts = mission_result.get("intelligence_depts", [])
            exec_depts = mission_result.get("execution_depts", [])
            
            attribution = {}
            
            # 1. Intelligence Attribution
            if start_depts:
                intel_share = (net_profit * self.INTELLIGENCE_WEIGHT) / len(start_depts)
                for dept in start_depts:
                    attribution[str(dept)] = attribution.get(str(dept), Decimal("0")) + intel_share

            # 2. Execution Attribution
            if exec_depts:
                exec_share = (net_profit * self.EXECUTION_WEIGHT) / len(exec_depts)
                for dept in exec_depts:
                    attribution[str(dept)] = attribution.get(str(dept), Decimal("0")) + exec_share
            
            # Convert Decimals back to float for JSON serialization
            return {k: float(v) for k, v in attribution.items()}
            
        except Exception as e:
            logger.error(f"Failed to calculate attribution: {e}")
            return {}

    def get_aggregated_stats(self, db_connection) -> List[Dict[str, Any]]:
        """
        Fetch aggregated ROI stats for all departments from DB traces.
        (Placeholder for SQL query)
        """
        # In a real impl, this would query the `agent_traces` table joined with a `mission_results` table
        return []

# Singleton
attribution_service = AttributionService()

def get_attribution_service() -> AttributionService:
    return attribution_service
