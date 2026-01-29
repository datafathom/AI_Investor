import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PPLIEfficiencyService:
    """
    Optimizes asset placement for PPLI (Private Placement Life Insurance).
    Focuses on wrapping assets with the highest 'Tax Drag' to maximize alpha.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PPLIEfficiencyService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("PPLIEfficiencyService initialized")

    def rank_assets_by_tax_drag(self, assets: List[Dict[str, Any]], ord_rate: Decimal = Decimal('0.37'), st_rate: Decimal = Decimal('0.37')) -> List[Dict[str, Any]]:
        """
        Policy: Tax Drag = (Yield * OrdRate) + (ShortTermGains * STRate).
        Higher drag = higher priority for PPLI wrapper.
        """
        ranked = []
        for asset in assets:
            annual_yield = asset.get('yield', Decimal('0'))
            st_gains = asset.get('st_gains_pct', Decimal('0'))
            
            tax_drag = (annual_yield * ord_rate) + (st_gains * st_rate)
            ranked.append({**asset, "tax_drag": round(tax_drag, 4)})
            
        # Sort descending
        ranked.sort(key=lambda x: x['tax_drag'], reverse=True)
        
        logger.info(f"PPLI_LOG: Ranked {len(ranked)} assets for wrapping. High: {ranked[0]['symbol'] if ranked else 'None'}")
        return ranked
