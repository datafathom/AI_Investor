import logging
from decimal import Decimal
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ReflexivitySim:
    """
    Phase 182.4: Sorosian Reflexivity Price -> Flow Simulator.
    Simulates the feedback loop where rising prices attract more passive flows.
    """
    
    def simulate_feedback_loop(
        self, 
        initial_price: float, 
        passive_participation: float, 
        steps: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Feedback Loop: Higher Prices -> Higher Sentiment -> Higher Forced Inflow -> Higher Prices.
        """
        history = []
        current_price = initial_price
        
        for i in range(steps):
            # Inelastic impact: Higher prices attract more 'blind' flows
            inflow_coef = 1.0 + (passive_participation * 0.1)
            price_delta = current_price * 0.02 * inflow_coef # 2% mechanical bump
            
            current_price += price_delta
            
            history.append({
                "step": i + 1,
                "price": round(current_price, 2),
                "inflow_pressure": round(inflow_coef, 2)
            })
            
        logger.info(f"SIM_LOG: Reflexivity simulation complete. Final Price: {current_price:.2f}")
        return history

    def simulate_unwind(self, current_price: float, withdrawal_shock_pct: float) -> Dict[str, Any]:
        """
        The 'Ticking Time Bomb' scenario where blind selling begets more selling.
        """
        unwind_price = current_price * (1 - (withdrawal_shock_pct * 3)) # 3x multiplier due to inelasticity
        return {
            "initial_price": current_price,
            "shock_pct": withdrawal_shock_pct,
            "final_unwind_price": round(unwind_price, 2),
            "status": "CRASH_DETECTED" if unwind_price < current_price * 0.70 else "RECOVERY_POSSIBLE"
        }
