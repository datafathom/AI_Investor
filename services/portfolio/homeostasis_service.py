
import logging
from typing import Dict, Any
from services.data.bank_simulation import bank_simulator

logger = logging.getLogger(__name__)

class HomeostasisService:
    """
    Phase 42: The Answer.
    Governs the balance between net worth, goals, and risk.
    """
    
    def __init__(self):
        self.homeostasis_target = 1000000.0  # $1M "Enough" metric
        self.current_net_worth = 0.0
        self.is_autopilot_enabled = True
        self.philanthropy_percentage = 0.10  # 10% of excess alpha

    def update_net_worth(self, tenant_id: str, net_worth: float):
        """Update current net worth and evaluate homeostasis."""
        self.current_net_worth = net_worth
        logger.info(f"Net worth updated for {tenant_id}: ${net_worth}")
        
        if self.current_net_worth >= self.homeostasis_target:
            self._activate_preservation_mode(tenant_id)
        
        if self.is_autopilot_enabled:
            self._run_autopilot(tenant_id)

    def _activate_preservation_mode(self, tenant_id: str):
        """Switch to low-risk, stable yielding strategy."""
        logger.warning(f"HOMEOTASIS REACHED for {tenant_id}! Switching to Preservation Mode.")
        # Trigger portfolio manager to shift to 100% Defensive Shield
        # In a real impl, this would call portfolio_manager.set_risk_profile('defensive')

    def _run_autopilot(self, tenant_id: str):
        """Automatically manage cash flows between bank and investments."""
        bank_status = bank_simulator.get_status(tenant_id)
        balance = bank_status['bank_balance']
        expenses = bank_status['monthly_expenses']
        
        # If bank has more than 3 months of expenses, pull surplus
        surplus_threshold = expenses * 3
        if balance > surplus_threshold:
            surplus = balance - surplus_threshold
            bank_simulator.pull_surplus(tenant_id, surplus)
            logger.info(f"Autopilot: Pulled ${surplus} to invest.")

    def get_homeostasis_status(self, tenant_id: str) -> Dict[str, Any]:
        """Return current status of the homeostasis system."""
        score = min(100, (self.current_net_worth / self.homeostasis_target) * 100) if self.homeostasis_target > 0 else 100
        return {
            "net_worth": self.current_net_worth,
            "target": self.homeostasis_target,
            "homeostasis_score": score,
            "autopilot": self.is_autopilot_enabled,
            "preservation_mode": self.current_net_worth >= self.homeostasis_target,
            "charity_rate": self.philanthropy_percentage
        }

homeostasis_service = HomeostasisService()
