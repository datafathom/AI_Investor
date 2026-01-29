
import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SolvencyValidator:
    """
    Validates that a transfer into an APT is not a fraudulent conveyance.
    Ensures the grantor remains solvent after the transfer.
    """
    
    def validate_solvency(
        self,
        transfer_amount: Decimal,
        remaining_net_worth: Decimal,
        existing_liabilities: Decimal,
        known_lawsuits: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates solvency ratio and lawsuit risk.
        """
        solvency_ratio = remaining_net_worth / existing_liabilities if existing_liabilities > 0 else Decimal('100.0')
        
        is_fraudulent_risk = known_lawsuits or (solvency_ratio < Decimal('1.2'))
        
        logger.info(f"Solvency Check: Transfer=${transfer_amount}, Ratio={solvency_ratio}, FraudRisk={is_fraudulent_risk}")
        
        return {
            "is_solvent": not is_fraudulent_risk,
            "solvency_ratio": float(solvency_ratio),
            "fraud_risk_detected": is_fraudulent_risk,
            "affidavit_qualified": not is_fraudulent_risk,
            "status": "APPROVED" if not is_fraudulent_risk else "REJECTED_POTENTIAL_FRAUD"
        }
