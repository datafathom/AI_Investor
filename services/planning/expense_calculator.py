import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ExpenseCalculator:
    """Calculates projected and historical living expenses."""
    
    def calculate_monthly_burn(self, transactions: List[Dict[str, Any]]) -> float:
        """Calculates average monthly spending from transaction history."""
        # logic to filter for recurring living expenses...
        total_spent = sum(t.get("amount", 0) for t in transactions if not t.get("is_investment"))
        
        # Extrapolate to monthly (30 days) based on sample size
        # Assume 1 transaction per day for the mock logic
        days_in_sample = len(transactions)
        if days_in_sample == 0: return 0.0
        
        daily_avg = total_spent / days_in_sample
        avg_burn = daily_avg * 30
        logger.info(f"EXPENSE_LOG: Calculated monthly burn rate: ${avg_burn:,.2f}")
        return round(avg_burn, 2)

    def project_annual_expenses(self, monthly_burn: float, inflation_rate: float = 0.03) -> float:
        """Projects annual expenses including an inflation buffer."""
        return round(monthly_burn * 12 * (1 + inflation_rate), 2)
