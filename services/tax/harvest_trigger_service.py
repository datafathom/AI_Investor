import logging
from uuid import UUID
from typing import List, Dict, Any
from services.tax.enhanced_tax_harvesting_service import EnhancedTaxHarvestingService

logger = logging.getLogger(__name__)

class HarvestTriggerService:
    """
    Automated trigger service for tax-loss harvesting.
    Bridges market data with specific tax lots in Postgres.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HarvestTriggerService, cls).__new__(cls)
        return cls._instance

    def __init__(self, enhanced_harvest_service: EnhancedTaxHarvestingService = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.harvester = enhanced_harvest_service or EnhancedTaxHarvestingService()
        self._initialized = True
        logger.info("HarvestTriggerService initialized")

    async def scan_for_triggers(self, portfolio_id: str) -> List[Dict[str, Any]]:
        """
        Scans tax lots in the portfolio for harvest triggers.
        """
        logger.info(f"TAX_LOG: Scanning portfolio {portfolio_id} for automated harvest triggers")
        
        # In production, this would query the 'tax_lots' table for lots with high cost basis
        # and current low market prices.
        
        opportunities = await self.harvester.identify_harvest_opportunities(portfolio_id)
        
        triggers = []
        for opp in opportunities:
            if opp.net_benefit > 1000: # Automatic trigger threshold
                logger.info(f"TAX_ALERT: AUTOMATIC TRIGGER for {opp.candidate.ticker} in portfolio {portfolio_id}. Benefit: ${opp.net_benefit}")
                triggers.append({
                    "ticker": opp.candidate.ticker,
                    "benefit": opp.net_benefit,
                    "status": "TRIGGERED"
                })
                
        return triggers
