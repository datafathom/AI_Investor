import logging
from typing import Dict, Any, List
from decimal import Decimal

logger = logging.getLogger(__name__)

class EventROITracker:
    """
    Phase 179.5: Event & Conference ROI Tracker.
    Measures value (contacts, deals) generated vs attendance cost.
    """
    
    def calculate_event_roi(
        self,
        event_name: str,
        cost: Decimal,
        contacts_gained: int,
        deals_sourced: int,
        total_deal_value: Decimal = Decimal('0')
    ) -> Dict[str, Any]:
        """
        Policy: Hard ROI = (Deal Value / Cost), Soft ROI = (Contacts / Cost).
        """
        hard_roi = (total_deal_value / cost) if cost > 0 else Decimal('0')
        cost_per_contact = cost / Decimal(str(contacts_gained)) if contacts_gained > 0 else cost
        
        logger.info(f"ANALYSIS_LOG: Event {event_name} ROI analyzed. Hard ROI: {hard_roi}x")
        
        return {
            "event": event_name,
            "hard_roi_multiplier": round(float(hard_roi), 2),
            "cost_per_contact": round(float(cost_per_contact), 2),
            "contacts_weight": contacts_gained * 10, # Heuristic
            "status": "ACCRETIVE" if hard_roi > 1 else "RELATIONSHIP_BUILDING"
        }
