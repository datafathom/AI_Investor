import logging
from typing import Dict, Any, List
from decimal import Decimal

logger = logging.getLogger(__name__)

class RateExposureAnalyzer:
    """
    Phase 171.5: Floating Rate vs. Fixed Rate Exposure Analyzer.
    Analyzes portfolio sensitivity to interest rate changes (SOFR/Libor).
    """
    
    def analyze_sensitivity(self, portfolio: List[Dict[str, Any]], rate_shift_bps: int) -> Dict[str, Any]:
        """
        Calculates annual interest income change for a given basis point shift.
        """
        shift_decimal = Decimal(str(rate_shift_bps)) / Decimal('10000')
        total_income_delta = Decimal('0')
        
        for loan in portfolio:
            if loan.get("is_floating", False):
                delta = Decimal(str(loan["principal"])) * shift_decimal
                total_income_delta += delta
                
        logger.info(f"ANALYSIS_LOG: Interest Rate Shift ({rate_shift_bps}bps) results in ${total_income_delta:,.2f} income delta.")
        
        return {
            "shift_bps": rate_shift_bps,
            "annual_income_impact": round(float(total_income_delta), 2),
            "sensitivity": "POSITIVE" if total_income_delta > 0 else "NEUTRAL/NEGATIVE"
        }
