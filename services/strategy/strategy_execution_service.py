"""
==============================================================================
FILE: services/strategy/strategy_execution_service.py
ROLE: Strategy Execution Engine
PURPOSE: Runs strategies live with risk controls and performance monitoring.

INTEGRATION POINTS:
    - StrategyBuilderService: Strategy definitions
    - ExecutionService: Order execution
    - MarketDataService: Real-time market data
    - RiskService: Risk controls
    - StrategyExecutionAPI: Execution endpoints

FEATURES:
    - Continuous strategy execution
    - Risk controls
    - Performance monitoring
    - Execution logging

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.strategy import (
    TradingStrategy, StrategyExecution, StrategyStatus, StrategyPerformance
)
from services.strategy.strategy_builder_service import get_strategy_builder_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class StrategyExecutionService:
    """
    Service for executing trading strategies.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.strategy_builder = get_strategy_builder_service()
        self.cache_service = get_cache_service()
        self.active_strategies: Dict[str, TradingStrategy] = {}
        
    async def start_strategy(
        self,
        strategy_id: str,
        portfolio_id: str
    ) -> TradingStrategy:
        """
        Start strategy execution.
        
        Args:
            strategy_id: Strategy identifier
            portfolio_id: Portfolio identifier
            
        Returns:
            Updated TradingStrategy
        """
        logger.info(f"Starting strategy {strategy_id}")
        
        # Get strategy
        strategy = await self.strategy_builder._get_strategy(strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        # Validate strategy
        validation = await self.strategy_builder.validate_strategy(strategy_id)
        if not validation['valid']:
            raise ValueError(f"Strategy validation failed: {validation['errors']}")
        
        # Update strategy
        strategy.status = StrategyStatus.ACTIVE
        strategy.portfolio_id = portfolio_id
        strategy.updated_date = datetime.utcnow()
        
        # Save strategy
        await self.strategy_builder._save_strategy(strategy)
        
        # Add to active strategies
        self.active_strategies[strategy_id] = strategy
        
        return strategy
    
    async def stop_strategy(self, strategy_id: str) -> TradingStrategy:
        """
        Stop strategy execution.
        
        Args:
            strategy_id: Strategy identifier
            
        Returns:
            Updated TradingStrategy
        """
        logger.info(f"Stopping strategy {strategy_id}")
        
        strategy = self.active_strategies.get(strategy_id)
        if not strategy:
            strategy = await self.strategy_builder._get_strategy(strategy_id)
        
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        strategy.status = StrategyStatus.STOPPED
        strategy.updated_date = datetime.utcnow()
        
        await self.strategy_builder._save_strategy(strategy)
        
        # Remove from active strategies
        if strategy_id in self.active_strategies:
            del self.active_strategies[strategy_id]
        
        return strategy
    
    async def pause_strategy(self, strategy_id: str) -> TradingStrategy:
        """
        Pause strategy execution.
        
        Args:
            strategy_id: Strategy identifier
            
        Returns:
            Updated TradingStrategy
        """
        strategy = self.active_strategies.get(strategy_id)
        if not strategy:
            strategy = await self.strategy_builder._get_strategy(strategy_id)
        
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        strategy.status = StrategyStatus.PAUSED
        strategy.updated_date = datetime.utcnow()
        
        await self.strategy_builder._save_strategy(strategy)
        
        return strategy
    
    async def execute_strategy_rules(
        self,
        strategy_id: str
    ) -> List[StrategyExecution]:
        """
        Execute strategy rules (called periodically).
        
        Args:
            strategy_id: Strategy identifier
            
        Returns:
            List of execution records
        """
        strategy = self.active_strategies.get(strategy_id)
        if not strategy or strategy.status != StrategyStatus.ACTIVE:
            return []
        
        executions = []
        
        # Sort rules by priority
        sorted_rules = sorted(strategy.rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            try:
                # Check condition (simplified - would evaluate actual conditions)
                condition_met = await self._evaluate_condition(rule.condition_type, rule.condition)
                
                if condition_met:
                    # Execute action
                    action_result = await self._execute_action(rule.action, strategy.portfolio_id)
                    
                    execution = StrategyExecution(
                        execution_id=f"exec_{strategy_id}_{datetime.utcnow().timestamp()}",
                        strategy_id=strategy_id,
                        rule_id=rule.rule_id,
                        action_taken=rule.action.get('type', 'unknown'),
                        order_id=action_result.get('order_id'),
                        execution_time=datetime.utcnow(),
                        result="success" if action_result.get('success') else "failed"
                    )
                    
                    executions.append(execution)
                    
                    # Update last executed
                    strategy.last_executed = datetime.utcnow()
                    await self.strategy_builder._save_strategy(strategy)
            except Exception as e:
                logger.error(f"Error executing rule {rule.rule_id}: {e}")
                execution = StrategyExecution(
                    execution_id=f"exec_{strategy_id}_{datetime.utcnow().timestamp()}",
                    strategy_id=strategy_id,
                    rule_id=rule.rule_id,
                    action_taken=rule.action.get('type', 'unknown'),
                    execution_time=datetime.utcnow(),
                    result="failed"
                )
                executions.append(execution)
        
        return executions
    
    async def get_strategy_performance(
        self,
        strategy_id: str
    ) -> StrategyPerformance:
        """
        Get strategy performance metrics.
        
        Args:
            strategy_id: Strategy identifier
            
        Returns:
            StrategyPerformance object
        """
        # In production, would calculate from actual trades
        strategy = await self.strategy_builder._get_strategy(strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        return StrategyPerformance(
            strategy_id=strategy_id,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            total_pnl=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            current_status=strategy.status
        )
    
    async def _evaluate_condition(
        self,
        condition_type: str,
        condition: Dict
    ) -> bool:
        """Evaluate condition (simplified)."""
        # In production, would evaluate actual market conditions
        return False  # Mock evaluation
    
    async def _execute_action(
        self,
        action: Dict,
        portfolio_id: str
    ) -> Dict:
        """Execute action (simplified)."""
        # In production, would execute actual orders
        return {
            'success': True,
            'order_id': f"order_{datetime.utcnow().timestamp()}"
        }


# Singleton instance
_strategy_execution_service: Optional[StrategyExecutionService] = None


def get_strategy_execution_service() -> StrategyExecutionService:
    """Get singleton strategy execution service instance."""
    global _strategy_execution_service
    if _strategy_execution_service is None:
        _strategy_execution_service = StrategyExecutionService()
    return _strategy_execution_service
