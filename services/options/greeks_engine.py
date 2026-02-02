"""
==============================================================================
FILE: services/options/greeks_engine.py
ROLE: Black-Scholes Greeks Calculator
PURPOSE: Calculate Delta, Gamma, Theta, Vega, and Rho for option chains.
         Used for 'Tail Risk Hedging' (buying cheap OTM puts) and 
         'Covered Calls' (selling income).

INTEGRATION:
    - MarketDataService: Spot price, volatility.
    - RiskService: Portfolio beta.

AUTHOR: AI Investor Team
CREATED: 2026-01-30
==============================================================================
"""

import logging
import math
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GreeksEngine:
    """
    Calculates Option Greeks using Black-Scholes logic.
    """

    def calculate_bs_greeks(
        self,
        S: float,      # Spot Price
        K: float,      # Strike Price
        T: float,      # Time to Expiry (years)
        r: float,      # Risk-free Rate
        sigma: float,  # Volatility
        is_call: bool = True
    ) -> Dict[str, float]:
        """
        Calculate Greeks using Black-Scholes-Merton.
        """
        if T <= 0:
            return {"delta": 0.0, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "rho": 0.0}

        try:
            sqrt_T = math.sqrt(T)
            d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt_T)
            d2 = d1 - sigma * sqrt_T

            # PDF and CDF
            pdf_d1 = (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * d1 ** 2)
            cdf_d1 = self._norm_cdf(d1)
            cdf_d2 = self._norm_cdf(d2)
            cdf_neg_d1 = self._norm_cdf(-d1)
            cdf_neg_d2 = self._norm_cdf(-d2)

            # Common Greeks (Gamma, Vega are same for Call/Put)
            gamma = pdf_d1 / (S * sigma * sqrt_T)
            vega = (S * pdf_d1 * sqrt_T) / 100.0  # Scaled by 1/100

            if is_call:
                delta = cdf_d1
                rho = (K * T * math.exp(-r * T) * cdf_d2) / 100.0
                theta = (- (S * pdf_d1 * sigma) / (2 * sqrt_T) 
                         - r * K * math.exp(-r * T) * cdf_d2) / 365.0
            else:
                delta = cdf_d1 - 1.0
                rho = (-K * T * math.exp(-r * T) * cdf_neg_d2) / 100.0
                theta = (- (S * pdf_d1 * sigma) / (2 * sqrt_T) 
                         + r * K * math.exp(-r * T) * cdf_neg_d2) / 365.0

            return {
                "delta": round(delta, 4),
                "gamma": round(gamma, 4),
                "theta": round(theta, 4),
                "vega": round(vega, 4),
                "rho": round(rho, 4)
            }
        except Exception as e:
            logger.error(f"Error calculating Greeks: {e}")
            return {"delta": 0.0, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "rho": 0.0}

    # Alias for backward compatibility if needed
    calculate_greeks = calculate_bs_greeks

    def _norm_cdf(self, x):
        """Standard Normal CDF."""
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
