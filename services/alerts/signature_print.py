"""
Signature Print Alert.
Alerts on out-of-sequence or late prints signaling intent.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SignaturePrintAlert:
    """Detects 'Signature' prints."""
    
    def check_print(self, print_id: str, sequence_code: str) -> bool:
        """Alert if code is 'Z' (Out of Sequence) or similar."""
        if sequence_code in ["Z", "T"]:
             logger.warning(f"SIGNATURE_PRINT: Detect late print {print_id}")
             return True
        return False
