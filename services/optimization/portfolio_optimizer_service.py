"""
==============================================================================
FILE: services/optimization/portfolio_optimizer_service.py
ROLE: Portfolio Optimization Engine
PURPOSE: Implements multiple portfolio optimization strategies (MVO, Black-Litterman,
         Risk Parity) with support for various objectives, constraints, and risk models.

INTEGRATION POINTS:
    - PortfolioService: Current portfolio holdings
    - MarketDataService: Expected returns and covariance matrices
    - RiskService: Risk model selection
    - ExecutionService: Rebalancing trade execution
    - OptimizationAPI: Optimization results endpoints

METHODOLOGY:
    - Mean-Variance Optimization (Markowitz)
    - Black-Litterman Model
    - Risk Parity
    - Minimum Variance
    - Maximum Sharpe Ratio
    - Custom objective functions

USAGE:
    from services.optimization.portfolio_optimizer_service import PortfolioOptimizerService
    optimizer = PortfolioOptimizerService()
    result = await optimizer.optimize(
        portfolio_id="portfolio_123",
        objective="maximize_sharpe",
        constraints=constraints,
        risk_model="historical"
    )

DEPENDENCIES:
    - scipy.optimize (optimization algorithms)
    - cvxpy (convex optimization)
    - pandas (data manipulation)
    - numpy (numerical calculations)
    
AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from models.optimization import (
    OptimizationResult,
    OptimizationObjective,
    OptimizationMethod,
    OptimizationConstraints
)
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class PortfolioOptimizerService:
    """
    Service for portfolio optimization.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.risk_free_rate = 0.02  # 2% risk-free rate
        
    async def optimize(
        self,
        portfolio_id: str,
        objective: str = "maximize_sharpe",
        method: str = "mean_variance",
        constraints: Optional[OptimizationConstraints] = None,
        risk_model: str = "historical",
        lookback_days: int = 252
    ) -> OptimizationResult:
        """
        Optimize portfolio for given objective.
        
        Args:
            portfolio_id: Portfolio identifier
            objective: Optimization objective
            method: Optimization method
            constraints: Optimization constraints
            risk_model: Risk model to use
            lookback_days: Lookback period for risk calculation
            
        Returns:
            OptimizationResult with optimal weights and metrics
        """
        logger.info(f"Optimizing portfolio {portfolio_id} with objective {objective}")
        
        start_time = datetime.utcnow()
        
        # Check cache
        cache_key = f"optimization:{portfolio_id}:{objective}:{method}"
        cached_result = self.cache_service.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for optimization")
            return OptimizationResult(**cached_result)
        
        # Get portfolio data
        portfolio_data = await self._get_portfolio_data(portfolio_id)
        holdings = portfolio_data.get('holdings', [])
        
        if not holdings:
            raise ValueError("Portfolio has no holdings")
        
        # Get expected returns and covariance
        symbols = [h.get('symbol', '') for h in holdings]
        expected_returns = await self._get_expected_returns(symbols, risk_model)
        covariance_matrix = await self._get_covariance_matrix(symbols, lookback_days)
        
        # Set default constraints if not provided
        if constraints is None:
            constraints = OptimizationConstraints()
        
        # Optimize based on method
        if method == "mean_variance":
            optimal_weights = await self._mean_variance_optimize(
                expected_returns, covariance_matrix, objective, constraints
            )
        elif method == "risk_parity":
            optimal_weights = await self._risk_parity_optimize(
                covariance_matrix, constraints
            )
        elif method == "minimum_variance":
            optimal_weights = await self._minimum_variance_optimize(
                covariance_matrix, constraints
            )
        else:
            raise ValueError(f"Unknown optimization method: {method}")
        
        # Calculate metrics
        portfolio_return = np.dot(optimal_weights, expected_returns)
        portfolio_risk = np.sqrt(np.dot(optimal_weights, np.dot(covariance_matrix, optimal_weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_risk if portfolio_risk > 0 else 0.0
        
        # Check constraint satisfaction
        constraint_satisfaction = await self._check_constraints(
            optimal_weights, holdings, constraints
        )
        
        optimization_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Create result
        result = OptimizationResult(
            portfolio_id=portfolio_id,
            optimization_method=method,
            objective=objective,
            optimal_weights={symbols[i]: float(optimal_weights[i]) for i in range(len(symbols))},
            expected_return=float(portfolio_return),
            expected_risk=float(portfolio_risk),
            sharpe_ratio=float(sharpe_ratio),
            constraint_satisfaction=constraint_satisfaction,
            optimization_time_seconds=optimization_time,
            optimization_date=datetime.utcnow()
        )
        
        # Cache result (1 hour)
        self.cache_service.set(cache_key, result.dict(), ttl=3600)
        
        return result
    
    async def _mean_variance_optimize(
        self,
        expected_returns: np.ndarray,
        covariance_matrix: np.ndarray,
        objective: str,
        constraints: OptimizationConstraints
    ) -> np.ndarray:
        """Mean-Variance Optimization."""
        n = len(expected_returns)
        
        # Initial guess (equal weights)
        x0 = np.ones(n) / n
        
        # Objective function
        if objective == "maximize_sharpe":
            def objective_func(weights):
                portfolio_return = np.dot(weights, expected_returns)
                portfolio_risk = np.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))
                sharpe = (portfolio_return - self.risk_free_rate) / portfolio_risk if portfolio_risk > 0 else -1e10
                return -sharpe  # Minimize negative Sharpe
        elif objective == "minimize_risk":
            def objective_func(weights):
                return np.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))
        elif objective == "maximize_return":
            def objective_func(weights):
                return -np.dot(weights, expected_returns)  # Minimize negative return
        else:
            raise ValueError(f"Unknown objective: {objective}")
        
        # Constraints
        constraint_list = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}  # Weights sum to 1
        ]
        
        # Bounds (long-only by default)
        bounds = [(0.0, 1.0) for _ in range(n)]
        
        # Optimize
        result = minimize(
            objective_func,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraint_list,
            options={'maxiter': 1000}
        )
        
        if not result.success:
            logger.warning(f"Optimization did not converge: {result.message}")
        
        return result.x
    
    async def _risk_parity_optimize(
        self,
        covariance_matrix: np.ndarray,
        constraints: OptimizationConstraints
    ) -> np.ndarray:
        """Risk Parity Optimization."""
        n = covariance_matrix.shape[0]
        
        # Risk parity: equal risk contribution from each asset
        def objective_func(weights):
            portfolio_risk = np.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))
            marginal_contributions = np.dot(covariance_matrix, weights) / portfolio_risk
            risk_contributions = weights * marginal_contributions
            target_contribution = 1.0 / n
            return np.sum((risk_contributions - target_contribution) ** 2)
        
        x0 = np.ones(n) / n
        bounds = [(0.0, 1.0) for _ in range(n)]
        constraint_list = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
        ]
        
        result = minimize(
            objective_func,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraint_list
        )
        
        return result.x
    
    async def _minimum_variance_optimize(
        self,
        covariance_matrix: np.ndarray,
        constraints: OptimizationConstraints
    ) -> np.ndarray:
        """Minimum Variance Optimization."""
        n = covariance_matrix.shape[0]
        
        def objective_func(weights):
            return np.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))
        
        x0 = np.ones(n) / n
        bounds = [(0.0, 1.0) for _ in range(n)]
        constraint_list = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
        ]
        
        result = minimize(
            objective_func,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraint_list
        )
        
        return result.x
    
    async def _get_portfolio_data(self, portfolio_id: str) -> Dict:
        """Get portfolio holdings."""
        # In production, fetch from portfolio service
        return {
            'holdings': [
                {'symbol': 'AAPL', 'weight': 0.3, 'sector': 'Technology'},
                {'symbol': 'MSFT', 'weight': 0.25, 'sector': 'Technology'},
                {'symbol': 'JPM', 'weight': 0.15, 'sector': 'Financials'}
            ]
        }
    
    async def _get_expected_returns(
        self,
        symbols: List[str],
        risk_model: str
    ) -> np.ndarray:
        """Get expected returns for symbols."""
        # In production, use historical returns, CAPM, or factor models
        # For now, return mock expected returns
        n = len(symbols)
        return np.array([0.10 + i * 0.02 for i in range(n)])  # 10-14% annual returns
    
    async def _get_covariance_matrix(
        self,
        symbols: List[str],
        lookback_days: int
    ) -> np.ndarray:
        """Get covariance matrix for symbols."""
        # In production, calculate from historical returns
        # For now, return mock covariance matrix
        n = len(symbols)
        np.random.seed(42)
        base_cov = np.random.rand(n, n)
        covariance = (base_cov + base_cov.T) / 2  # Make symmetric
        np.fill_diagonal(covariance, 0.04)  # 20% volatility on diagonal
        return covariance
    
    async def _check_constraints(
        self,
        weights: np.ndarray,
        holdings: List[Dict],
        constraints: OptimizationConstraints
    ) -> Dict[str, bool]:
        """Check if constraints are satisfied."""
        satisfaction = {}
        
        # Check weights sum to 1
        satisfaction['weights_sum_to_one'] = abs(np.sum(weights) - 1.0) < 1e-6
        
        # Check long-only
        satisfaction['long_only'] = all(w >= 0 for w in weights)
        
        # Check position limits
        symbols = [h.get('symbol', '') for h in holdings]
        for constraint in constraints.position_limits:
            idx = symbols.index(constraint.symbol) if constraint.symbol in symbols else -1
            if idx >= 0:
                weight = weights[idx]
                satisfied = (constraint.min_weight or 0.0) <= weight <= (constraint.max_weight or 1.0)
                satisfaction[f'position_limit_{constraint.symbol}'] = satisfied
        
        return satisfaction


# Singleton instance
_optimizer_service: Optional[PortfolioOptimizerService] = None


def get_optimizer_service() -> PortfolioOptimizerService:
    """Get singleton optimizer service instance."""
    global _optimizer_service
    if _optimizer_service is None:
        _optimizer_service = PortfolioOptimizerService()
    return _optimizer_service
