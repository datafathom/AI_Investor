"""
Monte Carlo Simulator Service.
Projects current strategy statistics forward to identify survival probability and ruin risk.
"""
import random
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MonteCarloSimulator:
    """
    Survival model for long-term expectancy projection.
    """

    @staticmethod
    def run_simulation(
        win_rate: float, 
        avg_win_r: float, 
        avg_loss_r: float, 
        initial_balance: float = 100000.0,
        risk_per_trade_pct: float = 0.01,
        num_trades: int = 1000
    ) -> Dict[str, Any]:
        """
        Simulate a sequence of trades based on statistical averages.
        """
        equity_curve = [initial_balance]
        current_equity = initial_balance
        peak_equity = initial_balance
        max_drawdown = 0.0
        
        for _ in range(num_trades):
            is_win = random.random() < win_rate
            risk_amount = current_equity * risk_per_trade_pct
            
            if is_win:
                result = risk_amount * avg_win_r
            else:
                result = -(risk_amount * abs(avg_loss_r))
                
            current_equity += result
            equity_curve.append(current_equity)
            
            # Update DD
            if current_equity > peak_equity:
                peak_equity = current_equity
            
            drawdown = (peak_equity - current_equity) / peak_equity
            if drawdown > max_drawdown:
                max_drawdown = drawdown

            # Ruin check
            if current_equity <= (initial_balance * 0.5): # 50% ruin threshold
                 break

        return {
            "final_equity": round(current_equity, 2),
            "max_drawdown_pct": round(max_drawdown * 100, 2),
            "ruin_occurred": current_equity <= (initial_balance * 0.5),
            "trades_completed": len(equity_curve) - 1
        }
