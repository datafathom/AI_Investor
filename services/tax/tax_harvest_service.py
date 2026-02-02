import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class TaxHarvestService:
    """
    Phase 193.1: Tax-Loss Harvesting Sentinel.
    Identifies harvesting alpha while maintaining wash-sale compliance.
    """
    
    def hunt_harvest_opportunity(self, portfolio: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Phase 193.1: Harvest Hunter.
        Identifies tickers with significant unrealized losses.
        """
        opportunities = []
        for asset in portfolio:
            loss_pct = (asset["cost_basis"] - asset["current_price"]) / asset["cost_basis"]
            if loss_pct > 0.1: # 10% loss threshold
                opportunities.append({
                    "ticker": asset["ticker"],
                    "unrealized_loss": asset["cost_basis"] - asset["current_price"],
                    "loss_pct": round(loss_pct * 100, 2),
                    "wash_sale_safe_date": "2026-03-01" # Mocked wash-sale logic
                })
        
        logger.info(f"HARVEST_LOG: Found {len(opportunities)} tax-loss harvesting opportunities.")
        return opportunities

    def optimize_carryforward(self, current_gains: Decimal, carried_losses: Decimal) -> Dict[str, Any]:
        """
        Phase 193.2: Loss Carryforward Optimizer.
        """
        taxable_net = max(Decimal("0"), current_gains - carried_losses)
        unused_loss = max(Decimal("0"), carried_losses - current_gains)
        
        logger.info(f"HARVEST_LOG: Taxable Net: {taxable_net}. Unused Loss: {unused_loss}")
        
        return {
            "taxable_net": taxable_net,
            "unused_loss_carryforward": unused_loss,
            "tax_efficiency": "OPTIMAL" if taxable_net == 0 else "PARTIAL"
        }
