
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class IntestacyLogic:
    """
    Maps 'Who gets what' when a person dies without a trust or will.
    """
    
    def map_succession(
        self, 
        has_spouse: bool, 
        child_count: int, 
        has_parents: bool,
        community_property_value: float,
        separate_property_value: float
    ) -> Dict[str, Any]:
        """
        Simplified Intestacy Successor Map (California Heuristic).
        """
        logger.info(f"Mapping Intestacy: Spouse={has_spouse}, Kids={child_count}")
        
        distributions = []
        
        # 1. Community Property
        if has_spouse:
            distributions.append({
                "party": "Spouse", 
                "type": "Community Property", 
                "portion": "100%", 
                "value": community_property_value
            })
        else:
            distributions.append({
                "party": "Children", 
                "type": "Community Property", 
                "portion": "100%", 
                "value": community_property_value
            })
            
        # 2. Separate Property
        if has_spouse:
            if child_count == 0:
                if has_parents:
                    distributions.append({"party": "Spouse", "type": "Separate", "portion": "50%", "value": separate_property_value * 0.5})
                    distributions.append({"party": "Parents", "type": "Separate", "portion": "50%", "value": separate_property_value * 0.5})
                else:
                    distributions.append({"party": "Spouse", "type": "Separate", "portion": "100%", "value": separate_property_value})
            elif child_count == 1:
                distributions.append({"party": "Spouse", "type": "Separate", "portion": "50%", "value": separate_property_value * 0.5})
                distributions.append({"party": "Child 1", "type": "Separate", "portion": "50%", "value": separate_property_value * 0.5})
            else:
                distributions.append({"party": "Spouse", "type": "Separate", "portion": "33.3%", "value": separate_property_value * 0.333})
                distributions.append({"party": "Children", "type": "Separate", "portion": "66.6%", "value": separate_property_value * 0.666})
        else:
            distributions.append({"party": "Children", "type": "Separate", "portion": "100%", "value": separate_property_value})

        return {
            "distributions": distributions,
            "risk_warning": "Intestacy often leads to unintended heirs receiving assets."
        }
