"""
Futures Service - Commodity Term Structure Analysis

Phase 53: Provides futures curve data with contango/backwardation detection
and roll yield calculations.

Features:
- Futures curve visualization
- Contango/Backwardation detection
- Roll yield calculation
- Crack spread analysis (Oil/Gas)

Usage:
    service = FuturesService()
    curve = await service.get_futures_curve("CL")
    is_contango = await service.detect_contango(curve)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Commodity(Enum):
    """Supported commodity futures."""
    CRUDE_OIL = "CL"
    NATURAL_GAS = "NG"
    GOLD = "GC"
    SILVER = "SI"
    COPPER = "HG"
    CORN = "ZC"
    SOYBEANS = "ZS"
    WHEAT = "ZW"


@dataclass
class FuturesContract:
    """Single futures contract."""
    symbol: str
    expiry_date: str
    price: float
    volume: int
    open_interest: int


@dataclass
class FuturesCurve:
    """Complete futures curve for a commodity."""
    commodity: str
    commodity_name: str
    contracts: List[FuturesContract]
    spot_price: float
    curve_shape: str  # "contango", "backwardation", "flat"
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SpreadData:
    """Spread calculation between related commodities."""
    name: str
    value: float
    historical_mean: float
    z_score: float
    components: Dict[str, float]


class FuturesService:
    """
    Service for commodity futures analysis.
    
    Provides curve shape analysis, roll yield calculations,
    and spread monitoring.
    """
    
    def __init__(self) -> None:
        """Initialize the futures service."""
        logger.info("FuturesService initialized")
    
    async def get_futures_curve(self, commodity: str) -> FuturesCurve:
        """
        Get complete futures curve for a commodity.
        
        Args:
            commodity: Commodity symbol (e.g., "CL" for crude oil)
            
        Returns:
            FuturesCurve with all contracts
        """
        # Mock futures data
        commodity_data = {
            "CL": ("Crude Oil", 72.50, True),  # Contango
            "NG": ("Natural Gas", 2.85, False),  # Backwardation
            "GC": ("Gold", 2050.0, True),
            "SI": ("Silver", 24.50, True),
        }
        
        name, spot, is_contango = commodity_data.get(commodity.upper(), ("Unknown", 100.0, True))
        
        # Generate mock curve
        contracts = []
        months = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]
        base_year = 26
        
        for i, month in enumerate(months[:6]):  # 6 months out
            if is_contango:
                price = spot * (1 + 0.005 * (i + 1))  # +0.5% per month
            else:
                price = spot * (1 - 0.01 * (i + 1))  # -1% per month
            
            contracts.append(FuturesContract(
                symbol=f"{commodity.upper()}{month}{base_year}",
                expiry_date=f"2026-{(i + 1):02d}-15",
                price=round(price, 2),
                volume=50000 - (i * 5000),
                open_interest=100000 - (i * 10000)
            ))
        
        return FuturesCurve(
            commodity=commodity.upper(),
            commodity_name=name,
            contracts=contracts,
            spot_price=spot,
            curve_shape="contango" if is_contango else "backwardation"
        )
    
    async def detect_contango(self, curve: FuturesCurve) -> bool:
        """
        Detect if curve is in contango.
        
        Contango = futures price > spot price (upward sloping curve).
        
        Args:
            curve: FuturesCurve to analyze
            
        Returns:
            True if in contango
        """
        if not curve.contracts:
            return False
        
        front_month = curve.contracts[0].price
        return front_month > curve.spot_price
    
    def detect_backwardation(self, curve: FuturesCurve) -> bool:
        """
        Detect if curve is in backwardation.
        
        Backwardation = futures price < spot price (downward sloping curve).
        """
        if not curve.contracts:
            return False
        
        front_month = curve.contracts[0].price
        return front_month < curve.spot_price
    
    async def calculate_roll_yield(self, curve: FuturesCurve) -> float:
        """
        Calculate implied roll yield from futures curve.
        
        Roll yield is profit/loss from rolling futures contracts.
        Positive in backwardation, negative in contango.
        
        Args:
            curve: FuturesCurve to analyze
            
        Returns:
            Annualized roll yield percentage
        """
        if len(curve.contracts) < 2:
            return 0.0
        
        front = curve.contracts[0].price
        second = curve.contracts[1].price
        
        # Monthly roll return
        monthly_return = (front - second) / front
        
        # Annualize (12 months)
        annual_yield = monthly_return * 12 * 100
        
        return round(annual_yield, 2)
    
    async def calculate_crack_spread(self) -> SpreadData:
        """
        Calculate 3-2-1 crack spread (Oil/Gasoline/Heating Oil).
        
        Crack spread = (2 * Gasoline + 1 * Heating Oil - 3 * Crude) / 3
        
        Returns:
            SpreadData with current and historical values
        """
        # Mock crack spread data
        crude = 72.50
        gasoline = 2.15 * 42  # Convert to $/bbl
        heating_oil = 2.35 * 42
        
        crack_spread = (2 * gasoline + heating_oil - 3 * crude) / 3
        historical_mean = 20.0  # $20/bbl average
        
        z_score = (crack_spread - historical_mean) / 8.0  # Assume $8 std dev
        
        return SpreadData(
            name="3-2-1 Crack Spread",
            value=round(crack_spread, 2),
            historical_mean=historical_mean,
            z_score=round(z_score, 2),
            components={
                "crude_oil": crude,
                "gasoline": gasoline,
                "heating_oil": heating_oil
            }
        )
    
    async def get_all_curves(self) -> List[FuturesCurve]:
        """Get curves for all major commodities."""
        commodities = ["CL", "NG", "GC", "SI"]
        curves = []
        
        for commodity in commodities:
            curve = await self.get_futures_curve(commodity)
            curves.append(curve)
        
        return curves
    
    def get_supported_commodities(self) -> List[Dict[str, str]]:
        """Get list of supported commodities."""
        return [
            {"symbol": "CL", "name": "Crude Oil", "sector": "Energy"},
            {"symbol": "NG", "name": "Natural Gas", "sector": "Energy"},
            {"symbol": "GC", "name": "Gold", "sector": "Metals"},
            {"symbol": "SI", "name": "Silver", "sector": "Metals"},
            {"symbol": "HG", "name": "Copper", "sector": "Metals"},
            {"symbol": "ZC", "name": "Corn", "sector": "Agriculture"},
            {"symbol": "ZS", "name": "Soybeans", "sector": "Agriculture"},
            {"symbol": "ZW", "name": "Wheat", "sector": "Agriculture"},
        ]
