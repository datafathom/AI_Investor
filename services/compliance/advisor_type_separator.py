import logging
from typing import List

logger = logging.getLogger(__name__)

class AdvisorTypeSeparator:
    """Categorizes advisors into specific sub-types based on service profile."""
    
    def determine_types(self, services: List[str], net_worth_min: float = 0) -> List[str]:
        types = []
        
        if "TAX" in services and "ESTATE" in services:
            types.append("WEALTH_MANAGER")
        
        if "INVESTMENTS" in services and "TRADING" in services:
            types.append("ASSET_MANAGER")
            
        if "BUDGETING" in services or "529" in services:
            types.append("FINANCIAL_PLANNER")
            
        if net_worth_min >= 10000000:
            types.append("PRIVATE_BANKER")
            
        if not types:
            types.append("GENERAL_ADVISOR")
            
        return types
