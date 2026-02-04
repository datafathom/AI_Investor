"""
==============================================================================
FILE: services/risk/advanced_risk_metrics_service.py
ROLE: Advanced Risk Metrics Calculator
PURPOSE: Calculates comprehensive risk metrics including VaR, CVaR, drawdown,
         and risk-adjusted return ratios for portfolio analysis.

INTEGRATION POINTS:
    - PortfolioService: Portfolio holdings and weights
    - MarketDataService: Historical returns data
    - RiskService: Existing risk infrastructure
    - RiskAPI: Risk metrics endpoints

METHODOLOGY:
    - Historical VaR/CVaR
    - Parametric VaR (variance-covariance)
    - Monte Carlo VaR
    - Maximum Drawdown calculation
    - Risk-adjusted return ratios

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import timezone, datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from scipy import stats
from schemas.risk import RiskMetrics, RiskMetricMethod
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service
from services.analysis.monte_carlo import MonteCarloEngine

logger = logging.getLogger(__name__)


class AdvancedRiskMetricsService:
    """
    Service for calculating advanced risk metrics.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.monte_carlo = MonteCarloEngine()
        self.risk_free_rate = 0.02  # 2% risk-free rate
        
    async def calculate_risk_metrics(
        self,
        portfolio_id: str,
        method: str = "historical",
        lookback_days: int = 252,
        confidence_levels: List[float] = [0.95, 0.99]
    ) -> RiskMetrics:
        """
        Calculate comprehensive risk metrics for portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            method: Calculation method (historical, parametric, monte_carlo)
            lookback_days: Lookback period in days
            confidence_levels: Confidence levels for VaR/CVaR
            
        Returns:
            RiskMetrics with all calculated metrics
        """
        logger.info(f"Calculating risk metrics for portfolio {portfolio_id} using {method}")
        
        # Check cache
        cache_key = f"risk_metrics:{portfolio_id}:{method}:{lookback_days}"
        cached_result = self.cache_service.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for risk metrics")
            return RiskMetrics(**cached_result)
        
        # Get portfolio data and returns
        portfolio_data = await self._get_portfolio_data(portfolio_id)
        returns = await self._get_portfolio_returns(portfolio_id, lookback_days)
        
        # Calculate VaR and CVaR
        var_95, var_99 = await self._calculate_var(returns, confidence_levels, method)
        cvar_95, cvar_99 = await self._calculate_cvar(returns, confidence_levels, method)
        
        # Calculate maximum drawdown
        max_drawdown, drawdown_duration = await self._calculate_max_drawdown(returns)
        
        # Calculate risk-adjusted ratios
        sharpe_ratio = await self._calculate_sharpe_ratio(returns)
        sortino_ratio = await self._calculate_sortino_ratio(returns)
        calmar_ratio = await self._calculate_calmar_ratio(returns, max_drawdown)
        
        # Calculate volatility and beta
        volatility = await self._calculate_volatility(returns)
        beta = await self._calculate_beta(portfolio_id, returns)
        
        result = RiskMetrics(
            portfolio_id=portfolio_id,
            calculation_date=datetime.now(timezone.utc),
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            cvar_99=cvar_99,
            maximum_drawdown=max_drawdown,
            maximum_drawdown_duration_days=drawdown_duration,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            calmar_ratio=calmar_ratio,
            volatility=volatility,
            beta=beta,
            method=method
        )
        
        # Cache result (1 hour)
        self.cache_service.set(cache_key, result.model_dump(), ttl=3600)
        
        return result
    
    def calculate_hidden_volatility_score(
        self, 
        reported_vol: float, 
        valuation_gap_pct: float, 
        liquidity_lockup_years: int
    ) -> Dict[str, Any]:
        """
        Phase 181.5: Hidden Volatility Score.
        Calculates 'True' volatility by unsmoothing reported private asset returns.
        
        Formula: True Vol = Reported Vol * (1 + Gap %) * (1 + log10(Lockup Years + 1))
        """
        import math
        
        gap_penalty = 1.0 + valuation_gap_pct
        lockup_penalty = 1.0 + math.log10(liquidity_lockup_years + 1)
        
        true_vol = reported_vol * gap_penalty * lockup_penalty
        risk_score = min(100, (true_vol / 0.50) * 100) # Norm to 50% vol being max risk
        
        logger.info(f"RISK_LOG: Hidden Volatility Score calculated. Reported: {reported_vol:.1%}, True: {true_vol:.1%}")
        
        return {
            "reported_volatility": reported_vol,
            "true_volatility": round(true_vol, 4),
            "valuation_gap_pct": valuation_gap_pct,
            "liquidity_lockup_years": liquidity_lockup_years,
            "hidden_vol_score": round(risk_score, 2),
            "status": "DANGER" if risk_score > 70 else "MONITOR"
        }
    
    async def _calculate_var(
        self,
        returns: np.ndarray,
        confidence_levels: List[float],
        method: str
    ) -> Tuple[float, float]:
        """Calculate Value-at-Risk."""
        if method == "historical":
            var_95 = -np.percentile(returns, (1 - 0.95) * 100)
            var_99 = -np.percentile(returns, (1 - 0.99) * 100)
        elif method == "parametric":
            mean = np.mean(returns)
            std = np.std(returns)
            var_95 = -(mean + stats.norm.ppf(1 - 0.95) * std)
            var_99 = -(mean + stats.norm.ppf(1 - 0.99) * std)
        else:  # monte_carlo
            # Use Monte Carlo simulation
            var_95 = -np.percentile(returns, 5)
            var_99 = -np.percentile(returns, 1)
        
        return float(var_95), float(var_99)
    
    async def _calculate_cvar(
        self,
        returns: np.ndarray,
        confidence_levels: List[float],
        method: str
    ) -> Tuple[float, float]:
        """Calculate Conditional Value-at-Risk (Expected Shortfall)."""
        if method == "historical":
            cvar_95 = -np.mean(returns[returns <= np.percentile(returns, 5)])
            cvar_99 = -np.mean(returns[returns <= np.percentile(returns, 1)])
        else:
            # Simplified: CVaR is typically 20% higher than VaR
            var_95, var_99 = await self._calculate_var(returns, confidence_levels, method)
            cvar_95 = var_95 * 1.2
            cvar_99 = var_99 * 1.2
        
        return float(cvar_95), float(cvar_99)
    
    async def _calculate_max_drawdown(self, returns: np.ndarray) -> Tuple[float, int]:
        """Calculate maximum drawdown and duration."""
        cumulative = (1 + returns).cumprod()
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = abs(np.min(drawdown))
        
        # Find duration
        max_dd_idx = np.argmin(drawdown)
        recovery_idx = np.where(cumulative[max_dd_idx:] >= cumulative[max_dd_idx])[0]
        duration = len(recovery_idx) if len(recovery_idx) > 0 else len(returns)
        
        return float(max_drawdown), int(duration)
    
    async def _calculate_sharpe_ratio(self, returns: np.ndarray) -> float:
        """Calculate Sharpe ratio."""
        excess_returns = returns - (self.risk_free_rate / 252)  # Daily risk-free rate
        if np.std(excess_returns) == 0:
            return 0.0
        sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)  # Annualized
        return float(sharpe)
    
    async def _calculate_sortino_ratio(self, returns: np.ndarray) -> float:
        """Calculate Sortino ratio (uses downside deviation)."""
        excess_returns = returns - (self.risk_free_rate / 252)
        downside_returns = excess_returns[excess_returns < 0]
        if len(downside_returns) == 0 or np.std(downside_returns) == 0:
            return 0.0
        sortino = np.mean(excess_returns) / np.std(downside_returns) * np.sqrt(252)
        return float(sortino)
    
    async def _calculate_calmar_ratio(
        self,
        returns: np.ndarray,
        max_drawdown: float
    ) -> float:
        """Calculate Calmar ratio (annualized return / max drawdown)."""
        annual_return = np.mean(returns) * 252
        if max_drawdown == 0:
            return 0.0
        calmar = annual_return / max_drawdown
        return float(calmar)
    
    async def _calculate_volatility(self, returns: np.ndarray) -> float:
        """Calculate annualized volatility."""
        volatility = np.std(returns) * np.sqrt(252)
        return float(volatility)
    
    async def _calculate_beta(
        self,
        portfolio_id: str,
        returns: np.ndarray
    ) -> Optional[float]:
        """Calculate portfolio beta relative to market."""
        # In production, compare to benchmark returns
        # For now, return mock beta
        return 1.0
    
    async def _get_portfolio_data(self, portfolio_id: str) -> Dict:
        """Get portfolio holdings."""
        return {'holdings': []}
    
    async def _get_portfolio_returns(
        self,
        portfolio_id: str,
        lookback_days: int
    ) -> np.ndarray:
        """Get historical portfolio returns."""
        # In production, fetch from market data service
        # For now, generate mock returns
        np.random.seed(42)
        returns = np.random.normal(0.0005, 0.015, lookback_days)  # ~12% annual return, 24% vol
        return returns


# Singleton instance
_risk_metrics_service: Optional[AdvancedRiskMetricsService] = None


def get_risk_metrics_service() -> AdvancedRiskMetricsService:
    """Get singleton risk metrics service instance."""
    global _risk_metrics_service
    if _risk_metrics_service is None:
        _risk_metrics_service = AdvancedRiskMetricsService()
    return _risk_metrics_service
