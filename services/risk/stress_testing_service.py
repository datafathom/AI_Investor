"""
==============================================================================
FILE: services/risk/stress_testing_service.py
ROLE: Stress Testing Engine
PURPOSE: Provides stress testing capabilities including historical scenario replay,
         Monte Carlo simulation, and custom stress scenarios.

INTEGRATION POINTS:
    - PortfolioService: Portfolio holdings
    - MarketDataService: Historical market data
    - StressTestingAPI: Stress test endpoints
    - FrontendRisk: Stress test visualization

FEATURES:
    - Historical scenario replay
    - Monte Carlo simulation
    - Custom stress scenarios
    - Correlation breakdown scenarios

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
from models.risk import StressTestResult, StressScenario, MonteCarloResult
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service
from services.analysis.monte_carlo import MonteCarloEngine

logger = logging.getLogger(__name__)


class StressTestingService:
    """
    Service for portfolio stress testing.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.monte_carlo = MonteCarloEngine()
        
        # Historical scenarios
        self.historical_scenarios = {
            "2008_financial_crisis": {
                "description": "2008 Financial Crisis",
                "market_shock": {"Equity": -0.50, "Fixed Income": -0.10},
                "duration_days": 252
            },
            "2020_covid_crash": {
                "description": "2020 COVID-19 Market Crash",
                "market_shock": {"Equity": -0.35, "Fixed Income": 0.05},
                "duration_days": 30
            },
            "2022_inflation_shock": {
                "description": "2022 Inflation and Rate Shock",
                "market_shock": {"Equity": -0.20, "Fixed Income": -0.15},
                "duration_days": 180
            }
        }
    
    async def run_historical_scenario(
        self,
        portfolio_id: str,
        scenario_name: str
    ) -> StressTestResult:
        """
        Run historical scenario stress test.
        
        Args:
            portfolio_id: Portfolio identifier
            scenario_name: Name of historical scenario
            
        Returns:
            StressTestResult with stress test results
        """
        logger.info(f"Running historical scenario {scenario_name} for portfolio {portfolio_id}")
        
        if scenario_name not in self.historical_scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        scenario_data = self.historical_scenarios[scenario_name]
        scenario = StressScenario(
            scenario_name=scenario_name,
            description=scenario_data["description"],
            market_shock=scenario_data["market_shock"],
            duration_days=scenario_data["duration_days"]
        )
        
        # Get portfolio value
        portfolio_value = await self._get_portfolio_value(portfolio_id)
        
        # Apply stress
        stressed_value = await self._apply_stress(portfolio_id, scenario)
        loss_amount = portfolio_value - stressed_value
        loss_percentage = (loss_amount / portfolio_value * 100) if portfolio_value > 0 else 0.0
        
        # Estimate recovery time (simplified)
        recovery_time = scenario.duration_days * 2  # Assume 2x duration to recover
        
        return StressTestResult(
            portfolio_id=portfolio_id,
            scenario=scenario,
            initial_value=portfolio_value,
            stressed_value=stressed_value,
            loss_amount=loss_amount,
            loss_percentage=loss_percentage,
            recovery_time_days=recovery_time,
            calculation_date=datetime.utcnow()
        )
    
    async def run_monte_carlo_simulation(
        self,
        portfolio_id: str,
        n_simulations: int = 10000,
        time_horizon_days: int = 252
    ) -> MonteCarloResult:
        """
        Run Monte Carlo simulation for portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            n_simulations: Number of simulations
            time_horizon_days: Time horizon in days
            
        Returns:
            MonteCarloResult with simulation results
        """
        logger.info(f"Running Monte Carlo simulation for portfolio {portfolio_id}")
        
        # Get portfolio parameters
        portfolio_value = await self._get_portfolio_value(portfolio_id)
        expected_return = 0.10  # 10% annual return
        volatility = 0.15  # 15% annual volatility
        
        # Run simulations
        simulations = []
        for _ in range(n_simulations):
            # Generate random return path
            daily_return = expected_return / 252
            daily_vol = volatility / np.sqrt(252)
            path = np.random.normal(daily_return, daily_vol, time_horizon_days)
            final_value = portfolio_value * np.prod(1 + path)
            simulations.append(final_value)
        
        simulations = np.array(simulations)
        
        # Calculate statistics
        expected_value = np.mean(simulations)
        value_at_5th = np.percentile(simulations, 5)
        value_at_95th = np.percentile(simulations, 95)
        probability_of_loss = np.sum(simulations < portfolio_value) / n_simulations
        probability_of_positive = np.sum(simulations > portfolio_value) / n_simulations
        
        return MonteCarloResult(
            portfolio_id=portfolio_id,
            n_simulations=n_simulations,
            time_horizon_days=time_horizon_days,
            expected_value=float(expected_value),
            value_at_5th_percentile=float(value_at_5th),
            value_at_95th_percentile=float(value_at_95th),
            probability_of_loss=float(probability_of_loss),
            probability_of_positive_return=float(probability_of_positive),
            calculation_date=datetime.utcnow()
        )
    
    async def run_custom_stress_scenario(
        self,
        portfolio_id: str,
        scenario: StressScenario
    ) -> StressTestResult:
        """
        Run custom stress scenario.
        
        Args:
            portfolio_id: Portfolio identifier
            scenario: Custom stress scenario
            
        Returns:
            StressTestResult with stress test results
        """
        logger.info(f"Running custom stress scenario for portfolio {portfolio_id}")
        
        portfolio_value = await self._get_portfolio_value(portfolio_id)
        stressed_value = await self._apply_stress(portfolio_id, scenario)
        loss_amount = portfolio_value - stressed_value
        loss_percentage = (loss_amount / portfolio_value * 100) if portfolio_value > 0 else 0.0
        
        return StressTestResult(
            portfolio_id=portfolio_id,
            scenario=scenario,
            initial_value=portfolio_value,
            stressed_value=stressed_value,
            loss_amount=loss_amount,
            loss_percentage=loss_percentage,
            recovery_time_days=None,
            calculation_date=datetime.utcnow()
        )
    
    async def _get_portfolio_value(self, portfolio_id: str) -> float:
        """Get current portfolio value."""
        # In production, fetch from portfolio service
        return 100000.0
    
    async def _apply_stress(
        self,
        portfolio_id: str,
        scenario: StressScenario
    ) -> float:
        """Apply stress scenario to portfolio."""
        portfolio_value = await self._get_portfolio_value(portfolio_id)
        
        # Get portfolio allocation by asset class
        allocation = await self._get_portfolio_allocation(portfolio_id)
        
        # Apply shocks
        stressed_value = portfolio_value
        for asset_class, shock in scenario.market_shock.items():
            weight = allocation.get(asset_class, 0.0)
            stressed_value -= portfolio_value * weight * shock
        
        return max(stressed_value, 0.0)  # Can't go negative
    
    async def _get_portfolio_allocation(self, portfolio_id: str) -> Dict[str, float]:
        """Get portfolio allocation by asset class."""
        # In production, fetch from portfolio service
        return {
            "Equity": 0.70,
            "Fixed Income": 0.20,
            "Cash": 0.10
        }


# Singleton instance
_stress_testing_service: Optional[StressTestingService] = None


def get_stress_testing_service() -> StressTestingService:
    """Get singleton stress testing service instance."""
    global _stress_testing_service
    if _stress_testing_service is None:
        _stress_testing_service = StressTestingService()
    return _stress_testing_service
