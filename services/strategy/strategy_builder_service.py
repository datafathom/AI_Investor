"""
==============================================================================
FILE: services/strategy/strategy_builder_service.py
ROLE: Strategy Builder Service
PURPOSE: Enables creation of automated trading strategies with visual
         interface, rule-based logic, and condition builders.

INTEGRATION POINTS:
    - ExecutionService: Strategy execution
    - BacktestingService: Strategy validation
    - MarketDataService: Real-time data feeds
    - StrategyAPI: Strategy management endpoints

FEATURES:
    - Visual strategy creation
    - Rule-based logic builder
    - Condition builders (price, volume, indicators)
    - Strategy templates

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
import json
import uuid
from datetime import timezone, datetime
from typing import Dict, List, Optional, Any
from schemas.strategy import (
    TradingStrategy, StrategyRule, ConditionType, StrategyStatus
)
from services.system.cache_service import get_cache_service
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)


class StrategyBuilderService:
    """
    Service for building and managing trading strategies.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def create_strategy(
        self,
        user_id: str,
        strategy_name: str,
        description: Optional[str] = None,
        rules: Optional[List[Dict]] = None
    ) -> TradingStrategy:
        """
        Create a new trading strategy.
        
        Args:
            user_id: User identifier
            strategy_name: Name of strategy
            description: Optional description
            rules: Optional list of rule dictionaries
            
        Returns:
            TradingStrategy object
        """
        logger.info(f"Creating strategy {strategy_name} for user {user_id}")
        
        # Convert rules to StrategyRule objects
        strategy_rules = []
        if rules:
            for rule_data in rules:
                rule = StrategyRule(
                    rule_id=f"rule_{user_id}_{datetime.now(timezone.utc).timestamp()}",
                    **rule_data
                )
                strategy_rules.append(rule)
        
        strategy = TradingStrategy(
            strategy_id=f"strategy_{user_id}_{datetime.now(timezone.utc).timestamp()}",
            user_id=user_id,
            strategy_name=strategy_name,
            description=description,
            rules=strategy_rules,
            status=StrategyStatus.DRAFT,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
        
        # Save strategy
        await self._save_strategy(strategy)
        
        return strategy
    
    async def add_rule(
        self,
        strategy_id: str,
        condition_type: str,
        condition: Dict[str, Any],
        action: Dict[str, Any],
        priority: int = 0
    ) -> StrategyRule:
        """
        Add rule to strategy.
        
        Args:
            strategy_id: Strategy identifier
            condition_type: Condition type (price, volume, indicator, time)
            condition: Condition parameters
            action: Action to take
            priority: Rule priority
            
        Returns:
            StrategyRule object
        """
        logger.info(f"Adding rule to strategy {strategy_id}")
        
        # Get strategy
        strategy = await self._get_strategy(strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        # Create rule
        rule = StrategyRule(
            rule_id=f"rule_{strategy_id}_{datetime.now(timezone.utc).timestamp()}",
            condition_type=ConditionType(condition_type),
            condition=condition,
            action=action,
            priority=priority
        )
        
        # Add rule to strategy
        strategy.rules.append(rule)
        strategy.updated_date = datetime.now(timezone.utc)
        
        # Save updated strategy
        await self._save_strategy(strategy)
        
        return rule
    
    async def get_strategy_templates(self) -> List[Dict]:
        """
        Get pre-built strategy templates.
        
        Returns:
            List of strategy template dictionaries
        """
        templates = [
            {
                "template_id": "moving_average_crossover",
                "name": "Moving Average Crossover",
                "description": "Buy when short MA crosses above long MA, sell when it crosses below",
                "rules": [
                    {
                        "condition_type": "indicator",
                        "condition": {
                            "indicator": "SMA",
                            "short_period": 50,
                            "long_period": 200,
                            "comparison": "cross_above"
                        },
                        "action": {
                            "type": "buy",
                            "quantity": 100
                        }
                    },
                    {
                        "condition_type": "indicator",
                        "condition": {
                            "indicator": "SMA",
                            "short_period": 50,
                            "long_period": 200,
                            "comparison": "cross_below"
                        },
                        "action": {
                            "type": "sell",
                            "quantity": 100
                        }
                    }
                ]
            },
            {
                "template_id": "rsi_divergence",
                "name": "RSI Divergence",
                "description": "Buy on RSI oversold, sell on RSI overbought",
                "rules": [
                    {
                        "condition_type": "indicator",
                        "condition": {
                            "indicator": "RSI",
                            "period": 14,
                            "comparison": "below",
                            "value": 30
                        },
                        "action": {
                            "type": "buy",
                            "quantity": 100
                        }
                    },
                    {
                        "condition_type": "indicator",
                        "condition": {
                            "indicator": "RSI",
                            "period": 14,
                            "comparison": "above",
                            "value": 70
                        },
                        "action": {
                            "type": "sell",
                            "quantity": 100
                        }
                    }
                ]
            }
        ]
        
        return templates
    
    async def validate_strategy(self, strategy_id: str) -> Dict:
        """
        Validate strategy for logical errors and risk issues.
        
        Args:
            strategy_id: Strategy identifier
            
        Returns:
            Validation result dictionary
        """
        strategy = await self._get_strategy(strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        errors = []
        warnings = []
        
        # Check for rules
        if not strategy.rules:
            errors.append("Strategy must have at least one rule")
        
        # Check for conflicting rules
        buy_rules = [r for r in strategy.rules if r.action.get('type') == 'buy']
        sell_rules = [r for r in strategy.rules if r.action.get('type') == 'sell']
        
        if not buy_rules:
            warnings.append("Strategy has no buy rules")
        if not sell_rules:
            warnings.append("Strategy has no sell rules")
        
        # Check risk limits
        if not strategy.risk_limits:
            warnings.append("No risk limits defined")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    async def _get_strategy(self, strategy_id: str) -> Optional[TradingStrategy]:
        """Get strategy from DB with cache fallback."""
        cache_key = f"strategy:{strategy_id}"
        strategy_data = self.cache_service.get(cache_key)
        if strategy_data:
            return TradingStrategy(**strategy_data)
        
        # Hit DB
        try:
            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    SELECT strategy_id, user_id, strategy_name, description, rules, 
                           status, portfolio_id, risk_limits, created_date, updated_date, last_executed
                    FROM strategies WHERE strategy_id = %s
                """, (strategy_id,))
                row = cur.fetchone()
                if row:
                    data = {
                        "strategy_id": row[0],
                        "user_id": str(row[1]),
                        "strategy_name": row[2],
                        "description": row[3],
                        "rules": row[4],
                        "status": row[5],
                        "portfolio_id": row[6],
                        "risk_limits": row[7],
                        "created_date": row[8],
                        "updated_date": row[9],
                        "last_executed": row[10]
                    }
                    strategy = TradingStrategy(**data)
                    self.cache_service.set(cache_key, strategy.model_dump(), ttl=3600)
                    return strategy
        except Exception as e:
            logger.error(f"Error fetching strategy from DB: {e}")
            
        return None
    
    async def _save_strategy(self, strategy: TradingStrategy):
        """Save strategy to DB and update cache."""
        try:
            # Convert UUID string to UUID object if needed
            user_id = strategy.user_id
            try:
                user_id_uuid = uuid.UUID(user_id)
            except ValueError:
                # Fallback for dev/mock IDs
                 user_id_uuid = uuid.UUID("00000000-0000-0000-0000-000000000001")

            with db_manager.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO strategies (
                        strategy_id, user_id, strategy_name, description, rules, 
                        status, portfolio_id, risk_limits, last_executed, created_date, updated_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (strategy_id) DO UPDATE SET
                        strategy_name = EXCLUDED.strategy_name,
                        description = EXCLUDED.description,
                        rules = EXCLUDED.rules,
                        status = EXCLUDED.status,
                        portfolio_id = EXCLUDED.portfolio_id,
                        risk_limits = EXCLUDED.risk_limits,
                        last_executed = EXCLUDED.last_executed,
                        updated_date = NOW()
                """, (
                    strategy.strategy_id, user_id_uuid, strategy.strategy_name,
                    strategy.description, json.dumps([r.model_dump() for r in strategy.rules]),
                    strategy.status.value, strategy.portfolio_id,
                    json.dumps(strategy.risk_limits), strategy.last_executed,
                    strategy.created_date, strategy.updated_date
                ))
            
            # Update cache
            cache_key = f"strategy:{strategy.strategy_id}"
            self.cache_service.set(cache_key, strategy.model_dump(), ttl=3600)
            
        except Exception as e:
            logger.error(f"Error saving strategy to DB: {e}")

    async def seed_strategies(self, user_id: str):
        """Seed some initial strategies for development UI."""
        templates = await self.get_strategy_templates()
        for i, template in enumerate(templates):
            await self.create_strategy(
                user_id=user_id,
                strategy_name=f"{template['name']} Beta",
                description=template['description'],
                rules=template['rules']
            )
        logger.info(f"Seeded {len(templates)} strategies for user {user_id}")


# Singleton instance
_strategy_builder_service: Optional[StrategyBuilderService] = None


def get_strategy_builder_service() -> StrategyBuilderService:
    """Get singleton strategy builder service instance."""
    global _strategy_builder_service
    if _strategy_builder_service is None:
        _strategy_builder_service = StrategyBuilderService()
    return _strategy_builder_service
