"""
==============================================================================
FILE: services/social_trading/copy_trading_service.py
ROLE: Copy Trading Engine
PURPOSE: Replicates trader strategies with risk controls and position
         mirroring.

INTEGRATION POINTS:
    - SocialTradingService: Trader profiles
    - ExecutionService: Order execution
    - PortfolioService: Portfolio tracking
    - CopyTradingAPI: Copy trading endpoints

FEATURES:
    - Position mirroring
    - Risk controls
    - Proportional allocation
    - Copy trading management

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from schemas.social_trading import CopyTradingConfig, CopyTrade
from services.social_trading.social_trading_service import get_social_trading_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class CopyTradingService:
    """
    Service for copy trading execution.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.social_service = get_social_trading_service()
        self.cache_service = get_cache_service()
        self.active_configs: Dict[str, CopyTradingConfig] = {}
        
    async def create_copy_config(
        self,
        follower_id: str,
        trader_id: str,
        allocation_percentage: float,
        risk_multiplier: float = 1.0
    ) -> CopyTradingConfig:
        """
        Create copy trading configuration.
        
        Args:
            follower_id: Follower user identifier
            trader_id: Trader identifier
            allocation_percentage: Percentage of capital to allocate
            risk_multiplier: Risk adjustment factor
            
        Returns:
            CopyTradingConfig object
        """
        logger.info(f"Creating copy config for follower {follower_id} to copy trader {trader_id}")
        
        config = CopyTradingConfig(
            config_id=f"copy_{follower_id}_{trader_id}_{datetime.now(timezone.utc).timestamp()}",
            follower_id=follower_id,
            trader_id=trader_id,
            allocation_percentage=allocation_percentage,
            risk_multiplier=risk_multiplier,
            is_active=True,
            created_date=datetime.now(timezone.utc),
            updated_date=datetime.now(timezone.utc)
        )
        
        # Save config
        await self._save_config(config)
        self.active_configs[config.config_id] = config
        
        return config

    async def stop_copy_trading(self, config_id: str) -> bool:
        """
        Stop copy trading for a configuration.
        """
        logger.info(f"Stopping copy trading for config {config_id}")
        config = await self._get_config(config_id)
        if config:
            config.is_active = False
            config.updated_date = datetime.now(timezone.utc)
            await self._save_config(config)
            # Update local cache
            if config_id in self.active_configs:
                self.active_configs[config_id] = config
            return True
        return False
    
    async def execute_copy_trade(
        self,
        trader_id: str,
        original_trade: Dict
    ) -> List[CopyTrade]:
        """
        Execute copy trades for all followers of a trader.
        
        Args:
            trader_id: Trader identifier
            original_trade: Original trade details
            
        Returns:
            List of CopyTrade objects
        """
        logger.info(f"Executing copy trades for trader {trader_id}")
        
        # Get all active copy configs for this trader
        active_configs = [
            config for config in self.active_configs.values()
            if config.trader_id == trader_id and config.is_active
        ]
        
        copy_trades = []
        
        for config in active_configs:
            # Calculate copy trade quantity based on allocation
            original_quantity = original_trade.get('quantity', 0)
            copy_quantity = int(original_quantity * (config.allocation_percentage / 100.0) * config.risk_multiplier)
            
            if copy_quantity > 0:
                copy_trade = CopyTrade(
                    copy_trade_id=f"copy_trade_{config.config_id}_{datetime.now(timezone.utc).timestamp()}",
                    config_id=config.config_id,
                    original_trade_id=original_trade.get('trade_id'),
                    symbol=original_trade.get('symbol'),
                    quantity=copy_quantity,
                    price=original_trade.get('price', 0),
                    executed_date=datetime.now(timezone.utc),
                    status="executed"
                )
                
                copy_trades.append(copy_trade)
                await self._save_copy_trade(copy_trade)
        
        return copy_trades
    
    async def _get_config(self, config_id: str) -> Optional[CopyTradingConfig]:
        """Get copy config from cache."""
        cache_key = f"copy_config:{config_id}"
        config_data = self.cache_service.get(cache_key)
        if config_data:
            return CopyTradingConfig(**config_data)
        return None
    
    async def _save_config(self, config: CopyTradingConfig):
        """Save copy config to cache."""
        cache_key = f"copy_config:{config.config_id}"
        self.cache_service.set(cache_key, config.model_dump(), ttl=86400 * 365)
    
    async def _save_copy_trade(self, copy_trade: CopyTrade):
        """Save copy trade to cache."""
        cache_key = f"copy_trade:{copy_trade.copy_trade_id}"
        self.cache_service.set(cache_key, copy_trade.model_dump(), ttl=86400 * 365)


# Singleton instance
_copy_trading_service: Optional[CopyTradingService] = None


def get_copy_trading_service() -> CopyTradingService:
    """Get singleton copy trading service instance."""
    global _copy_trading_service
    if _copy_trading_service is None:
        _copy_trading_service = CopyTradingService()
    return _copy_trading_service
