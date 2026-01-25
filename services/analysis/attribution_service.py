"""
Attribution Service - Brinson-Fachler Performance Decomposition

This service calculates portfolio performance attribution using the 
Brinson-Fachler model, decomposing returns into Allocation, Selection, 
and Interaction effects relative to benchmarks.

Key Features:
- Calculates sector-level allocation effect (overweight/underweight impact)
- Calculates selection effect (stock picking within sectors)
- Calculates interaction effect (combined allocation and selection)
- Detects regime shifts when strategy decouples from benchmark

Usage:
    service = AttributionService()
    result = await service.calculate_brinson_attribution(
        portfolio_id="user-portfolio-1",
        benchmark_id="sp500",
        period=DateRange(start="2025-01-01", end="2025-12-31")
    )
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class BenchmarkType(Enum):
    """Supported benchmark indices for attribution analysis."""
    SP500 = "sp500"
    NASDAQ = "nasdaq"
    CUSTOM = "custom"


@dataclass
class DateRange:
    """Date range for attribution period."""
    start: str
    end: str


@dataclass
class SectorAttribution:
    """Attribution breakdown for a single GICS sector."""
    sector: str
    allocation_effect: float  # Basis points
    selection_effect: float   # Basis points
    interaction_effect: float # Basis points
    portfolio_weight: float   # Percentage
    benchmark_weight: float   # Percentage
    portfolio_return: float   # Percentage
    benchmark_return: float   # Percentage


@dataclass
class RegimeShiftEvent:
    """Detected period of strategy-benchmark decoupling."""
    start_date: str
    end_date: str
    correlation_before: float
    correlation_during: float
    impact_basis_points: float
    description: str


@dataclass
class BrinsonAttribution:
    """Complete Brinson-Fachler attribution result."""
    portfolio_id: str
    benchmark_id: str
    period: DateRange
    total_active_return: float  # Basis points
    total_allocation_effect: float
    total_selection_effect: float
    total_interaction_effect: float
    sector_attributions: List[SectorAttribution] = field(default_factory=list)
    regime_shifts: List[RegimeShiftEvent] = field(default_factory=list)
    calculated_at: str = field(default_factory=lambda: datetime.now().isoformat())


# GICS Sector mapping for attribution analysis
GICS_SECTORS = [
    "Information Technology",
    "Health Care",
    "Financials",
    "Consumer Discretionary",
    "Communication Services",
    "Industrials",
    "Consumer Staples",
    "Energy",
    "Utilities",
    "Real Estate",
    "Materials"
]


class AttributionService:
    """
    Service for calculating portfolio performance attribution.
    
    Implements the Brinson-Fachler model to decompose active returns
    into allocation, selection, and interaction effects.
    """
    
    def __init__(self) -> None:
        """Initialize the attribution service."""
        self._benchmarks: Dict[str, Dict] = self._load_benchmark_data()
        logger.info("AttributionService initialized")
    
    def _load_benchmark_data(self) -> Dict[str, Dict]:
        """Load benchmark sector weights and returns."""
        # Mock data for initial implementation
        # In production, this would fetch from a data provider
        return {
            "sp500": {
                "name": "S&P 500",
                "sectors": {
                    "Information Technology": {"weight": 0.28, "return": 0.25},
                    "Health Care": {"weight": 0.13, "return": 0.08},
                    "Financials": {"weight": 0.12, "return": 0.15},
                    "Consumer Discretionary": {"weight": 0.10, "return": 0.18},
                    "Communication Services": {"weight": 0.09, "return": 0.22},
                    "Industrials": {"weight": 0.08, "return": 0.12},
                    "Consumer Staples": {"weight": 0.07, "return": 0.05},
                    "Energy": {"weight": 0.05, "return": -0.02},
                    "Utilities": {"weight": 0.03, "return": 0.04},
                    "Real Estate": {"weight": 0.03, "return": 0.03},
                    "Materials": {"weight": 0.02, "return": 0.10},
                }
            },
            "nasdaq": {
                "name": "NASDAQ Composite",
                "sectors": {
                    "Information Technology": {"weight": 0.45, "return": 0.28},
                    "Health Care": {"weight": 0.10, "return": 0.10},
                    "Consumer Discretionary": {"weight": 0.15, "return": 0.20},
                    "Communication Services": {"weight": 0.12, "return": 0.25},
                    "Financials": {"weight": 0.05, "return": 0.12},
                    "Industrials": {"weight": 0.05, "return": 0.14},
                    "Consumer Staples": {"weight": 0.03, "return": 0.06},
                    "Energy": {"weight": 0.02, "return": -0.01},
                    "Utilities": {"weight": 0.01, "return": 0.03},
                    "Real Estate": {"weight": 0.01, "return": 0.02},
                    "Materials": {"weight": 0.01, "return": 0.08},
                }
            }
        }
    
    async def calculate_brinson_attribution(
        self,
        portfolio_id: str,
        benchmark_id: str,
        period: DateRange
    ) -> BrinsonAttribution:
        """
        Calculate full Brinson-Fachler attribution for a portfolio.
        
        Args:
            portfolio_id: Unique identifier for the portfolio
            benchmark_id: Benchmark to compare against (sp500, nasdaq, custom)
            period: Date range for attribution analysis
            
        Returns:
            BrinsonAttribution with complete decomposition
        """
        logger.info(f"Calculating attribution for {portfolio_id} vs {benchmark_id}")
        
        # Get benchmark data
        benchmark = self._benchmarks.get(benchmark_id)
        if not benchmark:
            # Fallback to default if specified benchmark not found
            benchmark = self._benchmarks.get("sp500", list(self._benchmarks.values())[0])
        
        # Mock portfolio data - in production, fetch from portfolio service
        portfolio_sectors = self._get_mock_portfolio_data(portfolio_id)
        
        # Calculate attribution for each sector
        sector_attributions: List[SectorAttribution] = []
        total_allocation = 0.0
        total_selection = 0.0
        total_interaction = 0.0
        
        for sector in GICS_SECTORS:
            benchmark_data = benchmark["sectors"].get(sector, {"weight": 0, "return": 0})
            portfolio_data = portfolio_sectors.get(sector, {"weight": 0, "return": 0})
            
            # Brinson-Fachler formulas
            w_p = portfolio_data["weight"]
            w_b = benchmark_data["weight"]
            r_p = portfolio_data["return"]
            r_b = benchmark_data["return"]
            
            # Calculate benchmark total return for allocation effect
            benchmark_total_return = sum(
                s["weight"] * s["return"] 
                for s in benchmark["sectors"].values()
            )
            
            allocation_effect = (w_p - w_b) * (r_b - benchmark_total_return) * 10000
            selection_effect = w_b * (r_p - r_b) * 10000
            interaction_effect = (w_p - w_b) * (r_p - r_b) * 10000
            
            total_allocation += allocation_effect
            total_selection += selection_effect
            total_interaction += interaction_effect
            
            sector_attributions.append(SectorAttribution(
                sector=sector,
                allocation_effect=round(allocation_effect, 2),
                selection_effect=round(selection_effect, 2),
                interaction_effect=round(interaction_effect, 2),
                portfolio_weight=round(w_p * 100, 2),
                benchmark_weight=round(w_b * 100, 2),
                portfolio_return=round(r_p * 100, 2),
                benchmark_return=round(r_b * 100, 2)
            ))
        
        # Detect regime shifts
        regime_shifts = await self.detect_regime_shift(portfolio_id, benchmark_id)
        
        return BrinsonAttribution(
            portfolio_id=portfolio_id,
            benchmark_id=benchmark_id,
            period=period,
            total_active_return=round(total_allocation + total_selection + total_interaction, 2),
            total_allocation_effect=round(total_allocation, 2),
            total_selection_effect=round(total_selection, 2),
            total_interaction_effect=round(total_interaction, 2),
            sector_attributions=sector_attributions,
            regime_shifts=regime_shifts
        )
    
    def _get_mock_portfolio_data(self, portfolio_id: str) -> Dict[str, Dict]:
        """Get mock portfolio sector weights and returns."""
        # Mock data - in production, fetch from database
        return {
            "Information Technology": {"weight": 0.35, "return": 0.30},
            "Health Care": {"weight": 0.12, "return": 0.10},
            "Financials": {"weight": 0.08, "return": 0.18},
            "Consumer Discretionary": {"weight": 0.12, "return": 0.22},
            "Communication Services": {"weight": 0.10, "return": 0.20},
            "Industrials": {"weight": 0.08, "return": 0.15},
            "Consumer Staples": {"weight": 0.05, "return": 0.04},
            "Energy": {"weight": 0.03, "return": 0.05},
            "Utilities": {"weight": 0.02, "return": 0.03},
            "Real Estate": {"weight": 0.03, "return": 0.06},
            "Materials": {"weight": 0.02, "return": 0.12},
        }
    
    async def get_sector_allocation_effect(
        self,
        portfolio_id: str,
        sector: str
    ) -> float:
        """
        Get allocation effect for a specific sector.
        
        Args:
            portfolio_id: Portfolio to analyze
            sector: GICS sector name
            
        Returns:
            Allocation effect in basis points
        """
        result = await self.calculate_brinson_attribution(
            portfolio_id=portfolio_id,
            benchmark_id="sp500",
            period=DateRange(start="2025-01-01", end="2025-12-31")
        )
        
        for sa in result.sector_attributions:
            if sa.sector == sector:
                return sa.allocation_effect
        
        return 0.0
    
    async def get_selection_effect(
        self,
        portfolio_id: str,
        sector: str
    ) -> float:
        """
        Get selection effect for a specific sector.
        
        Args:
            portfolio_id: Portfolio to analyze
            sector: GICS sector name
            
        Returns:
            Selection effect in basis points
        """
        result = await self.calculate_brinson_attribution(
            portfolio_id=portfolio_id,
            benchmark_id="sp500",
            period=DateRange(start="2025-01-01", end="2025-12-31")
        )
        
        for sa in result.sector_attributions:
            if sa.sector == sector:
                return sa.selection_effect
        
        return 0.0
    
    async def detect_regime_shift(
        self,
        portfolio_id: str,
        benchmark_id: str
    ) -> List[RegimeShiftEvent]:
        """
        Detect periods when strategy decoupled from benchmark.
        
        Uses rolling correlation analysis to identify regime shifts.
        
        Args:
            portfolio_id: Portfolio to analyze
            benchmark_id: Benchmark for comparison
            
        Returns:
            List of detected regime shift events
        """
        # Mock regime shift detection
        # In production, this would analyze rolling correlations
        logger.info(f"Detecting regime shifts for {portfolio_id}")
        
        # Return mock regime shift for demonstration
        return [
            RegimeShiftEvent(
                start_date="2025-03-01",
                end_date="2025-04-15",
                correlation_before=0.92,
                correlation_during=0.45,
                impact_basis_points=185.0,
                description="Q1 tech rotation caused temporary decoupling"
            )
        ]
    
    def get_available_benchmarks(self) -> List[Dict[str, str]]:
        """Get list of available benchmarks for comparison."""
        return [
            {"id": "sp500", "name": "S&P 500"},
            {"id": "nasdaq", "name": "NASDAQ Composite"},
            {"id": "custom", "name": "Custom Index"}
        ]
