"""
==============================================================================
AI Investor - ETF Catalog Service
==============================================================================
PURPOSE:
    Manages categorization and tracking of ETF instruments by type.
    
    SUPPORTED CATEGORIES:
    
    1. VOLATILITY (VIX):
       - UVXY, VIXY, VXX, SVXY (inverse)
       - Used for hedging and volatility plays
       
    2. LEVERAGED:
       - 2x/3x Bull: TQQQ, UPRO, SPXL, SOXL
       - 2x/3x Bear: SQQQ, SPXU, SPXS, SOXS
       - Used for aggressive directional plays
       
    3. CURRENCY:
       - FXE (Euro), FXY (Yen), FXB (Pound), UUP (Dollar Bull)
       - Used for macro plays and hedging
       
    4. SECTOR:
       - XLF (Financials), XLE (Energy), XLK (Tech), XLV (Healthcare)
       - Used for sector rotation and conviction plays
       
    5. FIXED INCOME:
       - TLT (Long Treasury), HYG (High Yield), LQD (Investment Grade)
       - Used for defensive allocation and rate plays
       
    6. COMMODITIES:
       - GLD (Gold), SLV (Silver), USO (Oil), UNG (Natural Gas)
       - Used for inflation hedging and macro plays

ARCHITECTURE:
    - Static ETF database with category mappings
    - Correlation tracking between related ETFs
    - Leverage and decay characteristics for leveraged products
==============================================================================
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ETFCategory(Enum):
    """ETF category classification."""
    VOLATILITY = "volatility"           # VIX products
    LEVERAGED_BULL = "leveraged_bull"   # 2x/3x long
    LEVERAGED_BEAR = "leveraged_bear"   # 2x/3x short/inverse
    CURRENCY = "currency"               # FX ETFs
    SECTOR = "sector"                   # Sector-specific
    FIXED_INCOME = "fixed_income"       # Bonds
    COMMODITIES = "commodities"         # Gold, Oil, etc.
    BROAD_MARKET = "broad_market"       # SPY, QQQ, IWM
    INTERNATIONAL = "international"     # EEM, EFA, VWO
    THEMATIC = "thematic"               # ARK funds, clean energy


class LeverageType(Enum):
    """Leverage classification."""
    NONE = 1.0
    DOUBLE = 2.0
    TRIPLE = 3.0
    INVERSE = -1.0
    INVERSE_DOUBLE = -2.0
    INVERSE_TRIPLE = -3.0


@dataclass
class ETFInfo:
    """Information about a single ETF."""
    symbol: str
    name: str
    category: ETFCategory
    leverage: LeverageType = LeverageType.NONE
    underlying: Optional[str] = None  # What it tracks (e.g., VIX, SPX)
    expense_ratio: float = 0.0
    avg_volume: int = 0
    related_etfs: List[str] = field(default_factory=list)
    notes: str = ""


class ETFCatalog:
    """
    Catalog of ETFs organized by category.
    
    Provides lookup, filtering, and relationship mapping.
    """
    
    def __init__(self) -> None:
        """Initialize the ETF catalog with static data."""
        self.etfs: Dict[str, ETFInfo] = {}
        self._populate_catalog()
        logger.info(f"ETF Catalog initialized with {len(self.etfs)} instruments")
    
    def _populate_catalog(self) -> None:
        """Populate the catalog with known ETFs."""
        
        # -------------------------------------------------------------------
        # VOLATILITY (VIX) Products
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="UVXY",
            name="ProShares Ultra VIX Short-Term Futures",
            category=ETFCategory.VOLATILITY,
            leverage=LeverageType.DOUBLE,
            underlying="VIX",
            expense_ratio=0.95,
            related_etfs=["VIXY", "VXX", "SVXY"],
            notes="2x leveraged VIX. Decays over time. Use for short-term hedging."
        ))
        
        self._add_etf(ETFInfo(
            symbol="VIXY",
            name="ProShares VIX Short-Term Futures",
            category=ETFCategory.VOLATILITY,
            leverage=LeverageType.NONE,
            underlying="VIX",
            expense_ratio=0.87,
            related_etfs=["UVXY", "VXX", "SVXY"],
            notes="1x VIX. Less decay than UVXY."
        ))
        
        self._add_etf(ETFInfo(
            symbol="SVXY",
            name="ProShares Short VIX Short-Term Futures",
            category=ETFCategory.VOLATILITY,
            leverage=LeverageType.INVERSE,
            underlying="VIX",
            expense_ratio=0.95,
            related_etfs=["UVXY", "VIXY"],
            notes="Inverse VIX. Profits when volatility drops."
        ))
        
        # -------------------------------------------------------------------
        # LEVERAGED BULL ETFs
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="TQQQ",
            name="ProShares UltraPro QQQ",
            category=ETFCategory.LEVERAGED_BULL,
            leverage=LeverageType.TRIPLE,
            underlying="QQQ",
            expense_ratio=0.86,
            related_etfs=["QQQ", "SQQQ"],
            notes="3x NASDAQ-100. High risk, high reward."
        ))
        
        self._add_etf(ETFInfo(
            symbol="UPRO",
            name="ProShares UltraPro S&P 500",
            category=ETFCategory.LEVERAGED_BULL,
            leverage=LeverageType.TRIPLE,
            underlying="SPY",
            expense_ratio=0.91,
            related_etfs=["SPY", "SPXU"],
            notes="3x S&P 500. Daily rebalancing causes decay."
        ))
        
        self._add_etf(ETFInfo(
            symbol="SOXL",
            name="Direxion Semiconductor Bull 3X",
            category=ETFCategory.LEVERAGED_BULL,
            leverage=LeverageType.TRIPLE,
            underlying="SOXX",
            expense_ratio=0.76,
            related_etfs=["SOXX", "SOXS", "SMH"],
            notes="3x semiconductors. Great for NVDA market corner plays."
        ))
        
        # -------------------------------------------------------------------
        # LEVERAGED BEAR ETFs
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="SQQQ",
            name="ProShares UltraPro Short QQQ",
            category=ETFCategory.LEVERAGED_BEAR,
            leverage=LeverageType.INVERSE_TRIPLE,
            underlying="QQQ",
            expense_ratio=0.95,
            related_etfs=["QQQ", "TQQQ"],
            notes="3x inverse NASDAQ. Use for hedging tech exposure."
        ))
        
        self._add_etf(ETFInfo(
            symbol="SPXU",
            name="ProShares UltraPro Short S&P 500",
            category=ETFCategory.LEVERAGED_BEAR,
            leverage=LeverageType.INVERSE_TRIPLE,
            underlying="SPY",
            expense_ratio=0.91,
            related_etfs=["SPY", "UPRO"],
            notes="3x inverse S&P. For defensive hedging."
        ))
        
        self._add_etf(ETFInfo(
            symbol="SOXS",
            name="Direxion Semiconductor Bear 3X",
            category=ETFCategory.LEVERAGED_BEAR,
            leverage=LeverageType.INVERSE_TRIPLE,
            underlying="SOXX",
            expense_ratio=0.99,
            related_etfs=["SOXX", "SOXL"],
            notes="3x inverse semiconductors."
        ))
        
        # -------------------------------------------------------------------
        # CURRENCY ETFs
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="UUP",
            name="Invesco DB US Dollar Index Bullish",
            category=ETFCategory.CURRENCY,
            leverage=LeverageType.NONE,
            underlying="DXY",
            expense_ratio=0.79,
            related_etfs=["UDN", "FXE", "FXY"],
            notes="Dollar bull. Profits when USD strengthens."
        ))
        
        self._add_etf(ETFInfo(
            symbol="FXE",
            name="Invesco CurrencyShares Euro Trust",
            category=ETFCategory.CURRENCY,
            leverage=LeverageType.NONE,
            underlying="EUR/USD",
            expense_ratio=0.40,
            related_etfs=["UUP", "FXY", "FXB"],
            notes="Euro exposure vs USD."
        ))
        
        self._add_etf(ETFInfo(
            symbol="FXY",
            name="Invesco CurrencyShares Japanese Yen Trust",
            category=ETFCategory.CURRENCY,
            leverage=LeverageType.NONE,
            underlying="JPY/USD",
            expense_ratio=0.40,
            related_etfs=["UUP", "FXE"],
            notes="Yen exposure. Safe haven play."
        ))
        
        # -------------------------------------------------------------------
        # SECTOR ETFs
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="XLK",
            name="Technology Select Sector SPDR",
            category=ETFCategory.SECTOR,
            leverage=LeverageType.NONE,
            underlying="S&P 500 Tech",
            expense_ratio=0.10,
            related_etfs=["QQQ", "VGT", "TECL"],
            notes="Tech sector. AAPL, MSFT heavy."
        ))
        
        self._add_etf(ETFInfo(
            symbol="XLF",
            name="Financial Select Sector SPDR",
            category=ETFCategory.SECTOR,
            leverage=LeverageType.NONE,
            underlying="S&P 500 Financials",
            expense_ratio=0.10,
            related_etfs=["KRE", "KBE"],
            notes="Financials sector. Banks, insurance."
        ))
        
        self._add_etf(ETFInfo(
            symbol="XLE",
            name="Energy Select Sector SPDR",
            category=ETFCategory.SECTOR,
            leverage=LeverageType.NONE,
            underlying="S&P 500 Energy",
            expense_ratio=0.10,
            related_etfs=["OIH", "XOP", "USO"],
            notes="Energy sector. Oil, gas."
        ))
        
        self._add_etf(ETFInfo(
            symbol="XLV",
            name="Health Care Select Sector SPDR",
            category=ETFCategory.SECTOR,
            leverage=LeverageType.NONE,
            underlying="S&P 500 Healthcare",
            expense_ratio=0.10,
            related_etfs=["IBB", "XBI"],
            notes="Healthcare. Pharma, biotech, hospitals."
        ))
        
        # -------------------------------------------------------------------
        # BROAD MARKET ETFs
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="SPY",
            name="SPDR S&P 500 ETF",
            category=ETFCategory.BROAD_MARKET,
            leverage=LeverageType.NONE,
            underlying="S&P 500",
            expense_ratio=0.09,
            related_etfs=["IVV", "VOO", "UPRO", "SPXU"],
            notes="Most liquid ETF. Core holding."
        ))
        
        self._add_etf(ETFInfo(
            symbol="QQQ",
            name="Invesco QQQ Trust",
            category=ETFCategory.BROAD_MARKET,
            leverage=LeverageType.NONE,
            underlying="NASDAQ-100",
            expense_ratio=0.20,
            related_etfs=["TQQQ", "SQQQ"],
            notes="Tech-heavy NASDAQ. Growth exposure."
        ))
        
        # -------------------------------------------------------------------
        # COMMODITIES
        # -------------------------------------------------------------------
        self._add_etf(ETFInfo(
            symbol="GLD",
            name="SPDR Gold Shares",
            category=ETFCategory.COMMODITIES,
            leverage=LeverageType.NONE,
            underlying="Gold",
            expense_ratio=0.40,
            related_etfs=["IAU", "SLV", "GDX"],
            notes="Gold exposure. Inflation/crisis hedge."
        ))
        
        self._add_etf(ETFInfo(
            symbol="USO",
            name="United States Oil Fund",
            category=ETFCategory.COMMODITIES,
            leverage=LeverageType.NONE,
            underlying="WTI Crude",
            expense_ratio=0.79,
            related_etfs=["XLE", "OIH", "UNG"],
            notes="Oil exposure. Contango decay issues."
        ))
    
    def _add_etf(self, etf: ETFInfo) -> None:
        """Add an ETF to the catalog."""
        self.etfs[etf.symbol] = etf
    
    def get(self, symbol: str) -> Optional[ETFInfo]:
        """Get ETF info by symbol."""
        return self.etfs.get(symbol.upper())
    
    def get_by_category(self, category: ETFCategory) -> List[ETFInfo]:
        """Get all ETFs in a category."""
        return [e for e in self.etfs.values() if e.category == category]
    
    def get_volatility_products(self) -> List[ETFInfo]:
        """Get all VIX/volatility products."""
        return self.get_by_category(ETFCategory.VOLATILITY)
    
    def get_leveraged_products(self) -> List[ETFInfo]:
        """Get all leveraged (bull and bear) products."""
        bull = self.get_by_category(ETFCategory.LEVERAGED_BULL)
        bear = self.get_by_category(ETFCategory.LEVERAGED_BEAR)
        return bull + bear
    
    def get_currency_products(self) -> List[ETFInfo]:
        """Get all currency ETFs."""
        return self.get_by_category(ETFCategory.CURRENCY)
    
    def get_hedge_candidates(self) -> List[ETFInfo]:
        """Get ETFs suitable for hedging (volatility + inverse)."""
        vol = self.get_by_category(ETFCategory.VOLATILITY)
        bear = self.get_by_category(ETFCategory.LEVERAGED_BEAR)
        return vol + bear
    
    def get_aggressive_candidates(self) -> List[ETFInfo]:
        """Get ETFs suitable for aggressive plays (leveraged bull)."""
        return self.get_by_category(ETFCategory.LEVERAGED_BULL)
    
    def get_related(self, symbol: str) -> List[ETFInfo]:
        """Get related ETFs for a given symbol."""
        etf = self.get(symbol)
        if not etf:
            return []
        
        return [self.etfs[s] for s in etf.related_etfs if s in self.etfs]
    
    def get_inverse_pair(self, symbol: str) -> Optional[ETFInfo]:
        """Get the inverse ETF for a given symbol."""
        etf = self.get(symbol)
        if not etf:
            return None
        
        for related_symbol in etf.related_etfs:
            related = self.get(related_symbol)
            if related and self._is_inverse_pair(etf, related):
                return related
        
        return None
    
    def _is_inverse_pair(self, etf1: ETFInfo, etf2: ETFInfo) -> bool:
        """Check if two ETFs are inverse pairs."""
        if etf1.underlying != etf2.underlying:
            return False
        
        # One should be positive leverage, other negative
        lev1 = etf1.leverage.value
        lev2 = etf2.leverage.value
        
        return (lev1 > 0 and lev2 < 0) or (lev1 < 0 and lev2 > 0)
    
    def list_all(self) -> List[str]:
        """List all ETF symbols in the catalog."""
        return list(self.etfs.keys())
    
    def get_summary(self) -> Dict[str, int]:
        """Get count of ETFs by category."""
        summary = {}
        for category in ETFCategory:
            count = len(self.get_by_category(category))
            if count > 0:
                summary[category.value] = count
        return summary
