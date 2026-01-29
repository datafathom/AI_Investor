"""
Risk Constraint Gate.
Prevents trade execution if risk parameters are violated.
Acts as a hard gate before the broker executor.
"""
import logging
from decimal import Decimal
from typing import Dict, Any, Tuple

from config.risk_limits import RISK_CONFIG

logger = logging.getLogger(__name__)

class RiskConstraint:
    """
    Hard gate for institutional risk enforcement.
    """

    @staticmethod
    def validate_proposal(
        proposal: Dict[str, Any],
        account_equity: Decimal,
        daily_drawdown_pct: float = 0.0
    ) -> Tuple[bool, str]:
        """
        Validate a trade proposal against hard constraints.
        
        :param proposal: Dict containing 'lots', 'stop_loss_pips', 'risk_amount'
        :param account_equity: Current total account equity
        :param daily_drawdown_pct: Current daily drawdown % (0.0 to 1.0)
        :return: (is_valid, reason)
        """
        # 1. Check daily drawdown circuit breaker
        if daily_drawdown_pct >= RISK_CONFIG["MAX_DAILY_DRAWDOWN"]:
            return False, f"CIRCUIT_BREAKER: Daily drawdown {daily_drawdown_pct:.2%} exceeds limit."

        # 2. Check risk amount vs 1% rule
        risk_amount = Decimal(str(proposal.get("risk_amount", 0)))
        max_allowed_risk = account_equity * Decimal(str(RISK_CONFIG["REGIMES"]["NORMAL"]["max_risk_per_trade"]))
        
        if risk_amount > max_allowed_risk:
            return False, f"EXCESSIVE_RISK: Trade risks ${risk_amount:.2f} but max allowed is ${max_allowed_risk:.2f}."

        # 3. Prevent extremely tight stops (high leverage trap)
        sl_pips = proposal.get("stop_loss_pips", 0)
        if sl_pips < RISK_CONFIG["MIN_STOP_LOSS_PIPS"]:
            return False, f"INVALID_STOP: SL {sl_pips} pips is below institutional minimum of {RISK_CONFIG['MIN_STOP_LOSS_PIPS']}."

        return True, "VALIDATED"
