"""
==============================================================================
FILE: services/tax/enhanced_tax_harvesting_service.py
ROLE: Enhanced Tax-Loss Harvesting Engine
PURPOSE: Identifies and executes tax-loss harvesting opportunities with
         wash-sale protection, replacement suggestions, and batch processing.

INTEGRATION POINTS:
    - TaxHarvestService: Existing tax harvesting infrastructure
    - PortfolioService: Portfolio holdings and cost basis
    - ExecutionService: Trade execution for harvesting
    - MarketDataService: Replacement asset correlation data
    - NotificationService: Harvesting opportunity alerts

FEATURES:
    - Automated opportunity scanning
    - 30-day wash-sale lookback
    - Correlated replacement suggestions
    - Batch harvesting processing
    - Tax savings estimation

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from services.tax.harvest_service import TaxHarvestService, HarvestCandidate
from services.portfolio.portfolio_aggregator import get_portfolio_aggregator
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


@dataclass
class EnhancedHarvestOpportunity:
    """Enhanced harvest opportunity with additional metadata."""
    candidate: HarvestCandidate
    tax_savings: float
    net_benefit: float  # After transaction costs
    replacement_suggestions: List[Dict[str, any]]
    wash_sale_risk: bool
    rank: int = 0


@dataclass
class BatchHarvestResult:
    """Result of batch harvesting operation."""
    opportunities: List[EnhancedHarvestOpportunity]
    total_tax_savings: float
    total_net_benefit: float
    trades_required: int
    requires_approval: bool


class EnhancedTaxHarvestingService:
    """
    Enhanced tax-loss harvesting service with batch processing and optimization.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.base_service = TaxHarvestService()
        self.portfolio_aggregator = get_portfolio_aggregator()
        self.cache_service = get_cache_service()
        self.default_threshold_dollar = 500.0
        self.default_threshold_pct = 0.05  # 5%
        self.approval_threshold = 5000.0  # $5,000
        self.transaction_cost_rate = 0.001  # 0.1%
        
    async def identify_harvest_opportunities(
        self,
        portfolio_id: str,
        min_loss_dollar: Optional[float] = None,
        min_loss_pct: Optional[float] = None
    ) -> List[EnhancedHarvestOpportunity]:
        """
        Identify all harvest opportunities with enhanced analysis.
        
        Args:
            portfolio_id: Portfolio identifier
            min_loss_dollar: Minimum loss in dollars (default: $500)
            min_loss_pct: Minimum loss percentage (default: 5%)
            
        Returns:
            List of enhanced harvest opportunities ranked by net benefit
        """
        logger.info(f"Identifying harvest opportunities for portfolio {portfolio_id}")
        
        min_loss_dollar = min_loss_dollar or self.default_threshold_dollar
        min_loss_pct = min_loss_pct or self.default_threshold_pct
        
        # Get base candidates
        base_candidates = await self.base_service.identify_harvest_candidates(
            portfolio_id=portfolio_id,
            min_loss=min_loss_dollar
        )
        
        # Enhance with additional analysis
        opportunities = []
        for candidate in base_candidates:
            # Calculate tax savings
            tax_savings = await self._calculate_tax_savings(candidate)
            
            # Estimate transaction costs
            transaction_cost = await self._estimate_transaction_cost(candidate)
            
            # Calculate net benefit
            net_benefit = tax_savings - transaction_cost
            
            # Get replacement suggestions
            replacements = await self.base_service.suggest_replacement_assets(candidate.ticker)
            
            # Check wash-sale risk
            wash_check = await self.base_service.check_wash_sale_violation(
                candidate.ticker,
                portfolio_id
            )
            wash_sale_risk = wash_check.is_violation if wash_check else False
            
            # Check percentage threshold
            loss_pct = abs(candidate.unrealized_loss) / candidate.cost_basis if candidate.cost_basis > 0 else 0.0
            if loss_pct < min_loss_pct and abs(candidate.unrealized_loss) < min_loss_dollar:
                continue
            
            opportunities.append(EnhancedHarvestOpportunity(
                candidate=candidate,
                tax_savings=tax_savings,
                net_benefit=net_benefit,
                replacement_suggestions=replacements,
                wash_sale_risk=wash_sale_risk,
                rank=0  # Will be set after sorting
            ))
        
        # Rank by net benefit
        opportunities.sort(key=lambda x: x.net_benefit, reverse=True)
        for idx, opp in enumerate(opportunities):
            opp.rank = idx + 1
        
        return opportunities
    
    async def batch_harvest_analysis(
        self,
        portfolio_id: str,
        opportunities: Optional[List[EnhancedHarvestOpportunity]] = None
    ) -> BatchHarvestResult:
        """
        Analyze batch harvesting of multiple opportunities.
        
        Args:
            portfolio_id: Portfolio identifier
            opportunities: Optional pre-identified opportunities
            
        Returns:
            BatchHarvestResult with batch analysis
        """
        if opportunities is None:
            opportunities = await self.identify_harvest_opportunities(portfolio_id)
        
        # Filter out wash-sale risks
        safe_opportunities = [opp for opp in opportunities if not opp.wash_sale_risk]
        
        # Calculate totals
        total_tax_savings = sum(opp.tax_savings for opp in safe_opportunities)
        total_net_benefit = sum(opp.net_benefit for opp in safe_opportunities)
        trades_required = len(safe_opportunities) * 2  # Sell + Buy for each
        
        # Check if approval needed
        requires_approval = total_net_benefit > self.approval_threshold
        
        return BatchHarvestResult(
            opportunities=safe_opportunities,
            total_tax_savings=total_tax_savings,
            total_net_benefit=total_net_benefit,
            trades_required=trades_required,
            requires_approval=requires_approval
        )

    async def check_wash_sale_violation(
        self,
        portfolio_id: str,
        symbol: str,
        sale_date: datetime
    ) -> any:
        """Wrapper for base service wash-sale check."""
        return await self.base_service.check_wash_sale_violation(symbol, portfolio_id)
    
    async def execute_harvest(
        self,
        portfolio_id: str,
        opportunity: EnhancedHarvestOpportunity,
        replacement_symbol: Optional[str] = None,
        approved: bool = False
    ) -> Dict:
        """
        Execute tax-loss harvest trade.
        
        Args:
            portfolio_id: Portfolio identifier
            opportunity: Harvest opportunity to execute
            replacement_symbol: Optional replacement symbol (if None, uses suggestion)
            approved: Whether user has approved the trade
            
        Returns:
            Execution result
        """
        if opportunity.requires_approval and not approved:
            raise ValueError("Harvest requires approval but was not approved")
        
        if opportunity.wash_sale_risk:
            raise ValueError("Cannot execute harvest with wash-sale risk")
        
        logger.info(f"Executing harvest for {opportunity.candidate.ticker} in portfolio {portfolio_id}")
        
        # Select replacement
        if replacement_symbol is None:
            if opportunity.replacement_suggestions:
                replacement_symbol = opportunity.replacement_suggestions[0].get('symbol')
            else:
                raise ValueError("No replacement symbol provided or suggested")
        
        # Execute trades (in production, call execution service)
        # For now, return mock execution result
        return {
            'success': True,
            'harvest_trade': {
                'symbol': opportunity.candidate.ticker,
                'action': 'SELL',
                'quantity': opportunity.candidate.position_id,  # Simplified
                'realized_loss': abs(opportunity.candidate.unrealized_loss)
            },
            'replacement_trade': {
                'symbol': replacement_symbol,
                'action': 'BUY',
                'quantity': opportunity.candidate.position_id  # Simplified
            },
            'tax_savings': opportunity.tax_savings,
            'execution_date': datetime.now(timezone.utc).isoformat()
        }
    
    async def _calculate_tax_savings(self, candidate: HarvestCandidate) -> float:
        """Calculate tax savings from harvesting."""
        loss = abs(candidate.unrealized_loss)
        
        # Determine tax rate
        if candidate.is_long_term:
            tax_rate = 0.15  # Long-term capital gains
        else:
            tax_rate = 0.32  # Short-term (marginal rate)
        
        tax_savings = loss * tax_rate
        return tax_savings
    
    async def _estimate_transaction_cost(self, candidate: HarvestCandidate) -> float:
        """Estimate transaction costs."""
        trade_value = candidate.current_value
        transaction_cost = trade_value * self.transaction_cost_rate * 2  # Buy + Sell
        return transaction_cost


# Singleton instance
_enhanced_harvest_service: Optional[EnhancedTaxHarvestingService] = None


def get_enhanced_harvest_service() -> EnhancedTaxHarvestingService:
    """Get singleton enhanced harvest service instance."""
    global _enhanced_harvest_service
    if _enhanced_harvest_service is None:
        _enhanced_harvest_service = EnhancedTaxHarvestingService()
    return _enhanced_harvest_service
