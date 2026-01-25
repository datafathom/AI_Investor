"""
==============================================================================
FILE: services/portfolio/portfolio_aggregator.py
ROLE: Portfolio Aggregation Service
PURPOSE: Aggregates positions from multiple brokerage sources (Alpaca, IBKR,
         Robinhood) into a unified portfolio view with cost basis and gains.

INTEGRATION POINTS:
    - AlpacaClient: Alpaca positions
    - IBKRClient: IBKR positions
    - RobinhoodClient: Robinhood positions
    - PortfolioManager: Unified portfolio state

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)


class PortfolioAggregator:
    """
    Service for aggregating positions from multiple brokerages.
    """
    
    def __init__(self, mock: bool = False):
        """
        Initialize portfolio aggregator.
        
        Args:
            mock: Use mock mode if True
        """
        self.mock = mock
    
    async def aggregate_positions(
        self,
        user_id: str,
        include_alpaca: bool = True,
        include_ibkr: bool = False,
        include_robinhood: bool = False
    ) -> Dict[str, Any]:
        """
        Aggregate positions from all connected brokerages.
        
        Args:
            user_id: User ID
            include_alpaca: Include Alpaca positions
            include_ibkr: Include IBKR positions
            include_robinhood: Include Robinhood positions
            
        Returns:
            Dict with aggregated positions and totals
        """
        if self.mock:
            await asyncio.sleep(0.5)
            return {
                "positions": [
                    {
                        "symbol": "AAPL",
                        "quantity": 100,
                        "cost_basis": 15000.00,
                        "current_value": 15025.00,
                        "unrealized_gain": 25.00,
                        "sources": ["alpaca"]
                    }
                ],
                "total_cost_basis": 15000.00,
                "total_current_value": 15025.00,
                "total_unrealized_gain": 25.00,
                "sources": ["alpaca"]
            }
        
        aggregated = defaultdict(lambda: {
            "quantity": 0,
            "cost_basis": 0.0,
            "current_value": 0.0,
            "sources": []
        })
        
        # Aggregate from each source
        if include_alpaca:
            try:
                from services.brokerage.alpaca_client import get_alpaca_client
                alpaca = get_alpaca_client()
                alpaca_positions = await alpaca.get_positions()
                for pos in alpaca_positions:
                    symbol = pos.get("symbol")
                    aggregated[symbol]["quantity"] += float(pos.get("qty", 0))
                    aggregated[symbol]["cost_basis"] += float(pos.get("cost_basis", 0))
                    aggregated[symbol]["current_value"] += float(pos.get("market_value", 0))
                    aggregated[symbol]["sources"].append("alpaca")
            except Exception as e:
                logger.error(f"Failed to aggregate Alpaca positions: {e}")
        
        if include_robinhood:
            try:
                from services.brokerage.robinhood_client import get_robinhood_client
                robinhood = get_robinhood_client()
                rh_holdings = await robinhood.get_holdings()
                for holding in rh_holdings:
                    symbol = holding.get("symbol")
                    quantity = float(holding.get("quantity", 0))
                    avg_cost = float(holding.get("average_buy_price", 0))
                    current_price = float(holding.get("current_price", 0))
                    
                    aggregated[symbol]["quantity"] += quantity
                    aggregated[symbol]["cost_basis"] += quantity * avg_cost
                    aggregated[symbol]["current_value"] += quantity * current_price
                    aggregated[symbol]["sources"].append("robinhood")
            except Exception as e:
                logger.error(f"Failed to aggregate Robinhood positions: {e}")
        
        if include_ibkr:
            try:
                from services.brokerage.ibkr_client import get_ibkr_client
                ibkr = get_ibkr_client()
                if not ibkr.connected:
                    await ibkr.connect()
                ibkr_positions = await ibkr.get_positions()
                for pos in ibkr_positions:
                    symbol = pos.get("symbol")
                    quantity = float(pos.get("position", 0))
                    avg_cost = float(pos.get("avg_cost", 0))
                    market_value = float(pos.get("market_value", 0))
                    
                    aggregated[symbol]["quantity"] += quantity
                    aggregated[symbol]["cost_basis"] += quantity * avg_cost
                    aggregated[symbol]["current_value"] += market_value
                    aggregated[symbol]["sources"].append("ibkr")
            except Exception as e:
                logger.error(f"Failed to aggregate IBKR positions: {e}")
        
        # Format aggregated positions
        positions = []
        total_cost_basis = 0.0
        total_current_value = 0.0
        
        for symbol, data in aggregated.items():
            if data["quantity"] == 0:
                continue
            
            unrealized_gain = data["current_value"] - data["cost_basis"]
            
            positions.append({
                "symbol": symbol,
                "quantity": data["quantity"],
                "cost_basis": data["cost_basis"],
                "current_value": data["current_value"],
                "unrealized_gain": unrealized_gain,
                "unrealized_gain_pct": (unrealized_gain / data["cost_basis"] * 100) if data["cost_basis"] > 0 else 0,
                "sources": data["sources"]
            })
            
            total_cost_basis += data["cost_basis"]
            total_current_value += data["current_value"]
        
        return {
            "positions": positions,
            "total_cost_basis": total_cost_basis,
            "total_current_value": total_current_value,
            "total_unrealized_gain": total_current_value - total_cost_basis,
            "aggregated_at": datetime.now().isoformat()
        }
    
    async def calculate_unified_gains(
        self,
        user_id: str,
        include_crypto: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate unified gains across all brokerages.
        
        Args:
            user_id: User ID
            include_crypto: Include cryptocurrency positions
            
        Returns:
            Dict with total gains breakdown
        """
        positions_data = await self.aggregate_positions(user_id)
        
        total_gain = positions_data["total_unrealized_gain"]
        total_gain_pct = (total_gain / positions_data["total_cost_basis"] * 100) if positions_data["total_cost_basis"] > 0 else 0
        
        return {
            "total_unrealized_gain": total_gain,
            "total_unrealized_gain_pct": total_gain_pct,
            "total_cost_basis": positions_data["total_cost_basis"],
            "total_current_value": positions_data["total_current_value"],
            "position_count": len(positions_data["positions"])
        }


# Singleton instance
_portfolio_aggregator: Optional[PortfolioAggregator] = None


def get_portfolio_aggregator(mock: bool = True) -> PortfolioAggregator:
    """
    Get singleton portfolio aggregator instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        PortfolioAggregator instance
    """
    global _portfolio_aggregator
    
    if _portfolio_aggregator is None:
        _portfolio_aggregator = PortfolioAggregator(mock=mock)
        logger.info(f"Portfolio aggregator initialized (mock={mock})")
    
    return _portfolio_aggregator
