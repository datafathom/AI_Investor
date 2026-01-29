"""
Position Sizing Engine.
Calculates optimal lot sizes based on institutional risk rules.
Formula: (Balance * Risk%) / StopLossDistance
"""
import logging
from decimal import Decimal
from typing import Dict, Any, Optional

from config.risk_limits import RISK_CONFIG
from services.pip_calculator import PipCalculatorService

logger = logging.getLogger(__name__)

class PositionSizer:
    """
    Handles position sizing calculations with hard risk limits.
    """

    @staticmethod
    def calculate_size(
        balance: Decimal,
        stop_loss_pips: float,
        symbol: str,
        regime: str = "NORMAL",
        risk_override: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate the trade size in standard lots.
        
        :param balance: Current account equity
        :param stop_loss_pips: Distance from entry to stop in pips
        :param symbol: Asset symbol (e.g., 'EUR/USD')
        :param regime: Risk regime (NORMAL, CONSERVATIVE, ULTRA_SAFE)
        :param risk_override: Optional direct risk % (e.g., 0.01)
        :return: Dict containing units, lots, and risk_amount
        """
        # 1. Determine Risk Percentage
        max_risk = RISK_CONFIG["REGIMES"].get(regime, RISK_CONFIG["REGIMES"]["NORMAL"])["max_risk_per_trade"]
        
        # Enforce hard limit even on overrides
        risk_pct = Decimal(str(risk_override or max_risk))
        if risk_pct > Decimal(str(max_risk)):
            logger.warning(f"Risk override {risk_pct} exceeds regime max {max_risk}. Capping.")
            risk_pct = Decimal(str(max_risk))

        # 2. Calculate Risk Amount in Dollars
        risk_amount = balance * risk_pct

        # 3. Handle Stop Loss Minimums
        if stop_loss_pips < RISK_CONFIG["MIN_STOP_LOSS_PIPS"]:
            logger.warning(f"Stop loss {stop_loss_pips} below minimum. Adjusting to {RISK_CONFIG['MIN_STOP_LOSS_PIPS']}")
            stop_loss_pips = RISK_CONFIG["MIN_STOP_LOSS_PIPS"]

        # 4. Calculate Units per Pip
        # Standard Lot = 100,000 units
        # Pipeline: Unit Size = (Risk Amount) / (Stop Loss Pips * Pip Value)
        # Pip Value for 1 Standard Lot:
        # - Major FX (4th dec): $10.00
        # - JPY FX (2nd dec): ~$6.50 - $10.00 (depends on USD/JPY)
        # For simplicity in this primitive, we assume USD quote-based pip values
        
        pip_value_std_lot = Decimal("10.00") if not symbol.endswith("JPY") else Decimal("7.00") # Estimate for JPY

        # Units = Risk / (SL * PipValPerUnit)
        # Lots = Risk / (SL * PipValPerLot)
        
        lots = risk_amount / (Decimal(str(stop_loss_pips)) * pip_value_std_lot)
        lots = round(lots, 2) # Round to standard brokerage 0.01 increments

        return {
            "symbol": symbol,
            "balance": float(balance),
            "risk_pct": float(risk_pct),
            "risk_amount": float(risk_amount),
            "stop_loss_pips": stop_loss_pips,
            "lots": float(lots),
            "units": int(lots * 100000)
        }
