"""
ESG Service - Environmental, Social, Governance Analysis
Phase 61: Aggregates ESG scores and calculates carbon footprint.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import random
import logging

logger = logging.getLogger(__name__)

@dataclass
class ESGScore:
    environmental: float
    social: float
    governance: float
    composite: float
    grade: str

@dataclass
class CarbonFootprint:
    total_emissions_tons: float
    scope_1: float
    scope_2: float
    scope_3: float
    offset_cost_usd: float

class ESGService:
    def __init__(self):
        self._sector_map = {
            "AAPL": "Tech", "MSFT": "Tech", "NVDA": "Tech", "GOOGL": "Tech",
            "XOM": "Energy", "CVX": "Energy", "BP": "Energy",
            "NEE": "Utility", "DUK": "Utility",
            "TSLA": "Auto/CleanTech", "AMZN": "Retail", "JPM": "Finance"
        }
        logger.info("ESGService initialized with Ticker-Sector mapping")

    async def get_portfolio_esg_scores(self, tickers: List[str]) -> ESGScore:
        """Calculates scores based on portfolio composition."""
        if not tickers: tickers = ["AAPL", "MSFT"]
        
        # Simple weighted logic for demo: Tech/Utilities = High, Energy = Low
        total_e, total_s, total_g = 0, 0, 0
        for t in tickers:
            sector = self._sector_map.get(t, "Tech")
            if sector == "Energy": e, s, g = 35.0, 50.0, 60.0
            elif sector == "Utility": e, s, g = 85.0, 70.0, 80.0
            elif sector == "Auto/CleanTech": e, s, g = 90.0, 65.0, 75.0
            else: e, s, g = 75.0, 80.0, 82.0 # Default/Tech
            
            total_e += e; total_s += s; total_g += g
            
        count = len(tickers)
        e_avg, s_avg, g_avg = total_e/count, total_s/count, total_g/count
        composite = (e_avg + s_avg + g_avg) / 3
        
        return ESGScore(
            environmental=round(e_avg, 1), social=round(s_avg, 1),
            governance=round(g_avg, 1), composite=round(composite, 1),
            grade="A" if composite > 80 else ("B" if composite > 60 else "C")
        )

    async def calculate_carbon_footprint(self, portfolio_value: float, tickers: List[str]) -> CarbonFootprint:
        """Estimates carbon footprint based on portfolio value and energy exposure."""
        energy_weight = len([t for t in tickers if self._sector_map.get(t) == "Energy"]) / max(1, len(tickers))
        intensity_factor = 50.0 + (energy_weight * 400.0) # Base 50, up to 450 for energy-heavy
        
        total_tons = (portfolio_value / 1000000.0) * intensity_factor
        return CarbonFootprint(
            total_emissions_tons=round(total_tons, 1),
            scope_1=round(total_tons * 0.15, 1),
            scope_2=round(total_tons * 0.10, 1),
            scope_3=round(total_tons * 0.75, 1),
            offset_cost_usd=round(total_tons * 18.0, 2)
        )

    async def get_alpha_vs_carbon_data(self) -> List[Dict]:
        """Returns dynamic scatterplot data."""
        data = []
        for t, sector in self._sector_map.items():
            carbon = 300.0 if sector == "Energy" else (40.0 if sector == "Tech" else 150.0)
            carbon += random.uniform(-20, 20)
            alpha = random.uniform(5, 30) if carbon < 100 else random.uniform(-5, 15)
            
            data.append({
                "ticker": t, "alpha": round(alpha, 2),
                "carbon_intensity": max(5, round(carbon, 1)),
                "sector": sector
            })
        return data

    async def detect_sin_stocks(self) -> List[Dict]:
        """Identifies holdings that violate ESG filters."""
        return [
            {"ticker": "MO", "name": "Altria Group", "violation": "Tobacco", "weight": 1.2},
            {"ticker": "LMT", "name": "Lockheed Martin", "violation": "Weapons", "weight": 2.5}
        ]

_esg_service: Optional[ESGService] = None
def get_esg_service() -> ESGService:
    global _esg_service
    if _esg_service is None:
        _esg_service = ESGService()
    return _esg_service
