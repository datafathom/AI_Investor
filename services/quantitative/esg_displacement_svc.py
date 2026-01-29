import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ESGDisplacementService:
    """
    Identifies valuation distortions caused by institutional ESG mandates.
    Scans for 'Sin' stocks trading at deep discounts (High FCF, Low P/E) due to forced selling.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ESGDisplacementService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("ESGDisplacementService initialized")

    def scan_for_sin_stock_alpha(self, assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Policy: Identify 'Unloved' alpha.
        Logic: P/E < 10 AND FCF Yield > 10% AND Sector IN ('ENERGY', 'TOBACCO', 'DEFENSE').
        """
        opportunites = []
        sin_sectors = {'ENERGY', 'TOBACCO', 'DEFENSE'}
        
        for asset in assets:
            sector = asset.get('sector', '').upper()
            pe = asset.get('pe_ratio', Decimal('99'))
            fcf_yield = asset.get('fcf_yield', Decimal('0'))
            
            if sector in sin_sectors and pe < Decimal('10') and fcf_yield > Decimal('0.10'):
                drag_score = 1 - float(pe / 10) # Higher discount = higher alpha
                opportunites.append({**asset, "esg_discount_alpha_score": round(drag_score, 2)})
                
        # Sort by alpha score
        opportunites.sort(key=lambda x: x['esg_discount_alpha_score'], reverse=True)
        
        logger.info(f"ESG_LOG: Identified {len(opportunites)} displacement opportunities in Sin sectors.")
        return opportunites
