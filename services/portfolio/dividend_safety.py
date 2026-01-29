import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DividendSafetyService:
    """
    dentifies 'Dividend Aristocrats' - companies with consistent dividend growth.
    Crucial for 'Keep the Lights On' income overlay during bear markets.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DividendSafetyService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("DividendSafetyService initialized")

    def filter_aristocrats(self, assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters for stocks with > 25 years of dividend growth.
        """
        aristocrats = []
        
        for asset in assets:
            years_growing = asset.get('dividend_growth_years', 0)
            yield_pct = asset.get('dividend_yield', 0.0)
            
            # Simple Aristocrat Definition
            if years_growing >= 25 and yield_pct > 0.02:
                aristocrats.append(asset)
                
        logger.info(f"Dividend Safety: Found {len(aristocrats)} Aristocrats out of {len(assets)} candidates.")
        return aristocrats
