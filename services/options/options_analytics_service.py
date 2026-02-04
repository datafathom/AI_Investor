"""
==============================================================================
FILE: services/options/options_analytics_service.py
ROLE: Options Analytics Engine
PURPOSE: Calculates Greeks, P&L analysis, probability calculations, and
         implied volatility analysis for options strategies.

INTEGRATION POINTS:
    - OptionsStrategyBuilderService: Strategy definitions
    - OptionsPricingService: Option pricing models
    - OptionsAPI: Analytics endpoints
    - FrontendOptions: Analytics visualization

FEATURES:
    - Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
    - P&L analysis across price and time
    - Probability calculations
    - Implied volatility analysis

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
from scipy.stats import norm
from schemas.options import OptionsStrategy, StrategyGreeks, StrategyPnL, Greeks, StrategyAnalysis
from services.options.strategy_builder_service import get_strategy_builder_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class OptionsAnalyticsService:
    """
    Service for options analytics and Greeks calculations.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        self.risk_free_rate = 0.02  # 2% risk-free rate
    
    async def calculate_greeks(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
        days_to_expiration: int,
        volatility: float = 0.20
    ) -> StrategyGreeks:
        """
        Calculate Greeks for entire strategy.
        
        Args:
            strategy: Options strategy
            underlying_price: Current underlying price
            days_to_expiration: Days until expiration
            volatility: Implied volatility
            
        Returns:
            StrategyGreeks with total and per-leg Greeks
        """
        logger.info(f"Calculating Greeks for strategy {strategy.strategy_id}")
        
        total_delta = 0.0
        total_gamma = 0.0
        total_theta = 0.0
        total_vega = 0.0
        total_rho = 0.0
        
        leg_greeks = {}
        
        for i, leg in enumerate(strategy.legs):
            greeks = await self._calculate_leg_greeks(
                leg, underlying_price, days_to_expiration, volatility
            )
            
            # Multiply by quantity and action
            multiplier = leg.quantity * (1 if leg.action.value == "buy" else -1)
            
            total_delta += greeks.delta * multiplier
            total_gamma += greeks.gamma * multiplier
            total_theta += greeks.theta * multiplier
            total_vega += greeks.vega * multiplier
            if greeks.rho:
                total_rho += greeks.rho * multiplier
            
            # Use unique key for each leg
            leg_key = f"{leg.symbol}_{leg.option_type.value}_{leg.strike}_{i}"
            leg_greeks[leg_key] = greeks
        
        return StrategyGreeks(
            strategy_id=strategy.strategy_id,
            total_delta=total_delta,
            total_gamma=total_gamma,
            total_theta=total_theta,
            total_vega=total_vega,
            total_rho=total_rho if total_rho != 0 else None,
            leg_greeks=leg_greeks
        )
    
    async def calculate_pnl(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
        days_to_expiration: int
    ) -> StrategyPnL:
        """
        Calculate P&L for strategy at given price and time.
        
        Args:
            strategy: Options strategy
            underlying_price: Underlying price to analyze
            days_to_expiration: Days until expiration
            
        Returns:
            StrategyPnL with profit/loss analysis
        """
        logger.info(f"Calculating P&L for strategy {strategy.strategy_id}")
        
        total_value = 0.0
        intrinsic_value = 0.0
        time_value = 0.0
        
        for leg in strategy.legs:
            leg_value = await self._calculate_leg_value(
                leg, underlying_price, days_to_expiration
            )
            
            multiplier = leg.quantity * (1 if leg.action.value == "buy" else -1)
            total_value += leg_value * multiplier
            
            # Calculate intrinsic value
            if leg.option_type.value == "call":
                intrinsic = max(0, underlying_price - leg.strike)
            else:  # put
                intrinsic = max(0, leg.strike - underlying_price)
            
            intrinsic_value += intrinsic * leg.quantity * multiplier
            time_value += (leg_value - intrinsic) * leg.quantity * multiplier
        
        # Calculate P&L
        profit_loss = total_value - strategy.net_cost
        profit_loss_pct = (profit_loss / abs(strategy.net_cost) * 100) if strategy.net_cost != 0 else 0.0
        
        return StrategyPnL(
            strategy_id=strategy.strategy_id,
            underlying_price=underlying_price,
            days_to_expiration=days_to_expiration,
            profit_loss=profit_loss,
            profit_loss_pct=profit_loss_pct,
            intrinsic_value=intrinsic_value,
            time_value=time_value
        )
    
    async def analyze_strategy(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
        days_to_expiration: int,
        volatility: float = 0.20
    ) -> StrategyAnalysis:
        """
        Complete strategy analysis with Greeks and P&L.
        
        Args:
            strategy: Options strategy
            underlying_price: Current underlying price
            days_to_expiration: Days until expiration
            volatility: Implied volatility
            
        Returns:
            StrategyAnalysis with complete analysis
        """
        greeks = await self.calculate_greeks(
            strategy, underlying_price, days_to_expiration, volatility
        )
        
        pnl = await self.calculate_pnl(
            strategy, underlying_price, days_to_expiration
        )
        
        # Calculate probability of profit (simplified)
        probability_profit = await self._calculate_probability_profit(
            strategy, underlying_price, days_to_expiration, volatility
        )
        
        return StrategyAnalysis(
            strategy=strategy,
            greeks=greeks,
            pnl=pnl,
            probability_profit=probability_profit,
            implied_volatility=volatility
        )
    
    async def _calculate_leg_greeks(
        self,
        leg,
        underlying_price: float,
        days_to_expiration: int,
        volatility: float
    ) -> Greeks:
        """Calculate Greeks for single leg using Black-Scholes."""
        S = underlying_price
        K = leg.strike
        T = days_to_expiration / 365.0
        r = self.risk_free_rate
        sigma = volatility
        
        if T <= 0:
            # At expiration
            if leg.option_type.value == "call":
                delta = 1.0 if S > K else 0.0
            else:
                delta = -1.0 if S < K else 0.0
            return Greeks(delta=delta, gamma=0.0, theta=0.0, vega=0.0, rho=0.0)
        
        # Black-Scholes Greeks
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if leg.option_type.value == "call":
            delta = norm.cdf(d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                     r * K * np.exp(-r * T) * norm.cdf(d2)) / 365.0
        else:  # put
            delta = -norm.cdf(-d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + 
                     r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365.0
        
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100.0  # Per 1% change in vol
        
        if leg.option_type.value == "call":
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100.0
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100.0
        
        return Greeks(
            delta=float(delta),
            gamma=float(gamma),
            theta=float(theta),
            vega=float(vega),
            rho=float(rho)
        )
    
    async def _calculate_leg_value(
        self,
        leg,
        underlying_price: float,
        days_to_expiration: int
    ) -> float:
        """Calculate current value of option leg."""
        # Simplified: use intrinsic value + estimated time value
        if leg.option_type.value == "call":
            intrinsic = max(0, underlying_price - leg.strike)
        else:  # put
            intrinsic = max(0, leg.strike - underlying_price)
        
        # Simplified time value (would use Black-Scholes in production)
        time_value = leg.premium * 0.3 if days_to_expiration > 0 else 0.0
        
        return intrinsic + time_value
    
    async def _calculate_probability_profit(
        self,
        strategy: OptionsStrategy,
        underlying_price: float,
        days_to_expiration: int,
        volatility: float
    ) -> float:
        """Calculate probability of profit (simplified)."""
        # Simplified calculation
        # In production, use Monte Carlo or analytical methods
        if strategy.max_profit is not None and strategy.max_loss is not None:
            # Rough estimate based on strategy structure
            return 0.5  # 50% probability (simplified)
        return None


# Singleton instance
_options_analytics_service: Optional[OptionsAnalyticsService] = None


def get_options_analytics_service() -> OptionsAnalyticsService:
    """Get singleton options analytics service instance."""
    global _options_analytics_service
    if _options_analytics_service is None:
        _options_analytics_service = OptionsAnalyticsService()
    return _options_analytics_service
