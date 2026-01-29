"""
Precision Engine Service.
Handles price normalization and rounding across the system.
"""
import logging
from decimal import Decimal
from typing import Dict, Any, Union
from config.decimal_precision import get_precision_config
from utils.decimal_handler import to_decimal, quantize_decimal

logger = logging.getLogger(__name__)

class PrecisionEngine:
    """
    Service to ensure all pricing and order data conforms to asset-specific decimal standards.
    """

    @staticmethod
    def normalize_price(symbol: str, price: Union[float, str, Decimal]) -> Decimal:
        """
        Normalize a price to the correct decimal places for the symbol.
        """
        config = get_precision_config(symbol)
        dec_price = to_decimal(price)
        return quantize_decimal(dec_price, config['decimals'])

    @staticmethod
    def get_pip_value(symbol: str, price_diff: Union[float, Decimal]) -> Decimal:
        """
        Convert a raw price difference into pips with safe decimal math.
        """
        config = get_precision_config(symbol)
        dec_diff = to_decimal(price_diff)
        pip_size = Decimal(f"1e-{config['pip_position']}")
        
        # Round the result to 2 decimal places (standard for fractional pips)
        return quantize_decimal(dec_diff / pip_size, 2)

    @staticmethod
    def format_for_display(symbol: str, price: Union[float, Decimal]) -> str:
        """
        Format price as string for UI display with correct padding.
        """
        config = get_precision_config(symbol)
        normalized = PrecisionEngine.normalize_price(symbol, price)
        return f"{normalized:.{config['decimals']}f}"

    @staticmethod
    def check_lot_size(symbol: str, lots: float) -> Decimal:
        """
        Ensure lot size (position size) is rounded to standard FX increments (usually 0.01).
        """
        # Standard micro-lot is 0.01, mini is 0.1, standard is 1.0
        # We enforce 2 decimal places for lot sizing usually.
        return quantize_decimal(to_decimal(lots), 2)
