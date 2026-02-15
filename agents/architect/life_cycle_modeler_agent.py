import logging
from typing import Any, Dict, Optional
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider
from services.architect.life_cycle_service import get_lifecycle_service

logger = logging.getLogger(__name__)

class LifeCycleModelerAgent(BaseAgent):
    """
    Agent 2.1: The Life-Cycle Modeler
    
    Monitors long-term financial health and FI (Financial Independence) status.
    Calculates 40-year projections based on current assets, burn rate, and investment returns.
    
    Inputs:
    - current_nw (float): Current net worth.
    - monthly_savings (float): Target monthly savings amount.
    - monthly_burn (float): Expected monthly living expenses.
    - expected_return (float): Assumed portfolio growth rate (default: 7%).
    
    Outputs:
    - fi_year (int): Estimated year of financial independence.
    - fi_age (int): Estimated age at financial independence.
    - success_rate (float): Probability of portfolio survival via Monte Carlo.
    """

    def __init__(self) -> None:
        super().__init__(name="architect.life_cycle_modeler", provider=ModelProvider.GEMINI)
        self.lifecycle = get_lifecycle_service()

    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event.get("type") == "model.run_projection":
            return self._run_projection(event)
        return None

    def _run_projection(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a long-term projection."""
        params = event.get("params", {})
        result = self.lifecycle.run_simulation(
            current_nw=params.get("current_nw", 0.0),
            monthly_savings=params.get("monthly_savings", 0.0),
            monthly_burn=params.get("monthly_burn", 0.0),
            expected_return=params.get("expected_return", 0.07),
            inflation=params.get("inflation", 0.03),
            horizon_years=params.get("horizon_years", 50),
            current_age=params.get("current_age", 30)
        )
        
        return {
            "status": "COMPLETED",
            "fi_year": result.fi_year,
            "fi_age": result.fi_age,
            "success_rate": result.success_rate,
            "execution_time_ms": result.execution_time_ms,
            "under_1s_sla": result.execution_time_ms < 1000
        }
