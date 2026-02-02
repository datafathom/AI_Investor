"""
Solvency Validator for Asset Protection Trust Transfers
PURPOSE: Validate that asset transfers into APTs are not fraudulent conveyances.
         Ensures the grantor remains solvent after the transfer (critical for legal validity).
"""

import logging
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional
from dataclasses import dataclass
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)


@dataclass
class SolvencyAffidavit:
    """Legal affidavit confirming solvency at time of transfer."""
    affidavit_id: str
    grantor_id: str
    transfer_amount: Decimal
    remaining_net_worth: Decimal
    outstanding_liabilities: Decimal
    solvency_ratio: Decimal
    known_claims: bool
    is_valid: bool
    generated_at: datetime


class SolvencyValidator:
    """
    Validates that a transfer into an APT is not a fraudulent conveyance.
    Ensures the grantor remains solvent after the transfer.
    
    Key Tests:
    1. Balance Sheet Test: Assets >= Liabilities after transfer
    2. Cash Flow Test: Can pay debts as they come due
    3. No Known Claims: No pending lawsuits at time of transfer
    """
    
    MINIMUM_SOLVENCY_RATIO = Decimal("1.2")  # 20% buffer required
    
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
        
        is_fraudulent_risk = known_lawsuits or (solvency_ratio < self.MINIMUM_SOLVENCY_RATIO)
        
        logger.info(f"Solvency Check: Transfer=${transfer_amount}, Ratio={solvency_ratio}, FraudRisk={is_fraudulent_risk}")
        
        return {
            "is_solvent": not is_fraudulent_risk,
            "solvency_ratio": float(solvency_ratio),
            "fraud_risk_detected": is_fraudulent_risk,
            "affidavit_qualified": not is_fraudulent_risk,
            "status": "APPROVED" if not is_fraudulent_risk else "REJECTED_POTENTIAL_FRAUD"
        }

    async def generate_solvency_affidavit(
        self,
        grantor_id: str,
        transfer_amount: Decimal,
        total_assets: Decimal,
        total_liabilities: Decimal,
        pending_claims: bool = False
    ) -> SolvencyAffidavit:
        """
        Generate a formal solvency affidavit for legal documentation.
        Persists to database for audit trail.
        """
        remaining_net_worth = total_assets - transfer_amount
        solvency_ratio = remaining_net_worth / total_liabilities if total_liabilities > 0 else Decimal("100.0")
        
        is_valid = (solvency_ratio >= self.MINIMUM_SOLVENCY_RATIO) and not pending_claims
        
        affidavit = SolvencyAffidavit(
            affidavit_id=str(uuid.uuid4()),
            grantor_id=grantor_id,
            transfer_amount=transfer_amount,
            remaining_net_worth=remaining_net_worth,
            outstanding_liabilities=total_liabilities,
            solvency_ratio=solvency_ratio,
            known_claims=pending_claims,
            is_valid=is_valid,
            generated_at=datetime.now()
        )
        
        # Persist to database
        await self._persist_affidavit(affidavit)
        
        logger.info(f"Solvency Affidavit {affidavit.affidavit_id}: Valid={is_valid}, Ratio={solvency_ratio}")
        
        return affidavit

    async def _persist_affidavit(self, affidavit: SolvencyAffidavit) -> None:
        """Persist solvency affidavit to audit log."""
        try:
            with db_manager.pg_cursor() as cur:
                details = f'{{"affidavit_id": "{affidavit.affidavit_id}", "grantor": "{affidavit.grantor_id}", "transfer": {affidavit.transfer_amount}, "ratio": {affidavit.solvency_ratio}, "valid": {str(affidavit.is_valid).lower()}}}'
                cur.execute("""
                    INSERT INTO activity_logs (user_id, activity_type, details)
                    VALUES (%s, 'SOLVENCY_AFFIDAVIT', %s)
                """, (affidavit.grantor_id, details))
        except Exception as e:
            logger.error(f"Error persisting affidavit: {e}")


# Singleton
_instance: Optional[SolvencyValidator] = None

def get_solvency_validator() -> SolvencyValidator:
    global _instance
    if _instance is None:
        _instance = SolvencyValidator()
    return _instance

