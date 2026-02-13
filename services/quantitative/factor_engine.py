import logging
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class FactorEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FactorEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.factors = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "MOM"]
        self._initialized = True

    async def list_factors(self) -> List[Dict]:
        return [{"id": f, "name": f, "description": f"Factor {f}"} for f in self.factors]

    async def get_factor_returns(self, days: int = 30) -> List[Dict]:
        """Generate mock daily factor returns."""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            row = {"date": date}
            for f in self.factors:
                # Random daily return between -1% and +1%
                row[f] = round(np.random.normal(0.0002, 0.005), 4)
            data.append(row)
            
        return data

    async def calculate_exposure(self, ticker: str) -> Dict:
        """Mock regression for factor exposure."""
        # Deterministic random based on ticker
        seed = sum(ord(c) for c in ticker)
        random.seed(seed)
        
        exposures = {}
        for f in self.factors:
            beta = round(random.uniform(-0.5, 1.5), 2)
            if f == "Mkt-RF": beta = round(random.uniform(0.8, 1.2), 2)
            exposures[f] = beta
            
        return {
            "ticker": ticker,
            "exposures": exposures,
            "r_squared": round(random.uniform(0.6, 0.95), 2)
        }

    async def analyze_portfolio_factors(self, holdings: List[Dict]) -> Dict:
        """
        Holdings: [{"ticker": "AAPL", "weight": 0.4}, ...]
        """
        portfolio_exposures = {f: 0.0 for f in self.factors}
        total_weight = sum(h['weight'] for h in holdings)
        
        for h in holdings:
            exp = await self.calculate_exposure(h['ticker'])
            weight = h['weight'] / total_weight if total_weight > 0 else 0
            for f, beta in exp['exposures'].items():
                portfolio_exposures[f] += beta * weight
                
        return {
            "exposures": {k: round(v, 2) for k, v in portfolio_exposures.items()},
            "style": "Growth" if portfolio_exposures.get("HML", 0) < -0.2 else "Value" if portfolio_exposures.get("HML", 0) > 0.2 else "Core"
        }
