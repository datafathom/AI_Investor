"""
Options Pricing and Greeks Service
Phase 5 Implementation: The Volatility Engine

This service implements the Black-Scholes-Merton model for real-time
options pricing and Greeks calculation (Delta, Gamma, Theta, Vega).

ACCEPTANCE CRITERIA from Phase_5_ImplementationPlan.md:
- Greeks match QuantLib/Standard formulas within 0.001 margin.
- recaculate entire chain in < 1 second.
"""

import math
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from scipy.stats import norm

logger = logging.getLogger(__name__)

class OptionsPricingService:
    """
    High-performance options pricing service using Black-Scholes.
    
    Calculates Delta, Gamma, Theta, Vega, and Rho.
    """

    # Singleton pattern
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OptionsPricingService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("OptionsPricingService initialized")

    def black_scholes(
        self,
        S: float,  # Underling price
        K: float,  # Strike price
        T: float,  # Time to expiration (in years)
        r: float,  # Risk-free rate
        sigma: float,  # Volatility
        option_type: str = "call"
    ) -> Dict[str, float]:
        """
        Calculate Black-Scholes option price and Greeks.
        """
        if T <= 0:
            # At expiration
            price = max(0, S - K) if option_type == "call" else max(0, K - S)
            return {
                "price": price,
                "delta": 1.0 if (option_type == "call" and S > K) else (-1.0 if (option_type == "put" and S < K) else 0.0),
                "gamma": 0.0,
                "theta": 0.0,
                "vega": 0.0,
                "rho": 0.0
            }

        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type == "call":
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
            delta = norm.cdf(d1)
            rho = K * T * math.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            delta = norm.cdf(d1) - 1.0
            rho = -K * T * math.exp(-r * T) * norm.cdf(-d2)

        # Gamma and Vega are the same for calls and puts
        gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
        vega = S * norm.pdf(d1) * math.sqrt(T)
        
        # Theta
        if option_type == "call":
            theta = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)
        else:
            theta = -(S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)

        return {
            "price": price,
            "delta": delta,
            "gamma": gamma,
            "theta": theta / 365.0,  # Return daily theta
            "vega": vega / 100.0,    # Return vega per 1% change
            "rho": rho / 100.0       # Return rho per 1% change
        }

    def calculate_implied_volatility(
        self,
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: str = "call",
        precision: float = 0.0001,
        max_iterations: int = 100
    ) -> float:
        """
        Calculate implied volatility using Newton-Raphson method.
        """
        sigma = 0.5  # Initial guess
        for i in range(max_iterations):
            results = self.black_scholes(S, K, T, r, sigma, option_type)
            price = results["price"]
            vega = results["vega"] * 100.0  # Convert back to raw vega

            if vega == 0:
                break
                
            diff = market_price - price
            if abs(diff) < precision:
                return sigma
                
            sigma = sigma + diff / vega
            
        return sigma

# Singleton instance
options_pricing_service = OptionsPricingService()

def get_options_pricing_service() -> OptionsPricingService:
    return options_pricing_service
