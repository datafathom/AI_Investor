import logging
import random
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class HeatmapGenerator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HeatmapGenerator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

    async def get_correlation_heatmap(self, tickers: List[str] = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX"]) -> Dict:
        """Generate correlation matrix for a list of tickers (mocked for now)."""
        size = len(tickers)
        # Generate a random correlation matrix
        # 1.0 on diagonal, symmetric, values between -1 and 1
        matrix = np.eye(size)
        
        for i in range(size):
            for j in range(i + 1, size):
                # Random correlation between -0.5 and 0.95
                corr = random.uniform(-0.5, 0.95)
                # Tech stocks highly correlated
                if i < 4 and j < 4:
                     corr = random.uniform(0.6, 0.9)
                
                matrix[i][j] = corr
                matrix[j][i] = corr
                
        return {
            "tickers": tickers,
            "matrix": matrix.tolist()
        }

    async def get_sector_heatmap(self) -> Dict:
        """Generate sector performance heatmap data."""
        sectors = [
            "Technology", "Healthcare", "Financials", "Consumer Discretionary", 
            "Communication Services", "Industrials", "Consumer Staples", 
            "Energy", "Utilities", "Real Estate", "Materials"
        ]
        
        data = []
        for sector in sectors:
            # Random performance per sector
            perf = random.uniform(-3.0, 3.0)
            
            # Generate stocks within sector
            num_stocks = random.randint(5, 12)
            stocks = []
            for k in range(num_stocks):
                stocks.append({
                    "ticker": f"{sector[:3].upper()}{k}",
                    "change": perf + random.uniform(-1.0, 1.0),
                    "market_cap": random.uniform(10, 500) # Billion
                })
            
            data.append({
                "name": sector,
                "performance": perf,
                "stocks": stocks
            })
            
        return {"sectors": data}
