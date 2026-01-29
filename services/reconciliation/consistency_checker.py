"""
Consistency Checker.
Compares internal ledger state with the demo broker API.
"""
import logging
from decimal import Decimal
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class ConsistencyChecker:
    """
    Validates that the system's balance matches the source of truth.
    """

    @staticmethod
    def verify_ledger(internal_balance: Decimal, broker_balance: Decimal) -> Tuple[bool, Decimal]:
        """
        Check if drift exists.
        :return: (is_consistent, drift_amount)
        """
        drift = internal_balance - broker_balance
        is_consistent = abs(drift) < Decimal("0.01") # Tolerance for precision
        
        if not is_consistent:
            logger.error(f"RECONCILIATION_FAILURE: Drift of ${drift:,.2f} detected!")
            
        return is_consistent, drift

    @staticmethod
    def log_reconciliation(is_success: bool, drift: Decimal):
        """
        Audit the results of the check.
        """
        status = "PASSED" if is_success else "FAILED"
        print(f"[{status}] Reconciliation check completed. Drift: ${drift:,.2f}")
