import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class QualityTiltService:
    """
    Filters and scores assets based on 'Quality' factors.
    Used during Bear Markets to shift allocaton to durable companies.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QualityTiltService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("QualityTiltService initialized")

    def filter_for_quality(self, assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Selects assets with High ROE and Low Leverage.
        Criteria:
        - Return on Equity (ROE) > 15%
        - Debt-to-Equity < 0.5
        """
        quality_assets = []
        
        for asset in assets:
            roe = asset.get('roe', 0)
            debt_to_equity = asset.get('debt_to_equity', 99) # Default to high debt if unknown
            
            if roe > 0.15 and debt_to_equity < 0.5:
                asset['quality_score'] = 'HIGH'
                quality_assets.append(asset)
            else:
                asset['quality_score'] = 'LOW'
                
        logger.info(f"Quality Tilt: Filtered {len(assets)} assets down to {len(quality_assets)} quality picks.")
        return quality_assets
