import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PortfolioSelector:
    """Determines whether to use a Model Portfolio or a Custom Allocation."""
    
    def determine_strategy(self, asset_level: float, risk_profile: str) -> str:
        """
        Logic: 
        - < $500k: Model Portfolio (Low tracking error, cost-efficient)
        - > $500k: Customized (Direct indexing, tax optimization, thematic)
        """
        if asset_level >= 500000:
            strategy = "CUSTOMIZED"
        else:
            strategy = "MODEL_PORTFOLIO"
            
        logger.info(f"PORTFOLIO_LOG: Strategy selected: {strategy} for level ${asset_level:,.2f}")
        return strategy
