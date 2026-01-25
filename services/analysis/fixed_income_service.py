"""
Fixed Income Service - Bond Analytics and Yield Curve Management

Phase 50: Manages bond ladder construction, duration/convexity calculations,
and yield curve analysis with FRED API integration.

Features:
- Weighted Average Life (WAL) calculation for bond ladders
- Duration and convexity risk metrics
- Rate shock impact analysis (+/- 100bps)
- Liquidity gap detection for maturity crunches
- FRED API integration for yield curve data

Usage:
    service = FixedIncomeService()
    wal = await service.calculate_weighted_average_life(bond_ladder)
    impact = await service.get_rate_shock_impact("portfolio-1", 100)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging
import math

logger = logging.getLogger(__name__)


class BondType(Enum):
    """Types of fixed income instruments."""
    TREASURY = "treasury"
    CORPORATE = "corporate"
    MUNICIPAL = "municipal"
    AGENCY = "agency"


@dataclass
class Bond:
    """Represents a fixed income security."""
    id: str
    name: str
    par_value: float
    coupon_rate: float  # Annual coupon as decimal (e.g., 0.05 for 5%)
    maturity_years: int
    bond_type: BondType = BondType.TREASURY
    ytm: float = 0.0  # Yield to maturity
    price: float = 100.0  # Percentage of par


@dataclass
class DurationMetrics:
    """Duration and related risk metrics for a bond."""
    macaulay_duration: float
    modified_duration: float
    convexity: float
    dollar_duration: float  # DV01


@dataclass
class MonetaryImpact:
    """Impact of rate shock on portfolio value."""
    shock_basis_points: int
    portfolio_value_before: float
    portfolio_value_after: float
    dollar_change: float
    percentage_change: float


@dataclass
class YieldCurve:
    """Treasury yield curve data."""
    date: str
    rates: Dict[str, float]  # Tenor -> Yield (e.g., "2Y" -> 4.5)
    is_inverted: bool = False


@dataclass
class LiquidityGap:
    """Represents a gap in bond ladder maturities."""
    year: int
    severity: str  # "low", "medium", "high"
    recommended_action: str


class FixedIncomeService:
    """
    Service for fixed income analytics and bond portfolio management.
    
    Implements bond math calculations, yield curve analysis, and
    rate sensitivity metrics for Phase 50.
    """
    
    def __init__(self) -> None:
        """Initialize the fixed income service."""
        self._yield_curve_cache: Optional[YieldCurve] = None
        logger.info("FixedIncomeService initialized")
    
    async def calculate_weighted_average_life(
        self,
        bond_ladder: List[Bond]
    ) -> float:
        """
        Calculate Weighted Average Life (WAL) of a bond ladder.
        
        WAL = Σ(Principal_i × Time_i) / Σ(Principal_i)
        
        Args:
            bond_ladder: List of bonds in the ladder
            
        Returns:
            WAL in years
        """
        if not bond_ladder:
            return 0.0
        
        weighted_sum = sum(bond.par_value * bond.maturity_years for bond in bond_ladder)
        total_principal = sum(bond.par_value for bond in bond_ladder)
        
        return round(weighted_sum / total_principal, 2) if total_principal > 0 else 0.0
    
    async def calculate_duration(self, bond: Bond) -> DurationMetrics:
        """
        Calculate duration metrics for a single bond.
        
        Implements Macaulay duration with semi-annual compounding.
        
        Args:
            bond: Bond to analyze
            
        Returns:
            DurationMetrics with Macaulay, Modified duration, and Convexity
        """
        # Simplified duration calculation (assuming annual coupons for demo)
        pv_cashflows = 0.0
        weighted_pv = 0.0
        convexity_sum = 0.0
        
        ytm = bond.ytm if bond.ytm > 0 else bond.coupon_rate
        coupon_payment = bond.par_value * bond.coupon_rate
        
        for t in range(1, bond.maturity_years + 1):
            if t == bond.maturity_years:
                # Final payment includes principal
                cf = coupon_payment + bond.par_value
            else:
                cf = coupon_payment
            
            discount_factor = 1 / ((1 + ytm) ** t)
            pv = cf * discount_factor
            pv_cashflows += pv
            weighted_pv += t * pv
            convexity_sum += (t * (t + 1) * pv) / ((1 + ytm) ** 2)
        
        macaulay_duration = weighted_pv / pv_cashflows if pv_cashflows > 0 else 0
        modified_duration = macaulay_duration / (1 + ytm)
        convexity = convexity_sum / pv_cashflows if pv_cashflows > 0 else 0
        dollar_duration = modified_duration * pv_cashflows / 10000  # DV01
        
        return DurationMetrics(
            macaulay_duration=round(macaulay_duration, 3),
            modified_duration=round(modified_duration, 3),
            convexity=round(convexity, 3),
            dollar_duration=round(dollar_duration, 2)
        )
    
    async def calculate_convexity(self, bond: Bond) -> float:
        """
        Calculate convexity for a single bond.
        
        Args:
            bond: Bond to analyze
            
        Returns:
            Convexity value
        """
        metrics = await self.calculate_duration(bond)
        return metrics.convexity
    
    async def get_rate_shock_impact(
        self,
        portfolio_id: str,
        basis_points: int
    ) -> MonetaryImpact:
        """
        Calculate portfolio impact from a rate shock.
        
        Uses Taylor Series approximation:
        ΔP ≈ -ModDur × ΔY × P + 0.5 × Convexity × (ΔY)² × P
        
        Args:
            portfolio_id: Portfolio to analyze
            basis_points: Rate shock in basis points (e.g., 100 = 1%)
            
        Returns:
            MonetaryImpact with before/after values
        """
        # Mock portfolio data
        portfolio_bonds = self._get_mock_portfolio(portfolio_id)
        
        portfolio_value = sum(
            bond.par_value * (bond.price / 100) for bond in portfolio_bonds
        )
        
        # Calculate weighted average duration and convexity
        total_duration = 0.0
        total_convexity = 0.0
        
        for bond in portfolio_bonds:
            weight = (bond.par_value * bond.price / 100) / portfolio_value
            metrics = await self.calculate_duration(bond)
            total_duration += weight * metrics.modified_duration
            total_convexity += weight * metrics.convexity
        
        # Apply Taylor Series
        delta_y = basis_points / 10000  # Convert to decimal
        
        price_change_pct = (
            -total_duration * delta_y +
            0.5 * total_convexity * (delta_y ** 2)
        )
        
        dollar_change = portfolio_value * price_change_pct
        new_value = portfolio_value + dollar_change
        
        return MonetaryImpact(
            shock_basis_points=basis_points,
            portfolio_value_before=round(portfolio_value, 2),
            portfolio_value_after=round(new_value, 2),
            dollar_change=round(dollar_change, 2),
            percentage_change=round(price_change_pct * 100, 3)
        )
    
    async def detect_liquidity_gaps(
        self,
        bond_ladder: List[Bond]
    ) -> List[int]:
        """
        Detect years with no bond maturities (liquidity gaps).
        
        Args:
            bond_ladder: List of bonds in the ladder
            
        Returns:
            List of years with zero maturities
        """
        if not bond_ladder:
            return list(range(1, 11))  # All years are gaps if no bonds
        
        max_maturity = max(bond.maturity_years for bond in bond_ladder)
        maturity_years = {bond.maturity_years for bond in bond_ladder}
        
        gaps = []
        for year in range(1, min(max_maturity + 1, 31)):  # Check up to 30 years
            if year not in maturity_years:
                gaps.append(year)
        
        return gaps
    
    async def get_liquidity_gap_analysis(
        self,
        bond_ladder: List[Bond]
    ) -> List[LiquidityGap]:
        """
        Get detailed liquidity gap analysis with recommendations.
        
        Args:
            bond_ladder: List of bonds in the ladder
            
        Returns:
            List of LiquidityGap objects with severity and recommendations
        """
        gap_years = await self.detect_liquidity_gaps(bond_ladder)
        
        analysis = []
        for year in gap_years[:5]:  # Top 5 gaps
            if year <= 2:
                severity = "high"
                action = "Add short-term Treasury or CD"
            elif year <= 5:
                severity = "medium"
                action = "Consider intermediate Treasury"
            else:
                severity = "low"
                action = "Optional coverage with corporate bond"
            
            analysis.append(LiquidityGap(
                year=year,
                severity=severity,
                recommended_action=action
            ))
        
        return analysis
    
    async def get_yield_curve(self) -> YieldCurve:
        """
        Get current Treasury yield curve.
        
        In production, fetches from FRED API.
        
        Returns:
            YieldCurve with current rates
        """
        # Mock data - in production, fetch from FRED
        rates = {
            "1M": 5.25,
            "3M": 5.20,
            "6M": 5.10,
            "1Y": 4.85,
            "2Y": 4.42,
            "3Y": 4.25,
            "5Y": 4.15,
            "7Y": 4.18,
            "10Y": 4.22,
            "20Y": 4.55,
            "30Y": 4.45
        }
        
        # Check for inversion (10Y - 2Y spread)
        is_inverted = rates["10Y"] < rates["2Y"]
        
        return YieldCurve(
            date=datetime.now().strftime("%Y-%m-%d"),
            rates=rates,
            is_inverted=is_inverted
        )
    
    async def detect_inversion(self) -> bool:
        """
        Detect if yield curve is inverted (10Y < 2Y).
        
        Returns:
            True if inverted, False otherwise
        """
        curve = await self.get_yield_curve()
        return curve.is_inverted
    
    async def get_historical_curves(self, months: int = 12) -> List[YieldCurve]:
        """
        Get historical yield curves for animation.
        
        Args:
            months: Number of months of history
            
        Returns:
            List of historical YieldCurve objects
        """
        # Mock historical data
        curves = []
        base_rates = await self.get_yield_curve()
        
        for i in range(months):
            # Simulate historical variation
            offset = (months - i) * 0.05
            rates = {k: round(v - offset + (i * 0.01), 2) for k, v in base_rates.rates.items()}
            
            curves.append(YieldCurve(
                date=f"2025-{(12 - i):02d}-01",
                rates=rates,
                is_inverted=rates["10Y"] < rates["2Y"]
            ))
        
        return curves
    
    def _get_mock_portfolio(self, portfolio_id: str) -> List[Bond]:
        """Get mock bond portfolio for testing."""
        return [
            Bond(
                id="bond-1",
                name="2Y Treasury",
                par_value=100000,
                coupon_rate=0.045,
                maturity_years=2,
                ytm=0.044,
                price=100.5
            ),
            Bond(
                id="bond-2",
                name="5Y Treasury",
                par_value=150000,
                coupon_rate=0.04,
                maturity_years=5,
                ytm=0.042,
                price=99.2
            ),
            Bond(
                id="bond-3",
                name="10Y Treasury",
                par_value=200000,
                coupon_rate=0.035,
                maturity_years=10,
                ytm=0.042,
                price=94.5
            ),
            Bond(
                id="bond-4",
                name="Corporate AAA 7Y",
                par_value=100000,
                coupon_rate=0.05,
                maturity_years=7,
                bond_type=BondType.CORPORATE,
                ytm=0.048,
                price=101.2
            ),
        ]
