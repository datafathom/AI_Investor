
import logging
from datetime import date, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CrummeyGenerator:
    """
    Generates Crummey Power notices for ILIT beneficiaries.
    Required for the 'Present Interest' gift tax exclusion.
    """
    
    def generate_notice(self, beneficiary_name: str, gift_amount: float) -> Dict[str, Any]:
        """
        Creates the notice metadata and text.
        """
        sent_date = date.today()
        deadline = sent_date + timedelta(days=30)
        
        text = f"Dear {beneficiary_name}, This is to notify you that a gift of ${gift_amount} has been made to the ILIT. You have a 30-day right to withdraw your pro-rata share, expiring on {deadline}."
        
        logger.info(f"Crummey Notice: Generated for {beneficiary_name}, Amount=${gift_amount}")
        
        return {
            "beneficiary": beneficiary_name,
            "gift_amount": gift_amount,
            "notice_text": text,
            "withdrawal_deadline": deadline.isoformat(),
            "status": "SENT"
        }
