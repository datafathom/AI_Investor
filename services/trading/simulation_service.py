"""
==============================================================================
FILE: services/trading/simulation_service.py
ROLE: Simulation Service
PURPOSE: Provides historical replay and strategy testing capabilities.

INTEGRATION POINTS:
    - PaperTradingService: Order execution simulation
    - MarketDataService: Historical price data
    - StrategyService: Strategy definitions
    - SimulationAPI: Simulation endpoints

FEATURES:
    - Historical replay
    - Strategy backtesting
    - Performance comparison

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from schemas.paper_trading import SimulationResult, VirtualPortfolio
from services.trading.paper_trading_service import get_paper_trading_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class SimulationService:
    """
    Service for trading simulation and backtesting.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.paper_trading = get_paper_trading_service()
        self.cache_service = get_cache_service()
        
    async def run_historical_simulation(
        self,
        strategy_name: str,
        start_date: datetime,
        end_date: datetime,
        initial_capital: float = 100000.0,
        strategy_config: Optional[Dict] = None
    ) -> SimulationResult:
        """
        Run historical simulation/backtest.
        
        Args:
            strategy_name: Name of strategy
            start_date: Simulation start date
            end_date: Simulation end date
            initial_capital: Initial capital
            strategy_config: Optional strategy configuration
            
        Returns:
            SimulationResult with performance metrics
        """
        logger.info(f"Running historical simulation for {strategy_name}")
        
        # Create virtual portfolio
        portfolio = await self.paper_trading.create_virtual_portfolio(
            user_id="simulation",
            portfolio_name=f"{strategy_name}_simulation",
            initial_cash=initial_capital
        )
        
        # Simulate trading (simplified - would execute strategy logic)
        trades = await self._simulate_strategy(
            portfolio.portfolio_id,
            strategy_name,
            start_date,
            end_date,
            strategy_config or {}
        )
        
        # Get final performance
        performance = await self.paper_trading.get_portfolio_performance(portfolio.portfolio_id)
        
        # Calculate metrics
        total_return = performance['total_return'] / 100.0
        sharpe_ratio = await self._calculate_sharpe_ratio(trades)
        max_drawdown = await self._calculate_max_drawdown(trades)
        win_rate = await self._calculate_win_rate(trades)
        
        result = SimulationResult(
            simulation_id=f"sim_{strategy_name}_{datetime.now(timezone.utc).timestamp()}",
            strategy_name=strategy_name,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            final_capital=performance['total_value'],
            total_return=total_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            trades=trades
        )
        
        return result

    async def get_simulation_results(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get recent simulation results.
        """
        # In production, query database
        return await self._get_simulations_from_db(user_id, limit)

    async def _get_simulations_from_db(self, user_id: str, limit: int) -> List[Dict]:
        """Get simulations from DB (mockable)."""
        return []

    async def compare_simulations(
        self,
        simulations: List[SimulationResult]
    ) -> Dict[str, Any]:
        """
        Compare performance of multiple simulations.
        """
        if not simulations:
            return {}
            
        best_return = max(simulations, key=lambda s: s.total_return)
        best_sharpe = max(simulations, key=lambda s: s.sharpe_ratio)
        lowest_drawdown = min(simulations, key=lambda s: s.max_drawdown)
        
        return {
            "best_return": {
                "strategy": best_return.strategy_name,
                "value": best_return.total_return
            },
            "best_sharpe": {
                "strategy": best_sharpe.strategy_name,
                "value": best_sharpe.sharpe_ratio
            },
            "lowest_drawdown": {
                "strategy": lowest_drawdown.strategy_name,
                "value": lowest_drawdown.max_drawdown
            },
            "comparison_count": len(simulations)
        }
    
    async def _simulate_strategy(
        self,
        portfolio_id: str,
        strategy_name: str,
        start_date: datetime,
        end_date: datetime,
        config: Dict
    ) -> List[Dict]:
        """Simulate strategy execution (simplified)."""
        # In production, would execute actual strategy logic
        # For now, return mock trades
        return []
    
    async def _calculate_sharpe_ratio(self, trades: List[Dict]) -> float:
        """Calculate Sharpe ratio (simplified)."""
        if not trades:
            return 0.0
        # Simplified calculation
        return 1.5  # Mock value
    
    async def _calculate_max_drawdown(self, trades: List[Dict]) -> float:
        """Calculate maximum drawdown (simplified)."""
        if not trades:
            return 0.0
        # Simplified calculation
        return 0.15  # 15% mock value
    
    async def _calculate_win_rate(self, trades: List[Dict]) -> float:
        """Calculate win rate (simplified)."""
        if not trades:
            return 0.0
        # Simplified calculation
        return 0.55  # 55% mock value


# Singleton instance
_simulation_service: Optional[SimulationService] = None


def get_simulation_service() -> SimulationService:
    """Get singleton simulation service instance."""
    global _simulation_service
    if _simulation_service is None:
        _simulation_service = SimulationService()
    return _simulation_service
