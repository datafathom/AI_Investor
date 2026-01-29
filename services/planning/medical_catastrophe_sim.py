import logging
import random
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MedicalCatastropheSimulator:
    """
    Simulates financial impact of severe medical events.
    """
    
    SCENARIOS = {
        "SHORT_TERM_DISABILITY": {"months_lost": 4, "out_of_pocket": 5000},
        "LONG_TERM_DISABILITY": {"months_lost": 18, "out_of_pocket": 15000},
        "MAJOR_SURGERY": {"months_lost": 2, "out_of_pocket": 8000},
        "CHRONIC_ILLNESS": {"months_lost": 0, "out_of_pocket": 12000} # Annual recurring
    }

    def simulate_impact(self, user_income_monthly: float, scenario_name: str) -> Dict[str, Any]:
        scenario = self.SCENARIOS.get(scenario_name)
        if not scenario:
            return {"error": "Unknown scenario"}
            
        income_loss = user_income_monthly * scenario["months_lost"]
        total_hit = income_loss + scenario["out_of_pocket"]
        
        logger.info(f"SIM_MEDICAL: Scenario {scenario_name} impact: ${total_hit:,.2f}")
        
        return {
            "scenario": scenario_name,
            "income_loss": income_loss,
            "medical_bills": scenario["out_of_pocket"],
            "total_financial_hit": total_hit,
            "months_to_recover": round(total_hit / (user_income_monthly * 0.2), 1) # assuming 20% save rate
        }
