from typing import Dict
from agents.base_agent import BaseAgent
from agents.guardian.bill_automator_agent import BillAutomatorAgent
from agents.guardian.flow_master_agent import FlowMasterAgent
from agents.guardian.budget_enforcer_agent import BudgetEnforcerAgent
from agents.guardian.fraud_watchman_agent import FraudWatchmanAgent
from agents.guardian.subscription_assassin_agent import SubscriptionAssassinAgent
from agents.guardian.credit_score_sentinel_agent import CreditScoreSentinelAgent

def get_guardian_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Guardian department agents.
    """
    return {
        "guardian.bill_automator": BillAutomatorAgent(),
        "guardian.flow_master": FlowMasterAgent(),
        "guardian.budget_enforcer": BudgetEnforcerAgent(),
        "guardian.fraud_watchman": FraudWatchmanAgent(),
        "guardian.subscription_assassin": SubscriptionAssassinAgent(),
        "guardian.credit_score_sentinel": CreditScoreSentinelAgent(),
    }
