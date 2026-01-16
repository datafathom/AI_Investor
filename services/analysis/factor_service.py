"""
==============================================================================
FILE: services/analysis/factor_service.py
ROLE: Factor Analysis & Portfolio Construction
PURPOSE:
    Calculate risk factors (Volatility, Momentum) and generate
    portfolio weights using Risk Parity (Inverse Volatility).
    
    - Volatility: Rolling Standard Deviation of Returns
    - Momentum: Rolling Return (e.g. 12-month, or shorter for intraday)
    - Weights: w_i = (1/vol_i) / sum(1/vol_j)
    
ROADMAP: Phase 15 - Factor Analysis & Risk Parity
==============================================================================
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class FactorService:
    """
    Engine for calculating asset factors and portfolio weights.
    """
    
    def __init__(self):
        pass

    def calculate_factors(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Enrich DataFrame with Volatility and Momentum factors.
        Expects 'close' column.
        """
        if df.empty:
            return df
        
        df = df.copy()
        
        # Calculate Returns
        if 'returns' not in df.columns:
            df['returns'] = df['close'].pct_change()
            
        # 1. Volatility Factor (Realized Volatility)
        # Annualized logic: std * sqrt(252) if daily, or just raw std for relative comparison
        df['volatility'] = df['returns'].rolling(window=window).std()
        
        # 2. Momentum Factor (Rate of Change)
        df['momentum'] = df['close'].pct_change(periods=window)
        
        return df

    def calculate_risk_parity_weights(self, volatility_map: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate Naive Risk Parity weights (Inverse Volatility).
        Weight_i = (1 / Vol_i) / Sum(1 / Vol_j)
        
        Args:
            volatility_map: Dict of {symbol: volatility_value}
        Returns:
            Dict of {symbol: weight} where weights sum to 1.0
        """
        inv_vols = {}
        total_inv_vol = 0.0
        
        # Calculate inverse volatilities
        for sym, vol in volatility_map.items():
            if vol <= 0 or pd.isna(vol):
                logger.warning(f"Invalid volatility for {sym}: {vol}. Skipping.")
                continue
            
            inv = 1.0 / vol
            inv_vols[sym] = inv
            total_inv_vol += inv
            
        if total_inv_vol == 0:
            return {}
            
        # Normalize
        weights = {sym: inv_vol / total_inv_vol for sym, inv_vol in inv_vols.items()}
        return weights

    def get_portfolio_weights(self, prices_map: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """
        Orchestrator: Takes a map of {Symbol: DataFrame}, calculates latest volatility,
        and returns target weights.
        """
        vol_map = {}
        
        for symbol, df in prices_map.items():
            if df.empty:
                continue
                
            df_factors = self.calculate_factors(df)
            
            # Get latest valid volatility
            last_vol = df_factors['volatility'].iloc[-1]
            if pd.isna(last_vol):
                # Try to get last valid index
                valid_idx = df_factors['volatility'].last_valid_index()
                if valid_idx:
                    last_vol = df_factors['volatility'].loc[valid_idx]
                else:
                    logger.warning(f"No valid volatility data for {symbol}")
                    continue
                    
            vol_map[symbol] = float(last_vol)
            
        return self.calculate_risk_parity_weights(vol_map)

# Singleton
_instance = None

def get_factor_service() -> FactorService:
    global _instance
    if _instance is None:
        _instance = FactorService()
    return _instance
