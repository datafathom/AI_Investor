"""
==============================================================================
FILE: services/options/strategy_builder_service.py
ROLE: Options Strategy Builder
PURPOSE: Enables construction and validation of multi-leg options strategies
         with visual interface and strategy templates.

INTEGRATION POINTS:
    - OptionsDataService: Options chain data
    - OptionsPricingService: Strategy pricing and Greeks
    - ExecutionService: Strategy order execution
    - OptionsAPI: Strategy endpoints
    - FrontendOptions: Strategy builder UI

FEATURES:
    - Multi-leg strategy construction
    - Strategy templates (covered calls, protective puts, etc.)
    - Strategy validation
    - Risk/reward visualization

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.options import OptionsStrategy, OptionLeg, OptionType, OptionAction
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class OptionsStrategyBuilderService:
    """
    Service for building and validating options strategies.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
        # Strategy templates
        self.templates = {
            "covered_call": self._covered_call_template,
            "protective_put": self._protective_put_template,
            "collar": self._collar_template,
            "straddle": self._straddle_template,
            "strangle": self._strangle_template,
            "butterfly": self._butterfly_template,
            "iron_condor": self._iron_condor_template,
            "iron_butterfly": self._iron_butterfly_template
        }
    
    def get_strategy_templates(self) -> List[str]:
        """Get list of available strategy templates."""
        return list(self.templates.keys())
    
    async def create_strategy(
        self,
        strategy_name: str,
        underlying_symbol: str,
        legs: List[Dict],
        strategy_type: str = "custom"
    ) -> OptionsStrategy:
        """
        Create a new options strategy.
        
        Args:
            strategy_name: Name of the strategy
            underlying_symbol: Underlying stock symbol
            legs: List of leg dictionaries
            strategy_type: Type of strategy (template name or "custom")
            
        Returns:
            OptionsStrategy with calculated metrics
        """
        logger.info(f"Creating strategy {strategy_name} for {underlying_symbol}")
        
        # Convert legs to OptionLeg objects
        option_legs = []
        for leg_data in legs:
            leg = OptionLeg(**leg_data)
            option_legs.append(leg)
        
        # Validate strategy
        validation_result = await self.validate_strategy(option_legs)
        if not validation_result['valid']:
            raise ValueError(f"Invalid strategy: {validation_result['errors']}")
        
        # Calculate net cost and risk metrics
        net_cost = await self._calculate_net_cost(option_legs)
        max_profit, max_loss, breakeven = await self._calculate_risk_reward(option_legs)
        
        strategy = OptionsStrategy(
            strategy_id=f"strat_{underlying_symbol}_{datetime.utcnow().timestamp()}",
            strategy_name=strategy_name,
            underlying_symbol=underlying_symbol,
            legs=option_legs,
            net_cost=net_cost,
            max_profit=max_profit,
            max_loss=max_loss,
            breakeven_points=breakeven,
            created_date=datetime.utcnow(),
            strategy_type=strategy_type
        )
        
        # Cache strategy
        cache_key = f"strategy:{strategy.strategy_id}"
        self.cache_service.set(cache_key, strategy.dict(), ttl=86400)
        
        return strategy
    
    async def create_from_template(
        self,
        template_name: str,
        underlying_symbol: str,
        current_price: float,
        expiration: datetime,
        **kwargs
    ) -> OptionsStrategy:
        """
        Create strategy from template.
        
        Args:
            template_name: Name of template
            underlying_symbol: Underlying stock symbol
            current_price: Current stock price
            expiration: Option expiration date
            **kwargs: Template-specific parameters
            
        Returns:
            OptionsStrategy created from template
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template_func = self.templates[template_name]
        legs = template_func(underlying_symbol, current_price, expiration, **kwargs)
        
        return await self.create_strategy(
            strategy_name=template_name.replace('_', ' ').title(),
            underlying_symbol=underlying_symbol,
            legs=legs,
            strategy_type=template_name
        )
    
    async def validate_strategy(self, legs: List[OptionLeg]) -> Dict:
        """
        Validate strategy for logical consistency.
        
        Args:
            legs: List of option legs
            
        Returns:
            Validation result with errors if any
        """
        errors = []
        
        if len(legs) == 0:
            errors.append("Strategy must have at least one leg")
        
        if len(legs) > 10:
            errors.append("Strategy cannot have more than 10 legs")
        
        # Validate call spreads (long strike < short strike)
        call_legs = [l for l in legs if l.option_type == OptionType.CALL]
        if len(call_legs) >= 2:
            buy_calls = [l for l in call_legs if l.action == OptionAction.BUY]
            sell_calls = [l for l in call_legs if l.action == OptionAction.SELL]
            
            if buy_calls and sell_calls:
                max_buy_strike = max(l.strike for l in buy_calls)
                min_sell_strike = min(l.strike for l in sell_calls)
                if max_buy_strike >= min_sell_strike:
                    errors.append("Call spread: Long strike must be less than short strike")
        
        # Validate put spreads (long strike > short strike)
        put_legs = [l for l in legs if l.option_type == OptionType.PUT]
        if len(put_legs) >= 2:
            buy_puts = [l for l in put_legs if l.action == OptionAction.BUY]
            sell_puts = [l for l in put_legs if l.action == OptionAction.SELL]
            
            if buy_puts and sell_puts:
                min_buy_strike = min(l.strike for l in buy_puts)
                max_sell_strike = max(l.strike for l in sell_puts)
                if min_buy_strike <= max_sell_strike:
                    errors.append("Put spread: Long strike must be greater than short strike")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    async def _calculate_net_cost(self, legs: List[OptionLeg]) -> float:
        """Calculate net cost/premium of strategy."""
        total_cost = 0.0
        
        for leg in legs:
            premium = leg.premium or await self._get_option_premium(leg)
            cost = premium * leg.quantity
            
            if leg.action == OptionAction.BUY:
                total_cost += cost
            else:  # SELL
                total_cost -= cost
        
        return total_cost
    
    async def _calculate_risk_reward(
        self,
        legs: List[OptionLeg]
    ) -> tuple[Optional[float], Optional[float], List[float]]:
        """Calculate max profit, max loss, and breakeven points."""
        # Simplified calculation
        # In production, use proper options pricing models
        
        net_cost = await self._calculate_net_cost(legs)
        
        # For credit spreads, max profit is net credit, max loss is difference in strikes - net credit
        # For debit spreads, max profit is difference in strikes - net debit, max loss is net debit
        # This is simplified - full calculation requires analyzing all legs
        
        max_profit = None  # Would calculate based on strategy type
        max_loss = abs(net_cost)  # Simplified
        breakeven = []  # Would calculate based on strategy type
        
        return max_profit, max_loss, breakeven
    
    async def _get_option_premium(self, leg: OptionLeg) -> float:
        """Get option premium (mock for now)."""
        # In production, fetch from options data service
        return 5.0  # Mock premium
    
    # Template functions
    
    def _covered_call_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Covered call template: Long stock + Short call."""
        strike = strike or current_price * 1.05
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.SELL,
                'strike': strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _protective_put_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Protective put template: Long stock + Long put."""
        strike = strike or current_price * 0.95
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.BUY,
                'strike': strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _collar_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        put_strike: Optional[float] = None,
        call_strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Collar template: Long stock + Long put + Short call."""
        put_strike = put_strike or current_price * 0.95
        call_strike = call_strike or current_price * 1.05
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.BUY,
                'strike': put_strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.SELL,
                'strike': call_strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _straddle_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Straddle template: Long call + Long put at same strike."""
        strike = strike or current_price
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.BUY,
                'strike': strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.BUY,
                'strike': strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _strangle_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        call_strike: Optional[float] = None,
        put_strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Strangle template: Long call + Long put at different strikes."""
        call_strike = call_strike or current_price * 1.05
        put_strike = put_strike or current_price * 0.95
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.BUY,
                'strike': call_strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.BUY,
                'strike': put_strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _butterfly_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        lower_strike: Optional[float] = None,
        middle_strike: Optional[float] = None,
        upper_strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Butterfly template: Long lower strike + Short 2x middle strike + Long upper strike."""
        lower_strike = lower_strike or current_price * 0.90
        middle_strike = middle_strike or current_price
        upper_strike = upper_strike or current_price * 1.10
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.BUY,
                'strike': lower_strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.SELL,
                'strike': middle_strike,
                'expiration': expiration,
                'quantity': quantity * 2
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.BUY,
                'strike': upper_strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _iron_condor_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        put_lower: Optional[float] = None,
        put_upper: Optional[float] = None,
        call_lower: Optional[float] = None,
        call_upper: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Iron condor template: Sell put spread + Sell call spread."""
        put_lower = put_lower or current_price * 0.90
        put_upper = put_upper or current_price * 0.95
        call_lower = call_lower or current_price * 1.05
        call_upper = call_upper or current_price * 1.10
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.BUY,
                'strike': put_lower,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.SELL,
                'strike': put_upper,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.SELL,
                'strike': call_lower,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.BUY,
                'strike': call_upper,
                'expiration': expiration,
                'quantity': quantity
            }
        ]
    
    def _iron_butterfly_template(
        self,
        symbol: str,
        current_price: float,
        expiration: datetime,
        lower_strike: Optional[float] = None,
        middle_strike: Optional[float] = None,
        upper_strike: Optional[float] = None,
        quantity: int = 100
    ) -> List[Dict]:
        """Iron butterfly template: Sell straddle + Buy wings."""
        lower_strike = lower_strike or current_price * 0.95
        middle_strike = middle_strike or current_price
        upper_strike = upper_strike or current_price * 1.05
        return [
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.BUY,
                'strike': lower_strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.PUT,
                'action': OptionAction.SELL,
                'strike': middle_strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.SELL,
                'strike': middle_strike,
                'expiration': expiration,
                'quantity': quantity
            },
            {
                'symbol': symbol,
                'option_type': OptionType.CALL,
                'action': OptionAction.BUY,
                'strike': upper_strike,
                'expiration': expiration,
                'quantity': quantity
            }
        ]


# Singleton instance
_strategy_builder_service: Optional[OptionsStrategyBuilderService] = None


def get_strategy_builder_service() -> OptionsStrategyBuilderService:
    """Get singleton strategy builder service instance."""
    global _strategy_builder_service
    if _strategy_builder_service is None:
        _strategy_builder_service = OptionsStrategyBuilderService()
    return _strategy_builder_service
