import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EducationExpenseVerifier:
    """Verifies if 529 plan distributions meet qualified education expense criteria."""
    
    QUALIFIED_CATEGORIES = {
        "TUITION", "ROOM_BOARD", "BOOKS", "SUPPLIES", 
        "COMPUTER", "INTERNET", "STUDENT_LOAN", "K12_TUITION"
    }

    def verify_expense(self, category: str, amount: float, student_status: str = "FULL_TIME") -> Dict[str, Any]:
        """
        Policy: 
        - Category must be in qualified list.
        - Room/Board requires at least half-time status.
        - Student loan is $10k lifetime limit (handled by ledger).
        """
        cat = category.upper()
        is_qualified = cat in self.QUALIFIED_CATEGORIES
        
        if cat == "ROOM_BOARD" and student_status not in ["FULL_TIME", "HALF_TIME"]:
            is_qualified = False
            reason = "Student MUST be at least half-time for Room & Board coverage."
        else:
            reason = "Standard Qualified Category" if is_qualified else "NON-QUALIFIED Category"
            
        if not is_qualified:
            logger.warning(f"COMPLIANCE_ALERT: Non-qualified 529 withdrawal attempt: {category} (${amount:,.2f})")
            
        return {
            "is_qualified": is_qualified,
            "category": cat,
            "verification_note": reason
        }
