import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class PhilanthropyService:
    """
    Phase 195.1: Strategic Philanthropy Logic.
    Manages charitable contributions and social impact scoring.
    """
    
    def calculate_charitable_deduction(self, amount: Decimal, agi: Decimal, asset_type: str) -> Dict[str, Any]:
        """
        Phase 195.3: Donor Advised Fund Gate.
        Calculates tax limits for DAF/Charitable contributions.
        """
        # IRS Limits: 60% AGI for cash, 30% for appreciated assets
        limit_pct = Decimal("0.60") if asset_type.upper() == "CASH" else Decimal("0.30")
        max_deduction = agi * limit_pct
        
        deductible_amount = min(amount, max_deduction)
        carryover = max(Decimal("0"), amount - max_deduction)
        
        logger.info(f"PHILANTHROPY_LOG: Deduction for {amount} ({asset_type}): {deductible_amount}. Carryover: {carryover}")
        
        return {
            "amount_contributed": amount,
            "max_agi_limit": max_deduction,
            "deductible_this_year": deductible_amount,
            "carryover_amount": carryover,
            "limit_reached": deductible_amount == max_deduction
        }

    def score_social_impact(self, donations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Phase 195.2: Impact Calculator.
        Scores 'Charitable Alpha' based on donation efficacy.
        """
        total_donated = sum(d["amount"] for d in donations)
        # Mock efficacy score
        avg_efficacy = sum(d.get("efficacy", 0.8) for d in donations) / len(donations) if donations else 0.0
        
        social_id_score = total_donated * Decimal(str(avg_efficacy)) / Decimal("100000") # Normalized
        social_id_score = min(float(social_id_score), 100.0)
        
        logger.info(f"PHILANTHROPY_LOG: Social ID Score: {social_id_score:.2f}")
        
        return {
            "total_donated": float(total_donated),
            "social_id_score": round(social_id_score, 2),
            "tier": "PHILANTHROPIST" if social_id_score > 50 else "CONTRIBUTOR"
        }
