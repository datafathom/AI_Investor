import logging
from typing import List, Dict, Any
from models.spending import SpendingCategory

logger = logging.getLogger(__name__)

class SpendingAnalyzer:
    """Analyzes spending patterns and identifies savings opportunities."""
    
    def analyze_patterns(self, monthly_spending: SpendingCategory) -> Dict[str, Any]:
        opportunities = []
        
        # Upper-middle class "Waste" detection logic
        if monthly_spending.subscriptions > 200:
            opportunities.append({"category": "SUBSCRIPTIONS", "message": "High subscription burn detected (> $200)."})
            
        if monthly_spending.food_dining > 1000:
            opportunities.append({"category": "DINING", "message": "Dining expenses exceed peer-group average."})
            
        total = monthly_spending.total_spending
        savings = monthly_spending.savings_contributions + monthly_spending.investments
        
        savings_rate = (savings / (total + savings)) if (total + savings) > 0 else 0
        
        logger.info(f"SPENDING_LOG: Analyzed user {monthly_spending.user_id}, savings rate: {savings_rate*100:.1f}%")
        
        return {
            "user_id": monthly_spending.user_id,
            "savings_rate": round(savings_rate, 4),
            "opportunities": opportunities
        }
