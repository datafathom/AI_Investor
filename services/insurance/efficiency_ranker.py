import logging
from typing import List, Dict, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class TaxEfficiencyRanker:
    """
    Phase 177.1: High-Yield Asset Selection Algorithm.
    Ranks assets by 'Tax Drag' to prioritize PPLI placement.
    Formula: Tax Drag = (Yield * OrdRate) + (Turnover * STRate)
    """
    
    def rank_assets(self, assets: List[Dict[str, Any]], ord_rate: Decimal, st_rate: Decimal) -> List[Dict[str, Any]]:
        """
        Policy: Prioritize Short-Term Gains and Ordinary Income over LT Gains.
        """
        ranked = []
        for asset in assets:
            # Yield tax drag
            yield_drag = Decimal(str(asset.get('yield', 0))) * ord_rate
            # Capital gains drag (assumed turnover-based)
            turnover = Decimal(str(asset.get('turnover', 0)))
            cg_drag = turnover * st_rate
            
            total_drag = yield_drag + cg_drag
            
            ranked.append({
                "ticker": asset['ticker'],
                "type": asset.get('type', 'EQUITY'),
                "tax_drag_bps": int(total_drag * 10000),
                "ppli_priority": "CRITICAL" if total_drag > 0.04 else "HIGH" if total_drag > 0.02 else "STANDARD"
            })
            
        # Sort by drag descending
        ranked.sort(key=lambda x: x['tax_drag_bps'], reverse=True)
        
        logger.info(f"TAX_LOG: Ranked {len(ranked)} assets for PPLI shield.")
        return ranked
