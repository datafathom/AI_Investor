"""
Gamma Exposure (GEX) Calculator.
Predicts institutional dealer hedging pressure based on options chain data.
"""
from typing import List, Dict, Any, Optional
import math
import logging

logger = logging.getLogger(__name__)

class GEXCalculator:
    """
    Calculates aggregate Gamma Exposure for indices (SPY, QQQ).
    """

    @staticmethod
    def calculate_gex(spot_price: float, options_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate total GEX and find the Gamma Flip point.
        
        Args:
            spot_price: Current underlying price.
            options_chain: List of option contracts with strike, gamma, open_interest, and type.
            
        Returns:
            Dict: {total_gex, gamma_flip_price, call_gex, put_gex}
        """
        total_gex = 0.0
        call_gex = 0.0
        put_gex = 0.0
        
        # Group by strike for flip detection
        strike_gex: Dict[float, float] = {}

        for contract in options_chain:
            strike = float(contract['strike'])
            gamma = float(contract['gamma'])
            oi = float(contract['open_interest'])
            
            # Simplified GEX calculation
            # GEX = Gamma * OI * 100 (contract size) * Spot^2 (if normalized)
            # Standard GEX = Gamma * OI * 100
            gex_val = gamma * oi * 100
            
            if contract['type'].upper() == 'CALL':
                call_gex += gex_val
                strike_gex[strike] = strike_gex.get(strike, 0) + gex_val
            else:
                # Puts are negative gamma for dealers usually
                put_gex -= gex_val
                strike_gex[strike] = strike_gex.get(strike, 0) - gex_val
                
        total_gex = call_gex + put_gex

        # Gamma Flip is where strike_gex transitions from positive to negative
        # Find strike closest to zero GEX
        sorted_strikes = sorted(strike_gex.keys())
        gamma_flip = spot_price # Default to spot
        
        closest_val = float('inf')
        for s in sorted_strikes:
            if abs(strike_gex[s]) < closest_val:
                closest_val = abs(strike_gex[s])
                gamma_flip = s

        return {
            'total_gex': float(total_gex),
            'call_gex': float(call_gex),
            'put_gex': float(put_gex),
            'gamma_flip_price': float(gamma_flip),
            'market_regime': 'LONG_GAMMA' if total_gex > 0 else 'SHORT_GAMMA'
        }
