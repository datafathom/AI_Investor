from typing import Dict
from agents.base_agent import BaseAgent
from agents.banker.transaction_categorizer_agent import TransactionCategorizerAgent
from agents.banker.ach_wire_tracker_agent import AchWireTrackerAgent
from agents.banker.envelope_budget_manager_agent import EnvelopeBudgetManagerAgent
from agents.banker.recurring_payment_agent_agent import RecurringPaymentAgentAgent
from agents.banker.tax_reserve_calculator_agent import TaxReserveCalculatorAgent
from agents.banker.interest_arbitrage_scout_agent import InterestArbitrageScoutAgent

def get_banker_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Banker department agents.
    """
    return {
        "banker.transaction_categorizer": TransactionCategorizerAgent(),
        "banker.ach_wire_tracker": AchWireTrackerAgent(),
        "banker.envelope_budget_manager": EnvelopeBudgetManagerAgent(),
        "banker.recurring_payment_agent": RecurringPaymentAgentAgent(),
        "banker.tax_reserve_calculator": TaxReserveCalculatorAgent(),
        "banker.interest_arbitrage_scout": InterestArbitrageScoutAgent(),
    }
