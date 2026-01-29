import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GlobalRiskAggregator:
    """
    Aggregates financial exposure by country and currency.
    Provides data for the Geopolitical Risk Map.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GlobalRiskAggregator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("GlobalRiskAggregator initialized")

    def aggregate_geo_exposure(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Policy: Map positions to sovereign risk buckets.
        """
        exposure_map = {}
        for pos in positions:
            country = pos.get('country_code', 'US')
            value = pos.get('market_value', Decimal('0'))
            exposure_map[country] = exposure_map.get(country, Decimal('0')) + value
            
        logger.info(f"RISK_LOG: Aggregated geopolitical exposure for {len(exposure_map)} nations.")
        return {
            "sovereign_exposure": {k: round(v, 2) for k, v in exposure_map.items()},
            "concentrated_risk_flag": any(v > Decimal('5000000') for v in exposure_map.values())
        }
