"""
==============================================================================
FILE: services/tax/tax_optimization_service.py
ROLE: Tax Optimization Service
PURPOSE: Optimizes portfolio decisions for tax efficiency including lot
         selection, tax-aware rebalancing, and tax projections.

INTEGRATION POINTS:
    - PortfolioService: Holdings and lot-level cost basis
    - TaxHarvestService: Harvesting opportunities
    - RebalancingService: Tax-aware rebalancing
    - TaxProjectionService: Year-end tax planning

FEATURES:
    - FIFO/LIFO/Highest Cost/Specific Lot selection
    - Tax-aware rebalancing optimization
    - Year-end tax projections
    - Tax-efficient withdrawal sequencing

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class LotSelectionMethod(str, Enum):
    """Lot selection methods."""
    FIFO = "fifo"  # First In, First Out
    LIFO = "lifo"  # Last In, First Out
    HIGHEST_COST = "highest_cost"
    LOWEST_COST = "lowest_cost"
    SPECIFIC_LOT = "specific_lot"


class TaxOptimizationService:
    """
    Service for tax optimization.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        
    async def optimize_lot_selection(
        self,
        portfolio_id: str,
        symbol: str,
        quantity: float,
        method: str = "highest_cost"
    ) -> Dict:
        """
        Optimize lot selection for tax efficiency.
        
        Args:
            portfolio_id: Portfolio identifier
            symbol: Symbol to sell
            quantity: Quantity to sell
            method: Lot selection method
            
        Returns:
            Optimal lot selection with tax impact
        """
        logger.info(f"Optimizing lot selection for {symbol} in portfolio {portfolio_id}")
        
        # Get lots for symbol
        lots = await self._get_lots(portfolio_id, symbol)
        
        if not lots:
            raise ValueError(f"No lots found for {symbol}")
        
        # Select lots based on method
        selected_lots = await self._select_lots(lots, quantity, method)
        
        # Calculate tax impact
        total_cost_basis = sum(lot['cost_basis'] for lot in selected_lots)
        current_price = await self._get_current_price(symbol)
        proceeds = quantity * current_price
        gain_loss = proceeds - total_cost_basis
        
        tax_impact = await self._calculate_tax_impact(gain_loss, selected_lots)
        
        return {
            'symbol': symbol,
            'quantity': quantity,
            'method': method,
            'selected_lots': selected_lots,
            'total_cost_basis': total_cost_basis,
            'proceeds': proceeds,
            'gain_loss': gain_loss,
            'tax_impact': tax_impact
        }
    
    async def project_year_end_tax(
        self,
        portfolio_id: str,
        planned_transactions: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Project year-end tax liability.
        
        Args:
            portfolio_id: Portfolio identifier
            planned_transactions: Optional list of planned transactions
            
        Returns:
            Tax projection with breakdown
        """
        logger.info(f"Projecting year-end tax for portfolio {portfolio_id}")
        
        # Get current realized gains/losses
        realized_gains = await self._get_realized_gains(portfolio_id)
        
        # Get unrealized gains/losses
        unrealized_gains = await self._get_unrealized_gains(portfolio_id)
        
        # Estimate impact of planned transactions
        planned_impact = 0.0
        if planned_transactions:
            for transaction in planned_transactions:
                impact = await self._estimate_transaction_tax_impact(transaction)
                planned_impact += impact
        
        # Calculate total taxable income
        total_realized = sum(g.get('gain', 0) for g in realized_gains)
        total_planned = planned_impact
        
        # Estimate tax liability
        tax_liability = await self._calculate_tax_liability(
            total_realized + total_planned,
            realized_gains
        )
        
        return {
            'portfolio_id': portfolio_id,
            'realized_gains_losses': total_realized,
            'planned_transaction_impact': total_planned,
            'estimated_tax_liability': tax_liability,
            'breakdown': {
                'short_term': sum(g.get('gain', 0) for g in realized_gains if not g.get('long_term', False)),
                'long_term': sum(g.get('gain', 0) for g in realized_gains if g.get('long_term', False))
            },
            'projection_date': datetime.utcnow().isoformat()
        }
    
    async def optimize_withdrawal_sequence(
        self,
        portfolio_id: str,
        withdrawal_amount: float,
        account_types: List[str] = ["taxable", "tax_deferred", "tax_free"]
    ) -> Dict:
        """
        Optimize withdrawal sequence for tax efficiency.
        
        Args:
            portfolio_id: Portfolio identifier
            withdrawal_amount: Total amount to withdraw
            account_types: Available account types
            
        Returns:
            Optimal withdrawal sequence
        """
        logger.info(f"Optimizing withdrawal sequence for portfolio {portfolio_id}")
        
        # Get account balances
        accounts = await self._get_account_balances(portfolio_id, account_types)
        
        # Optimize sequence: taxable -> tax_deferred -> tax_free
        sequence = []
        remaining = withdrawal_amount
        
        for account_type in ["taxable", "tax_deferred", "tax_free"]:
            if remaining <= 0:
                break
            
            account = accounts.get(account_type, {})
            balance = account.get('balance', 0.0)
            
            if balance > 0:
                withdrawal = min(remaining, balance)
                sequence.append({
                    'account_type': account_type,
                    'amount': withdrawal,
                    'tax_rate': account.get('tax_rate', 0.0)
                })
                remaining -= withdrawal
        
        total_tax = sum(s['amount'] * s['tax_rate'] for s in sequence)
        
        return {
            'withdrawal_amount': withdrawal_amount,
            'sequence': sequence,
            'total_tax': total_tax,
            'after_tax_amount': withdrawal_amount - total_tax
        }
    
    # Private helper methods
    
    async def _get_lots(self, portfolio_id: str, symbol: str) -> List[Dict]:
        """Get lots for a symbol."""
        # In production, fetch from portfolio service
        return [
            {'lot_id': 'lot1', 'quantity': 50, 'cost_basis': 150.0, 'purchase_date': '2023-01-15'},
            {'lot_id': 'lot2', 'quantity': 30, 'cost_basis': 160.0, 'purchase_date': '2023-06-20'},
            {'lot_id': 'lot3', 'quantity': 20, 'cost_basis': 140.0, 'purchase_date': '2024-01-10'}
        ]
    
    async def _select_lots(
        self,
        lots: List[Dict],
        quantity: float,
        method: str
    ) -> List[Dict]:
        """Select lots based on method."""
        selected = []
        remaining = quantity
        
        if method == "highest_cost":
            sorted_lots = sorted(lots, key=lambda x: x['cost_basis'], reverse=True)
        elif method == "lowest_cost":
            sorted_lots = sorted(lots, key=lambda x: x['cost_basis'])
        elif method == "fifo":
            sorted_lots = sorted(lots, key=lambda x: x['purchase_date'])
        elif method == "lifo":
            sorted_lots = sorted(lots, key=lambda x: x['purchase_date'], reverse=True)
        else:
            sorted_lots = lots
        
        for lot in sorted_lots:
            if remaining <= 0:
                break
            lot_qty = min(remaining, lot['quantity'])
            selected.append({
                **lot,
                'selected_quantity': lot_qty
            })
            remaining -= lot_qty
        
        return selected
    
    async def _get_current_price(self, symbol: str) -> float:
        """Get current price for symbol."""
        # In production, fetch from market data service
        return 100.0
    
    async def _calculate_tax_impact(
        self,
        gain_loss: float,
        lots: List[Dict]
    ) -> Dict:
        """Calculate tax impact of gain/loss."""
        # Determine if long-term or short-term
        # Simplified: assume all lots are long-term if held > 1 year
        is_long_term = True  # Simplified
        
        if gain_loss < 0:  # Loss
            tax_rate = 0.15 if is_long_term else 0.32
            tax_benefit = abs(gain_loss) * tax_rate
            return {
                'gain_loss': gain_loss,
                'tax_rate': tax_rate,
                'tax_impact': -tax_benefit,  # Negative = benefit
                'is_loss': True
            }
        else:  # Gain
            tax_rate = 0.15 if is_long_term else 0.32
            tax_cost = gain_loss * tax_rate
            return {
                'gain_loss': gain_loss,
                'tax_rate': tax_rate,
                'tax_impact': tax_cost,
                'is_loss': False
            }
    
    async def _get_realized_gains(self, portfolio_id: str) -> List[Dict]:
        """Get realized gains/losses for year."""
        # In production, fetch from transaction history
        return []
    
    async def _get_unrealized_gains(self, portfolio_id: str) -> List[Dict]:
        """Get unrealized gains/losses."""
        # In production, fetch from portfolio service
        return []
    
    async def _estimate_transaction_tax_impact(self, transaction: Dict) -> float:
        """Estimate tax impact of planned transaction."""
        # Simplified calculation
        return 0.0
    
    async def _calculate_tax_liability(
        self,
        total_gains: float,
        realized_gains: List[Dict]
    ) -> float:
        """Calculate estimated tax liability."""
        # Simplified: assume 20% on long-term, 32% on short-term
        long_term = sum(g.get('gain', 0) for g in realized_gains if g.get('long_term', False))
        short_term = sum(g.get('gain', 0) for g in realized_gains if not g.get('long_term', False))
        
        return long_term * 0.20 + short_term * 0.32
    
    async def _get_account_balances(
        self,
        portfolio_id: str,
        account_types: List[str]
    ) -> Dict[str, Dict]:
        """Get account balances by type."""
        # In production, fetch from portfolio service
        return {
            'taxable': {'balance': 50000.0, 'tax_rate': 0.20},
            'tax_deferred': {'balance': 200000.0, 'tax_rate': 0.25},
            'tax_free': {'balance': 50000.0, 'tax_rate': 0.0}
        }


# Singleton instance
_tax_optimization_service: Optional[TaxOptimizationService] = None


def get_tax_optimization_service() -> TaxOptimizationService:
    """Get singleton tax optimization service instance."""
    global _tax_optimization_service
    if _tax_optimization_service is None:
        _tax_optimization_service = TaxOptimizationService()
    return _tax_optimization_service
