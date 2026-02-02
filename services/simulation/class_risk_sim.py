import logging
import random
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ClassRiskSim:
    """
    Monte Carlo simulator for 'Drop in Class' risk.
    Calculates the probability that a portfolio fails to support a given lifestyle.
    """
    
    def run_simulation(self, 
                       current_wealth: Decimal, 
                       annual_spend: Decimal, 
                       clew_inflation: Decimal,
                       expected_return: Decimal,
                       volatility: Decimal,
                       years: int = 30,
                       iterations: int = 1000) -> Dict[str, Any]:
        """
        Simulates iterative portfolio returns vs lifestyle burn.
        """
        failures = 0
        ending_balances = []
        
        for _ in range(iterations):
            balance = current_wealth
            spend = annual_spend
            failed = False
            
            for _ in range(years):
                # Annual Return (Normally distributed)
                annual_return = Decimal(str(random.normalvariate(float(expected_return), float(volatility))))
                
                # Apply growth
                balance = balance * (1 + annual_return)
                
                # Apply spend
                balance -= spend
                
                # Inflate spend for next year
                spend = spend * (1 + clew_inflation)
                
                if balance <= 0:
                    failed = True
                    break
            
            if failed:
                failures += 1
            ending_balances.append(float(balance))
            
        failure_prob = Decimal(str(failures)) / Decimal(str(iterations))
        avg_end_balance = sum(ending_balances) / len(ending_balances)
        
        logger.info(f"ClassRiskSim: Iterations={iterations}, FailureProb={failure_prob:.2%}")
        
        return {
            "failure_probability": float(failure_prob),
            "iterations": iterations,
            "years": years,
            "average_ending_wealth": round(avg_end_balance, 2),
            "risk_rating": "HIGH" if failure_prob > 0.10 else "MODERATE" if failure_prob > 0.02 else "LOW"
        }
