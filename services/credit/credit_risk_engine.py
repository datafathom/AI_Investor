import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CreditRiskEngine:
    """
    Mathematical engine for Private Credit (Direct Lending).
    Calculates expected net yield after defaults and recoveries.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CreditRiskEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("CreditRiskEngine initialized")

    def calculate_expected_net_yield(
        self, 
        gross_spread_bps: int, 
        base_rate: Decimal,
        default_prob_annual: Decimal, 
        recovery_rate: Decimal
    ) -> Dict[str, Any]:
        """
        Policy: Net Yield = Gross Yield - Expected Loss.
        Expected Loss = Default Probability * (1 - Recovery Rate).
        """
        gross_yield = base_rate + (Decimal(str(gross_spread_bps)) / Decimal('10000'))
        
        loss_given_default = Decimal('1') - recovery_rate
        expected_loss = default_prob_annual * loss_given_default
        
        net_yield = gross_yield - expected_loss
        
        logger.info(f"CREDIT_LOG: Gross {gross_yield:.2%} -> Net {net_yield:.2%} (Exp Loss: {expected_loss:.2%})")
        
        return {
            "gross_yield_pct": round(Decimal(str(gross_yield * 100)), 2),
            "expected_loss_pct": round(Decimal(str(expected_loss * 100)), 2),
            "net_yield_pct": round(Decimal(str(net_yield * 100)), 2),
            "risk_status": "STABLE" if expected_loss < Decimal('0.02') else "WATCHLIST"
        }
