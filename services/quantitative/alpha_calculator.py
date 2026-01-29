import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AlphaCalculator:
    """Calculates Alpha (Excess Return) relative to a benchmark and risk-free rate."""
    
    def calculate_simple_alpha(self, portfolio_return: float, benchmark_return: float) -> float:
        """Simple Alpha = Rp - Rm"""
        alpha = portfolio_return - benchmark_return
        logger.info(f"QUANT_LOG: Simple Alpha: {alpha:.2%}")
        return round(float(alpha), 4)

    def calculate_jensens_alpha(self, portfolio_ret: float, benchmark_ret: float, rf_rate: float, beta: float) -> float:
        """
        Jensen's Alpha = Rp - [Rf + Beta * (Rm - Rf)]
        """
        expected_ret = rf_rate + (beta * (benchmark_ret - rf_rate))
        alpha = portfolio_ret - expected_ret
        
        logger.info(f"QUANT_LOG: Jensen's Alpha: {alpha:.4f} (Expected: {expected_ret:.2%}, Actual: {portfolio_ret:.2%})")
        return round(float(alpha), 4)
