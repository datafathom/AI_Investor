"""
==============================================================================
FILE: services/risk/risk_monitor.py
ROLE: Real-time Risk Engine
PURPOSE:
    Monitor portfolio exposure and calculate risk metrics.
    
    1. Value at Risk (VaR):
       - Parametric Method (Normal Distribution assumptions).
       - VaR = Portfolio Value * Volatility * Z-Score (e.g. 1.65 for 95% Conf).
       
    2. Concentration Checks:
       - Alert if any single sector > 20%.
       - Alert if any single asset > 10%.
       
ROADMAP: Phase 20 - Risk Monitor
==============================================================================
"""

import logging
from typing import List, Dict, Any
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class RiskMonitor:
    def __init__(self):
        self.CONFIDENCE_LEVEL = 0.95
        self.Z_SCORE_95 = 1.645 # 1.645 standard deviations for 95% confidence
        
        # Risk Limits
        self.MAX_SECTOR_EXPOSURE = 0.30 # 30% Max per sector
        self.MAX_SINGLE_ASSET_EXPOSURE = 0.20 # 20% Max per asset

    def calculate_parametric_var(self, 
                               portfolio_value: float, 
                               portfolio_volatility: float) -> float:
        """
        Calculate Value at Risk (VaR) using Parametric method (1-day).
        VaR = Value * Volatility * Z-Score
        
        Meaning: "We are 95% confident that we will not lose more than $VaR in 1 day."
        """
        return portfolio_value * portfolio_volatility * self.Z_SCORE_95

    def check_concentration_limits(self, 
                                 holdings: List[Dict[str, Any]]) -> List[str]:
        """
        Check for over-exposure to sectors or assets.
        Args:
            holdings: List of {'symbol': 'AAPL', 'sector': 'Tech', 'weight': 0.15}
        Returns:
            List of warning messages.
        """
        warnings = []
        sector_weights = {}
        
        for item in holdings:
            sym = item.get('symbol', 'UNKNOWN')
            weight = item.get('weight', 0.0)
            sector = item.get('sector', 'Unclassified')
            
            # Check Single Asset Limit
            if weight > self.MAX_SINGLE_ASSET_EXPOSURE:
                warnings.append(f"ASSET WARNING: {sym} weight ({weight*100:.1f}%) exceeds limit ({self.MAX_SINGLE_ASSET_EXPOSURE*100}%)")
                
            # Aggregate Sector Weight
            sector_weights[sector] = sector_weights.get(sector, 0.0) + weight
            
        # Check Sector Limits
        for sector, total_weight in sector_weights.items():
            if total_weight > self.MAX_SECTOR_EXPOSURE:
                warnings.append(f"SECTOR WARNING: {sector} weight ({total_weight*100:.1f}%) exceeds limit ({self.MAX_SECTOR_EXPOSURE*100}%)")
                
        return warnings

# Singleton
_instance = None

def get_risk_monitor() -> RiskMonitor:
    global _instance
    if _instance is None:
        _instance = RiskMonitor()
    return _instance
