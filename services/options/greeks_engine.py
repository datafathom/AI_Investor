import logging
import math
from typing import Dict, Any
from scipy.stats import norm

logger = logging.getLogger(__name__)

class GreeksEngine:
    """
    High-precision Black-Scholes engine for calculating option Greeks.
    Essential for tail-risk hedging and portfolio protection.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GreeksEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("GreeksEngine initialized")

    def calculate_bs_greeks(
        self, 
        S: float,  # Spot price
        K: float,  # Strike price
        T: float,  # Time to expiry (years)
        r: float,  # Risk-free rate (decimal)
        sigma: float, # Volatility (decimal)
        is_call: bool = True
    ) -> Dict[str, Any]:
        """
        Black-Scholes Greek Formulae.
        """
        try:
            d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
            d2 = d1 - sigma * math.sqrt(T)
            
            if is_call:
                delta = norm.cdf(d1)
                theta = (- (S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2))
            else:
                delta = norm.cdf(d1) - 1
                theta = (- (S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2))
            
            gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
            vega = S * norm.pdf(d1) * math.sqrt(T)
            
            logger.debug(f"GREEKS_LOG: Calculated {('Call' if is_call else 'Put')} Greeks for {S}/{K}.")
            
            return {
                "delta": round(delta, 4),
                "gamma": round(gamma, 6),
                "theta": round(theta / 365, 4), # Daily theta
                "vega": round(vega / 100, 4),   # Vega per 1% vol
                "d1": round(d1, 4),
                "d2": round(d2, 4)
            }
        except Exception as e:
            logger.error(f"MATH_ERR: Black-Scholes failure: {str(e)}")
            return {}
