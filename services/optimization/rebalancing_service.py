"""
==============================================================================
FILE: services/optimization/rebalancing_service.py
ROLE: Automated Rebalancing Engine
PURPOSE: Monitors portfolio drift and executes rebalancing trades with tax-aware
         execution and smart trade optimization.

INTEGRATION POINTS:
    - PortfolioService: Current portfolio state
    - PortfolioOptimizerService: Target allocation calculation
    - ExecutionService: Trade execution
    - TaxService: Tax impact calculation
    - NotificationService: Rebalancing alerts

FEATURES:
    - Threshold-based rebalancing
    - Time-based rebalancing schedules
    - Tax-aware trade selection
    - Smart execution optimization
    - Pre-trade approval workflow

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.optimization import (
    RebalancingRecommendation,
    RebalancingStrategy,
    RebalancingSchedule,
    RebalancingHistory
)
from services.optimization.portfolio_optimizer_service import get_optimizer_service
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class RebalancingService:
    """
    Service for automated portfolio rebalancing.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.optimizer = get_optimizer_service()
        self.cache_service = get_cache_service()
        self.default_threshold = 0.05  # 5% drift threshold
        self.approval_threshold = 10000.0  # $10,000 approval threshold
        
    async def check_rebalancing_needed(
        self,
        portfolio_id: str,
        threshold: Optional[float] = None
    ) -> bool:
        """
        Check if portfolio needs rebalancing based on drift threshold.
        
        Args:
            portfolio_id: Portfolio identifier
            threshold: Drift threshold (default: 5%)
            
        Returns:
            True if rebalancing is needed
        """
        threshold = threshold or self.default_threshold
        
        # Get current and target allocations
        current_weights = await self._get_current_weights(portfolio_id)
        target_weights = await self._get_target_weights(portfolio_id)
        
        # Check drift
        max_drift = 0.0
        for symbol in set(list(current_weights.keys()) + list(target_weights.keys())):
            current = current_weights.get(symbol, 0.0)
            target = target_weights.get(symbol, 0.0)
            drift = abs(current - target)
            max_drift = max(max_drift, drift)
        
        return max_drift > threshold
    
    async def generate_rebalancing_recommendation(
        self,
        portfolio_id: str,
        strategy: str = "threshold"
    ) -> RebalancingRecommendation:
        """
        Generate rebalancing recommendation.
        
        Args:
            portfolio_id: Portfolio identifier
            strategy: Rebalancing strategy (full, threshold, cash_flow)
            
        Returns:
            RebalancingRecommendation with recommended trades
        """
        logger.info(f"Generating rebalancing recommendation for portfolio {portfolio_id}")
        
        # Get current and target weights
        current_weights = await self._get_current_weights(portfolio_id)
        target_weights = await self._get_target_weights(portfolio_id)
        
        # Calculate drift
        drift = await self._calculate_drift(current_weights, target_weights)
        
        # Generate recommended trades
        recommended_trades = await self._generate_trades(
            portfolio_id, current_weights, target_weights, strategy
        )
        
        # Calculate costs
        estimated_cost = await self._estimate_trading_cost(recommended_trades)
        estimated_tax_impact = await self._estimate_tax_impact(recommended_trades)
        
        # Check if approval needed
        requires_approval = estimated_cost > self.approval_threshold
        
        return RebalancingRecommendation(
            portfolio_id=portfolio_id,
            current_weights=current_weights,
            target_weights=target_weights,
            recommended_trades=recommended_trades,
            drift_percentage=drift,
            estimated_cost=estimated_cost,
            estimated_tax_impact=estimated_tax_impact,
            requires_approval=requires_approval,
            recommendation_date=datetime.utcnow()
        )
    
    async def execute_rebalancing(
        self,
        portfolio_id: str,
        recommendation: RebalancingRecommendation,
        approved: bool = False
    ) -> RebalancingHistory:
        """
        Execute rebalancing trades.
        
        Args:
            portfolio_id: Portfolio identifier
            recommendation: Rebalancing recommendation
            approved: Whether user has approved the rebalancing
            
        Returns:
            RebalancingHistory with execution details
        """
        if recommendation.requires_approval and not approved:
            raise ValueError("Rebalancing requires approval but was not approved")
        
        logger.info(f"Executing rebalancing for portfolio {portfolio_id}")
        
        # Execute trades (in production, call execution service)
        trades_executed = recommendation.recommended_trades
        
        # Create history record
        history = RebalancingHistory(
            rebalancing_id=f"rebal_{portfolio_id}_{datetime.utcnow().timestamp()}",
            portfolio_id=portfolio_id,
            rebalancing_date=datetime.utcnow(),
            strategy="threshold",
            before_weights=recommendation.current_weights,
            after_weights=recommendation.target_weights,
            trades_executed=trades_executed,
            total_cost=recommendation.estimated_cost,
            tax_impact=recommendation.estimated_tax_impact,
            status="executed"
        )
        
        # Store in cache/history
        cache_key = f"rebalancing_history:{portfolio_id}"
        history_list = self.cache_service.get(cache_key) or []
        history_list.append(history.dict())
        self.cache_service.set(cache_key, history_list, ttl=86400 * 365)  # 1 year
        
        return history
    
    async def get_rebalancing_history(
        self,
        portfolio_id: str,
        limit: int = 10
    ) -> List[RebalancingHistory]:
        """
        Get rebalancing history for portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            limit: Maximum number of records to return
            
        Returns:
            List of RebalancingHistory records
        """
        cache_key = f"rebalancing_history:{portfolio_id}"
        history_list = self.cache_service.get(cache_key) or []
        
        # Convert to RebalancingHistory objects
        histories = [RebalancingHistory(**h) for h in history_list[-limit:]]
        
        return histories
    
    # Private helper methods
    
    async def _get_current_weights(self, portfolio_id: str) -> Dict[str, float]:
        """Get current portfolio weights."""
        # In production, fetch from portfolio service
        return {
            'AAPL': 0.35,  # Drifted from 0.30
            'MSFT': 0.22,  # Drifted from 0.25
            'JPM': 0.18    # Drifted from 0.15
        }
    
    async def _get_target_weights(self, portfolio_id: str) -> Dict[str, float]:
        """Get target portfolio weights."""
        # In production, get from optimizer or user-defined targets
        return {
            'AAPL': 0.30,
            'MSFT': 0.25,
            'JPM': 0.15
        }
    
    async def _calculate_drift(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float]
    ) -> float:
        """Calculate maximum drift percentage."""
        max_drift = 0.0
        for symbol in set(list(current_weights.keys()) + list(target_weights.keys())):
            current = current_weights.get(symbol, 0.0)
            target = target_weights.get(symbol, 0.0)
            drift = abs(current - target)
            max_drift = max(max_drift, drift)
        
        return max_drift * 100  # Convert to percentage
    
    async def _generate_trades(
        self,
        portfolio_id: str,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        strategy: str
    ) -> List[Dict]:
        """Generate recommended trades."""
        trades = []
        
        # Get portfolio value
        portfolio_value = 100000.0  # Mock value
        
        for symbol in set(list(current_weights.keys()) + list(target_weights.keys())):
            current = current_weights.get(symbol, 0.0)
            target = target_weights.get(symbol, 0.0)
            
            if abs(current - target) < 0.01:  # Skip if difference < 1%
                continue
            
            weight_diff = target - current
            trade_value = weight_diff * portfolio_value
            
            trades.append({
                'symbol': symbol,
                'action': 'BUY' if trade_value > 0 else 'SELL',
                'quantity': abs(trade_value) / 100.0,  # Simplified: assume $100 per share
                'price': 100.0,  # Mock price
                'value': abs(trade_value)
            })
        
        return trades
    
    async def _estimate_trading_cost(self, trades: List[Dict]) -> float:
        """Estimate total trading cost."""
        total_value = sum(t.get('value', 0) for t in trades)
        commission_rate = 0.001  # 0.1% commission
        return total_value * commission_rate
    
    async def _estimate_tax_impact(self, trades: List[Dict]) -> float:
        """Estimate tax impact of trades."""
        # Simplified: estimate based on gains/losses
        # In production, use tax service
        sell_trades = [t for t in trades if t.get('action') == 'SELL']
        total_sell_value = sum(t.get('value', 0) for t in sell_trades)
        tax_rate = 0.20  # 20% capital gains tax
        return total_sell_value * tax_rate * 0.1  # Assume 10% gain on sold positions


# Singleton instance
_rebalancing_service: Optional[RebalancingService] = None


def get_rebalancing_service() -> RebalancingService:
    """Get singleton rebalancing service instance."""
    global _rebalancing_service
    if _rebalancing_service is None:
        _rebalancing_service = RebalancingService()
    return _rebalancing_service
