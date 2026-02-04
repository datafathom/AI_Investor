"""
==============================================================================
FILE: services/retirement/retirement_projection_service.py
ROLE: Retirement Projection Engine
PURPOSE: Provides Monte Carlo retirement projections with multiple scenarios,
         probability analysis, and year-by-year projections.

INTEGRATION POINTS:
    - PortfolioService: Current retirement savings
    - MarketDataService: Expected returns and volatility
    - MonteCarloService: Simulation engine
    - RetirementAPI: Projection endpoints
    - FrontendRetirement: Retirement dashboard

FEATURES:
    - Monte Carlo simulations
    - Multiple scenarios
    - Probability analysis
    - Year-by-year projections

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import timezone, datetime
from typing import Dict, List, Optional
import numpy as np
from schemas.retirement import RetirementScenario, RetirementProjection
from services.analysis.monte_carlo import MonteCarloEngine
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class RetirementProjectionService:
    """
    Service for retirement projections and Monte Carlo analysis.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.monte_carlo = MonteCarloEngine()
        self.cache_service = get_cache_service()
        
    async def project_retirement(
        self,
        scenario: RetirementScenario,
        n_simulations: int = 10000
    ) -> RetirementProjection:
        """
        Project retirement with Monte Carlo simulation.
        
        Args:
            scenario: Retirement scenario parameters
            n_simulations: Number of Monte Carlo simulations
            
        Returns:
            RetirementProjection with probability analysis
        """
        logger.info(f"Projecting retirement for scenario {scenario.scenario_name}")
        
        years_to_retirement = scenario.retirement_age - scenario.current_age
        years_in_retirement = scenario.life_expectancy - scenario.retirement_age
        
        # Run Monte Carlo simulations
        simulation_results = []
        for _ in range(n_simulations):
            result = await self._simulate_retirement_path(scenario)
            simulation_results.append(result)
        
        simulation_results = np.array(simulation_results)
        
        # Calculate statistics
        projected_savings = np.percentile(simulation_results, 50)  # Median
        projected_income = projected_savings * scenario.withdrawal_rate
        
        # Calculate probability of success (savings > 0 at life expectancy)
        success_count = np.sum(simulation_results > 0)
        probability_success = success_count / n_simulations
        
        # Percentile results
        monte_carlo_results = {
            '5th_percentile': float(np.percentile(simulation_results, 5)),
            '25th_percentile': float(np.percentile(simulation_results, 25)),
            '50th_percentile': float(np.percentile(simulation_results, 50)),
            '75th_percentile': float(np.percentile(simulation_results, 75)),
            '95th_percentile': float(np.percentile(simulation_results, 95))
        }
        
        # Generate year-by-year projection (deterministic)
        timeline = await self._generate_timeline(scenario)
        
        return RetirementProjection(
            scenario_id=f"scenario_{scenario.scenario_name}_{datetime.now(timezone.utc).timestamp()}",
            projected_retirement_savings=float(projected_savings),
            projected_annual_income=float(projected_income),
            years_in_retirement=years_in_retirement,
            probability_of_success=float(probability_success),
            monte_carlo_results=monte_carlo_results,
            projected_timeline=timeline
        )
    
    async def compare_scenarios(
        self,
        scenarios: List[RetirementScenario],
        n_simulations: int = 10000
    ) -> Dict[str, RetirementProjection]:
        """
        Compare multiple retirement scenarios.
        
        Args:
            scenarios: List of scenarios to compare
            n_simulations: Number of simulations per scenario
            
        Returns:
            Dictionary of {scenario_name: projection}
        """
        logger.info(f"Comparing {len(scenarios)} retirement scenarios")
        
        results = {}
        for scenario in scenarios:
            projection = await self.project_retirement(scenario, n_simulations)
            results[scenario.scenario_name] = projection
        
        return results
    
    async def _simulate_retirement_path(
        self,
        scenario: RetirementScenario
    ) -> float:
        """Simulate a single retirement path."""
        years_to_retirement = scenario.retirement_age - scenario.current_age
        years_in_retirement = scenario.life_expectancy - scenario.retirement_age
        
        # Accumulation phase
        current_savings = scenario.current_savings
        annual_return = scenario.expected_return
        volatility = 0.15  # 15% volatility
        
        for year in range(years_to_retirement):
            # Random return
            return_rate = np.random.normal(annual_return, volatility)
            current_savings = current_savings * (1 + return_rate) + scenario.annual_contribution
        
        # Retirement phase (withdrawals)
        annual_withdrawal = current_savings * scenario.withdrawal_rate
        
        for year in range(years_in_retirement):
            # Random return
            return_rate = np.random.normal(annual_return, volatility)
            # Adjust withdrawal for inflation
            inflation_adjusted_withdrawal = annual_withdrawal * ((1 + scenario.inflation_rate) ** year)
            current_savings = current_savings * (1 + return_rate) - inflation_adjusted_withdrawal
            
            # Add Social Security if applicable
            if scenario.social_security_benefit:
                current_savings += scenario.social_security_benefit
        
        return current_savings
    
    async def _generate_timeline(
        self,
        scenario: RetirementScenario
    ) -> List[Dict]:
        """Generate year-by-year deterministic projection."""
        timeline = []
        years_to_retirement = scenario.retirement_age - scenario.current_age
        years_in_retirement = scenario.life_expectancy - scenario.retirement_age
        
        current_savings = scenario.current_savings
        current_age = scenario.current_age
        
        # Accumulation phase
        for year in range(years_to_retirement):
            current_savings = current_savings * (1 + scenario.expected_return) + scenario.annual_contribution
            timeline.append({
                'age': current_age + year,
                'year': year + 1,
                'savings': float(current_savings),
                'contribution': scenario.annual_contribution,
                'phase': 'accumulation'
            })
        
        # Retirement phase
        annual_withdrawal = current_savings * scenario.withdrawal_rate
        for year in range(years_in_retirement):
            inflation_adjusted_withdrawal = annual_withdrawal * ((1 + scenario.inflation_rate) ** year)
            current_savings = current_savings * (1 + scenario.expected_return) - inflation_adjusted_withdrawal
            
            if scenario.social_security_benefit:
                current_savings += scenario.social_security_benefit
            
            timeline.append({
                'age': scenario.retirement_age + year,
                'year': years_to_retirement + year + 1,
                'savings': float(current_savings),
                'withdrawal': float(inflation_adjusted_withdrawal),
                'phase': 'retirement'
            })
        
        return timeline


# Singleton instance
_retirement_projection_service: Optional[RetirementProjectionService] = None


def get_retirement_projection_service() -> RetirementProjectionService:
    """Get singleton retirement projection service instance."""
    global _retirement_projection_service
    if _retirement_projection_service is None:
        _retirement_projection_service = RetirementProjectionService()
    return _retirement_projection_service
