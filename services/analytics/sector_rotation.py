import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SectorRotationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SectorRotationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.sectors = [
            "Technology", "Healthcare", "Financials", "Energy", 
            "Consumer Discretionary", "Consumer Staples", "Industrials", 
            "Utilities", "Real Estate", "Materials", "Communication Services"
        ]
        self._initialized = True

    async def get_sector_performance(self) -> List[Dict]:
        """Mock sector performance."""
        performance = []
        for s in self.sectors:
            # Random performance with some correlation to "cycle"
            seed = sum(ord(c) for c in s) + datetime.now().day
            random.seed(seed)
            
            performance.append({
                "sector": s,
                "return_1m": round(random.uniform(-0.05, 0.08), 4),
                "return_3m": round(random.uniform(-0.10, 0.15), 4),
                "return_6m": round(random.uniform(-0.15, 0.20), 4),
                "return_1y": round(random.uniform(-0.20, 0.30), 4),
            })
        
        return sorted(performance, key=lambda x: x['return_3m'], reverse=True)

    async def get_business_cycle_phase(self) -> Dict:
        """Mock business cycle phase."""
        phases = ["Early Cycle", "Mid Cycle", "Late Cycle", "Recession"]
        # Simulate phase based on month
        current_month = datetime.now().month
        phase_idx = (current_month // 3) % 4
        
        return {
            "phase": phases[phase_idx],
            "description": "Growth is slowing, inflation remains potential risk. favoring defensive sectors.",
            "confidence": 0.75
        }

    async def get_rotation_signals(self) -> Dict:
        """Mock rotation signals."""
        phase_data = await self.get_business_cycle_phase()
        phase = phase_data['phase']
        
        into = []
        out = []
        
        if phase == "Early Cycle":
            into = ["Financials", "Real Estate", "Consumer Discretionary"]
            out = ["Utilities", "Healthcare"]
        elif phase == "Mid Cycle":
            into = ["Technology", "Industrials"]
            out = ["Materials"]
        elif phase == "Late Cycle":
            into = ["Energy", "Materials", "Healthcare"]
            out = ["Technology", "Consumer Discretionary"]
        else: # Recession
            into = ["Utilities", "Consumer Staples", "Healthcare"]
            out = ["Industrials", "Financials", "Energy"]
            
        return {
            "phase": phase,
            "rotate_into": into,
            "rotate_out_of": out,
            "rationale": f"Based on {phase} dynamics, capital is shifting towards safer yields and inflation hedges."
        }

    async def get_sector_rotation(self) -> Dict:
        """Combined data for widget."""
        perf = await self.get_sector_performance()
        signals = await self.get_rotation_signals()
        
        return {
            "performance": perf,
            "signals": signals
        }
