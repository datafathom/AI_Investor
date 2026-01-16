"""
==============================================================================
FILE: services/analysis/feature_service.py
ROLE: Feature Engineering Pipeline
PURPOSE:
    Transforms raw OHLCV market data into ML-ready feature vectors.
    Optimized for speed (< 50ms) using vectorized Pandas/Numpy operations.
    
    Features:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - Bollinger Bands
    - Returns & Volatility
    - Lagged Features
    
ROADMAP: Phase 13 - Feature Engineering Pipeline
==============================================================================
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class FeatureEngineeringService:
    """
    Central engine for generating technical and statistical features
    from financial time-series data.
    """
    
    def __init__(self):
        pass

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main pipeline to generate all features for a given DataFrame.
        Expects columns: ['open', 'high', 'low', 'close', 'volume']
        """
        if df.empty:
            logger.warning("Empty DataFrame provided for feature generation.")
            return df
            
        # Ensure we work on a copy to avoid SettingWithCopy warnings
        df = df.copy()
        
        # Sort by date just in case
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp')
            
        try:
            # 1. Basic Returns
            df['returns'] = df['close'].pct_change()
            df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
            
            # 2. Volatility (Rolling Std Dev)
            df['volatility_20'] = df['returns'].rolling(window=20).std()
            
            # 3. RSI (Relative Strength Index)
            df = self._calculate_rsi(df, window=14)
            
            # 4. MACD
            df = self._calculate_macd(df)
            
            # 5. Bollinger Bands
            df = self._calculate_bollinger_bands(df)
            
            # 6. Lagged Features (e.g., returns from t-1, t-2...)
            lags = [1, 2, 3, 5]
            for lag in lags:
                df[f'returns_lag_{lag}'] = df['returns'].shift(lag)
                df[f'volume_change_lag_{lag}'] = df['volume'].pct_change(periods=lag)
                
            # drop NaN values created by windows/lags
            # df.dropna(inplace=True) 
            # Note: We often want to keep the latest row even if early history is NaN, 
            # but for training we usually drop. For inference, we need history.
            
            return df
            
        except Exception as e:
            logger.error(f"Error in feature generation: {e}")
            raise e

    def _calculate_rsi(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Relative Strength Index (RSI) using vectorized pandas."""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Fill NaN with 50 (neutral) or drop
        df['rsi'] = df['rsi'].fillna(50)
        return df

    def _calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Calculate MACD, MACD Signal, and MACD Histogram."""
        exp1 = df['close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['close'].ewm(span=slow, adjust=False).mean()
        
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        return df

    def _calculate_bollinger_bands(self, df: pd.DataFrame, window: int = 20, num_std: int = 2) -> pd.DataFrame:
        """Calculate Bollinger Bands (Upper, Middle, Lower)."""
        df['bb_middle'] = df['close'].rolling(window=window).mean()
        std_dev = df['close'].rolling(window=window).std()
        
        df['bb_upper'] = df['bb_middle'] + (std_dev * num_std)
        df['bb_lower'] = df['bb_middle'] - (std_dev * num_std)
        
        # %B Indicator (Where price is relative to bands)
        # > 1 = above upper band, < 0 = below lower band
        df['bb_percent_b'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        return df

    def get_latest_feature_vector(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Returns the most recent feature vector as a dictionary, useful for 
        real-time inference.
        """
        if df.empty:
            return {}
            
        full_df = self.generate_features(df)
        latest = full_df.iloc[-1]
        
        # Select numeric columns only
        features = {}
        for col in latest.index:
            if isinstance(latest[col], (int, float, np.number)) and not pd.isna(latest[col]):
                features[col] = float(latest[col])
                
        return features

# Singleton Instance
_instance = None

def get_feature_service() -> FeatureEngineeringService:
    global _instance
    if _instance is None:
        _instance = FeatureEngineeringService()
    return _instance
