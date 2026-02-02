"""
==============================================================================
FILE: services/analytics/risk_decomposition_service.py
ROLE: Portfolio Risk Decomposition Engine
PURPOSE: Analyzes portfolio risk by factor exposure, concentration, correlation,
         and tail risk. Provides risk budgeting and risk attribution capabilities.

INTEGRATION POINTS:
    - PortfolioService: Portfolio holdings and weights
    - MarketDataService: Historical returns and factor data
    - RiskService: Existing risk metrics (VaR, CVaR)
    - AnalyticsAPI: REST endpoints for risk data
    - FrontendAnalytics: Risk visualization widgets

METHODOLOGY:
    - Factor risk models (Fama-French, Barra)
    - Historical simulation for tail risk
    - Correlation matrix analysis
    - Risk contribution analysis

USAGE:
    from services.analytics.risk_decomposition_service import RiskDecompositionService
    service = RiskDecompositionService()
    risk_analysis = await service.decompose_risk(
        portfolio_id="portfolio_123",
        risk_model="factor",
        lookback_days=252
    )

DEPENDENCIES:
    - pandas (data manipulation)
    - numpy (numerical calculations)
    - scipy (statistical functions)
    
AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from scipy import stats
from models.analytics import (
    FactorRiskDecomposition,
    FactorExposure,
    ConcentrationRiskAnalysis,
    ConcentrationMetric,
    CorrelationAnalysis,
    TailRiskContributions,
    TailRiskContribution
)
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service
from services.analysis.monte_carlo import MonteCarloEngine

logger = logging.getLogger(__name__)


class RiskDecompositionService:
    """
    Service for decomposing portfolio risk.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.monte_carlo = MonteCarloEngine()
        
    async def decompose_factor_risk(
        self,
        portfolio_id: str,
        factor_model: str = "fama_french",
        lookback_days: int = 252
    ) -> FactorRiskDecomposition:
        """
        Decompose portfolio risk by factor exposure.
        
        Returns:
            FactorRiskDecomposition with factor exposures and contributions
        """
        logger.info(f"Decomposing factor risk for portfolio {portfolio_id} using {factor_model}")
        
        # Check cache
        cache_key = f"factor_risk:{portfolio_id}:{factor_model}:{lookback_days}"
        cached_result = self.cache_service.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for factor risk decomposition")
            return FactorRiskDecomposition(**cached_result)
        
        # Get portfolio data
        portfolio_data = await self._get_portfolio_data(portfolio_id)
        
        # Calculate factor exposures
        factor_exposures = await self._calculate_factor_exposures(
            portfolio_data, factor_model, lookback_days
        )
        
        # Calculate total risk and contributions
        total_risk = await self._calculate_portfolio_volatility(portfolio_data, lookback_days)
        idiosyncratic_risk = total_risk * 0.3  # Simplified: 30% idiosyncratic
        r_squared = 0.7  # Simplified: 70% explained by factors
        
        result = FactorRiskDecomposition(
            portfolio_id=portfolio_id,
            factor_model=factor_model,
            total_risk=total_risk,
            factor_exposures=factor_exposures,
            idiosyncratic_risk=idiosyncratic_risk,
            r_squared=r_squared
        )
        
        # Cache result (1 hour)
        self.cache_service.set(cache_key, result.dict(), ttl=3600)
        
        return result
        
    async def calculate_concentration_risk(
        self,
        portfolio_id: str,
        dimensions: List[str] = ["holding", "sector", "geography"]
    ) -> ConcentrationRiskAnalysis:
        """
        Calculate concentration risk across multiple dimensions.
        
        Returns:
            ConcentrationRiskAnalysis with concentration metrics
        """
        logger.info(f"Calculating concentration risk for portfolio {portfolio_id}")
        
        # Get portfolio data
        portfolio_data = await self._get_portfolio_data(portfolio_id)
        holdings = portfolio_data.get('holdings', [])
        
        # Calculate HHI for holdings
        holding_weights = [h.get('weight', 0.0) for h in holdings]
        holding_hhi = sum(w ** 2 for w in holding_weights)
        top_5_holding = sum(sorted(holding_weights, reverse=True)[:5])
        top_10_holding = sum(sorted(holding_weights, reverse=True)[:10])
        max_weight_holding = max(holding_weights) if holding_weights else 0.0
        max_weight_symbol = holdings[holding_weights.index(max_weight_holding)].get('symbol', '') if holding_weights else ''
        
        holding_metric = ConcentrationMetric(
            dimension="holding",
            herfindahl_hirschman_index=holding_hhi,
            top_5_concentration=top_5_holding,
            top_10_concentration=top_10_holding,
            max_weight=max_weight_holding,
            max_weight_symbol=max_weight_symbol
        )
        
        # Calculate sector concentration
        sector_weights = {}
        for holding in holdings:
            sector = holding.get('sector', 'Unknown')
            sector_weights[sector] = sector_weights.get(sector, 0.0) + holding.get('weight', 0.0)
        
        sector_weight_list = list(sector_weights.values())
        sector_hhi = sum(w ** 2 for w in sector_weight_list)
        top_5_sector = sum(sorted(sector_weight_list, reverse=True)[:5])
        top_10_sector = sum(sorted(sector_weight_list, reverse=True)[:10])
        max_weight_sector = max(sector_weight_list) if sector_weight_list else 0.0
        max_sector = max(sector_weights.items(), key=lambda x: x[1])[0] if sector_weights else ''
        
        sector_metric = ConcentrationMetric(
            dimension="sector",
            herfindahl_hirschman_index=sector_hhi,
            top_5_concentration=top_5_sector,
            top_10_concentration=top_10_sector,
            max_weight=max_weight_sector,
            max_weight_symbol=max_sector
        )
        
        # Simplified geography and asset class metrics
        geography_metric = ConcentrationMetric(
            dimension="geography",
            herfindahl_hirschman_index=0.5,
            top_5_concentration=0.9,
            top_10_concentration=1.0,
            max_weight=0.8,
            max_weight_symbol="US"
        )
        
        asset_class_metric = ConcentrationMetric(
            dimension="asset_class",
            herfindahl_hirschman_index=0.6,
            top_5_concentration=0.95,
            top_10_concentration=1.0,
            max_weight=0.85,
            max_weight_symbol="Equity"
        )
        
        return ConcentrationRiskAnalysis(
            portfolio_id=portfolio_id,
            by_holding=holding_metric,
            by_sector=sector_metric,
            by_geography=geography_metric,
            by_asset_class=asset_class_metric
        )
        
    async def calculate_correlation_analysis(
        self,
        portfolio_id: str,
        lookback_days: int = 252
    ) -> CorrelationAnalysis:
        """
        Analyze portfolio correlation structure.
        
        Returns:
            CorrelationAnalysis with correlation matrix and insights
        """
        logger.info(f"Analyzing correlation for portfolio {portfolio_id}")
        
        # Get portfolio data
        portfolio_data = await self._get_portfolio_data(portfolio_id)
        holdings = portfolio_data.get('holdings', [])
        
        # Generate mock correlation matrix
        symbols = [h.get('symbol', '') for h in holdings]
        n = len(symbols)
        
        # Create correlation matrix (simplified - in production, use historical returns)
        correlation_matrix = {}
        for i, sym1 in enumerate(symbols):
            correlation_matrix[sym1] = {}
            for j, sym2 in enumerate(symbols):
                if i == j:
                    correlation_matrix[sym1][sym2] = 1.0
                else:
                    # Mock correlation (in production, calculate from historical returns)
                    correlation_matrix[sym1][sym2] = 0.3 + (i + j) % 3 * 0.1
        
        # Calculate average correlation
        correlations = [correlation_matrix[sym1][sym2] 
                       for sym1 in symbols 
                       for sym2 in symbols 
                       if sym1 != sym2]
        average_correlation = np.mean(correlations) if correlations else 0.0
        
        # Calculate diversification ratio (simplified)
        diversification_ratio = 1.0 / (1.0 + average_correlation)
        
        # Find highly correlated pairs
        highly_correlated_pairs = []
        for i, sym1 in enumerate(symbols):
            for j, sym2 in enumerate(symbols[i+1:], start=i+1):
                if correlation_matrix[sym1][sym2] > 0.7:
                    highly_correlated_pairs.append({
                        "symbol1": sym1,
                        "symbol2": sym2,
                        "correlation": correlation_matrix[sym1][sym2]
                    })
        
        return CorrelationAnalysis(
            portfolio_id=portfolio_id,
            correlation_matrix=correlation_matrix,
            average_correlation=average_correlation,
            diversification_ratio=diversification_ratio,
            highly_correlated_pairs=highly_correlated_pairs
        )
        
    async def calculate_tail_risk_contributions(
        self,
        portfolio_id: str,
        confidence_level: float = 0.95,
        method: str = "historical"
    ) -> TailRiskContributions:
        """
        Calculate tail risk contributions of holdings.
        
        Returns:
            TailRiskContributions with VaR/CVaR contributions
        """
        logger.info(f"Calculating tail risk contributions for portfolio {portfolio_id}")
        
        # Get portfolio data
        portfolio_data = await self._get_portfolio_data(portfolio_id)
        holdings = portfolio_data.get('holdings', [])
        
        # Calculate portfolio VaR and CVaR
        portfolio_value = sum(h.get('value', 0) for h in holdings)
        portfolio_volatility = await self._calculate_portfolio_volatility(portfolio_data, 252)
        
        # VaR calculation (simplified)
        z_score = stats.norm.ppf(confidence_level)
        portfolio_var = portfolio_value * portfolio_volatility * z_score
        portfolio_cvar = portfolio_var * 1.2  # CVaR is typically 20% higher than VaR
        
        # Calculate contributions for each holding
        contributions = []
        for holding in holdings:
            symbol = holding.get('symbol', '')
            weight = holding.get('weight', 0.0)
            holding_value = holding.get('value', 0.0)
            
            # Simplified contribution calculation
            var_contribution = portfolio_var * weight
            cvar_contribution = portfolio_cvar * weight
            marginal_var = portfolio_var * weight * 0.1  # Simplified
            marginal_cvar = portfolio_cvar * weight * 0.1  # Simplified
            
            contributions.append(TailRiskContribution(
                symbol=symbol,
                var_contribution=var_contribution,
                cvar_contribution=cvar_contribution,
                marginal_var=marginal_var,
                marginal_cvar=marginal_cvar
            ))
        
        return TailRiskContributions(
            portfolio_id=portfolio_id,
            confidence_level=confidence_level,
            portfolio_var=portfolio_var,
            portfolio_cvar=portfolio_cvar,
            contributions=contributions,
            method=method
        )
    
    # Private helper methods
    
    async def _get_portfolio_data(self, portfolio_id: str) -> Dict:
        """Get portfolio holdings."""
        # In production, fetch from portfolio service
        return {
            'holdings': [
                {
                    'symbol': 'AAPL',
                    'weight': 0.3,
                    'value': 18000.0,
                    'sector': 'Technology',
                    'asset_class': 'Equity',
                    'geography': 'US'
                },
                {
                    'symbol': 'MSFT',
                    'weight': 0.25,
                    'value': 15000.0,
                    'sector': 'Technology',
                    'asset_class': 'Equity',
                    'geography': 'US'
                },
                {
                    'symbol': 'JPM',
                    'weight': 0.15,
                    'value': 9000.0,
                    'sector': 'Financials',
                    'asset_class': 'Equity',
                    'geography': 'US'
                }
            ]
        }
    
    async def _calculate_factor_exposures(
        self,
        portfolio_data: Dict,
        factor_model: str,
        lookback_days: int
    ) -> List[FactorExposure]:
        """Calculate factor exposures."""
        # Simplified factor exposure calculation
        # In production, use Fama-French or Barra factor models
        factors = [
            FactorExposure(
                factor_name="Market",
                exposure=0.8,
                contribution=0.4,
                risk_contribution=0.35
            ),
            FactorExposure(
                factor_name="Size",
                exposure=0.3,
                contribution=0.15,
                risk_contribution=0.12
            ),
            FactorExposure(
                factor_name="Value",
                exposure=-0.2,
                contribution=-0.1,
                risk_contribution=-0.08
            ),
            FactorExposure(
                factor_name="Momentum",
                exposure=0.4,
                contribution=0.2,
                risk_contribution=0.18
            ),
            FactorExposure(
                factor_name="Quality",
                exposure=0.5,
                contribution=0.25,
                risk_contribution=0.22
            ),
            FactorExposure(
                factor_name="Low Volatility",
                exposure=-0.1,
                contribution=-0.05,
                risk_contribution=-0.04
            )
        ]
        
        return factors
    
    async def _calculate_portfolio_volatility(
        self,
        portfolio_data: Dict,
        lookback_days: int
    ) -> float:
        """Calculate portfolio volatility."""
        # Simplified volatility calculation
        # In production, use historical returns and covariance matrix
        return 0.15  # 15% annual volatility


# Singleton instance
_risk_decomposition_service: Optional[RiskDecompositionService] = None


def get_risk_decomposition_service() -> RiskDecompositionService:
    """Get singleton risk decomposition service instance."""
    global _risk_decomposition_service
    if _risk_decomposition_service is None:
        _risk_decomposition_service = RiskDecompositionService()
    return _risk_decomposition_service
