"""
Macro Service - Global Economic & Political Data Aggregation

Phase 53: Aggregates macroeconomic indicators, political insider trading,
and commodity data for the world map visualization.

Features:
- Political insider trading detection
- Regional CPI data per country
- Inflation hedge correlations
- Real-time economic indicator updates

Usage:
    service = MacroService()
    trades = await service.get_political_insider_trades("US")
    cpi = await service.get_regional_cpi("USA")
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Region(Enum):
    """Global regions."""
    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    LATIN_AMERICA = "latin_america"
    MIDDLE_EAST = "middle_east"


@dataclass
class InsiderTrade:
    """Political insider trading record."""
    politician: str
    party: str
    country: str
    ticker: str
    action: str  # "BUY" or "SELL"
    amount: float
    trade_date: str
    disclosure_date: str
    delay_days: int


@dataclass
class CPIData:
    """Consumer Price Index data for a country."""
    country_code: str
    country_name: str
    current_cpi: float
    yoy_change: float
    core_cpi: float
    updated_at: str


@dataclass
class CorrelationMatrix:
    """Asset correlation matrix for inflation hedging."""
    assets: List[str]
    correlations: Dict[str, Dict[str, float]]
    best_hedge: str
    worst_hedge: str


@dataclass
class EconomicIndicator:
    """Generic economic indicator."""
    name: str
    value: float
    previous: float
    change_percent: float
    country: str
    updated_at: str


from services.data.fred_service import FredMacroService
from config.environment_manager import get_settings

from services.system.api_governance import get_governor

class MacroService:
    """
    Service for macroeconomic data aggregation.
    """
    
    def __init__(self, fred_service: Optional[FredMacroService] = None) -> None:
        """Initialize the macro service."""
        settings = get_settings()
        self._fred = fred_service or FredMacroService(
            api_key=settings.FRED_API_KEY,
            mock=(not settings.FRED_API_KEY or settings.FRED_API_KEY == "your_fred_api_key_here")
        )
        self._governor = get_governor()
        self._indicators: Dict[str, List[EconomicIndicator]] = {}
        logger.info(f"MacroService initialized (FRED Mock: {self._fred.mock})")
    
    async def get_political_insider_trades(
        self,
        region: Optional[str] = None
    ) -> List[InsiderTrade]:
        """Get recent political insider trading data (Mock for now)."""
        # Mock remain for this complex data source
        trades = [
            InsiderTrade("Sen. Example", "D", "USA", "NVDA", "BUY", 50000.0, "2025-12-01", "2025-12-15", 14),
            InsiderTrade("Rep. Sample", "R", "USA", "MSFT", "SELL", 100000.0, "2025-11-20", "2025-12-10", 20),
            InsiderTrade("MP Smith", "Conservative", "UK", "BP", "BUY", 25000.0, "2025-12-05", "2025-12-12", 7),
        ]
        if region:
            r = region.lower()
            if r in ["us", "usa", "north_america"]: trades = [t for t in trades if t.country == "USA"]
            elif r in ["uk", "europe"]: trades = [t for t in trades if t.country in ["UK", "Germany"]]
        return trades
    
    async def get_regional_cpi(self, country_code: str) -> CPIData:
        """Get CPI data, pulling from FRED for USA if available."""
        if country_code.upper() == "USA" and not self._fred.mock:
            await self._governor.wait_for_slot("FRED")
            try:
                regime = self._fred.get_macro_regime()
                self._governor.report_usage("FRED")
                cpi_val = regime["metrics"].get("INFLATION", 312.0)
                return CPIData("USA", "United States", cpi_val, 3.2, 295.0, datetime.now().isoformat())
            except Exception as e:
                logger.error(f"FRED regime fetch failed: {e}")
            
        # Mock CPI data for others
        cpi_data = {
            "USA": CPIData("USA", "United States", 312.0, 3.2, 295.0, datetime.now().isoformat()),
            "UK": CPIData("UK", "United Kingdom", 134.5, 4.1, 128.0, datetime.now().isoformat()),
            "EU": CPIData("EU", "European Union", 122.8, 2.8, 118.5, datetime.now().isoformat()),
        }
        return cpi_data.get(country_code.upper(), CPIData(country_code, country_code, 100.0, 0.0, 100.0, datetime.now().isoformat()))
    
    async def get_inflation_hedge_correlations(self) -> CorrelationMatrix:
        """Get correlation matrix."""
        assets = ["GLD", "TIP", "REIT", "BTC", "Oil", "Stocks"]
        correlations = {
            "GLD": {"CPI": 0.72}, "TIP": {"CPI": 0.85}, "REIT": {"CPI": 0.55},
            "BTC": {"CPI": 0.30}, "Oil": {"CPI": 0.80}, "Stocks": {"CPI": 0.40}
        }
        return CorrelationMatrix(assets=assets, correlations=correlations, best_hedge="TIP", worst_hedge="BTC")
    
    async def get_world_map_data(self) -> Dict[str, Dict]:
        """Get world map data, using FRED for USA metrics."""
        base_data = {
            "USA": {"cpi": 3.2, "gdp_growth": 2.4, "unemployment": 3.7, "sentiment": "bullish"},
            "UK": {"cpi": 4.1, "gdp_growth": 1.2, "unemployment": 4.2, "sentiment": "neutral"},
            "EU": {"cpi": 2.8, "gdp_growth": 0.8, "unemployment": 6.0, "sentiment": "bearish"},
        }
        
        if not self._fred.mock:
            await self._governor.wait_for_slot("FRED")
            try:
                regime = self._fred.get_macro_regime()
                self._governor.report_usage("FRED")
                base_data["USA"]["unemployment"] = regime["metrics"].get("UNEMPLOYMENT", 3.7)
            except Exception as e:
                logger.error(f"FRED world map update failed: {e}")
            
        return base_data
    
    async def get_economic_calendar(self, days_ahead: int = 7) -> List[Dict]:
        """Upcoming events."""
        return [{"date": "2026-01-20", "event": "Fed Rate Decision", "country": "USA", "importance": "high"}]
