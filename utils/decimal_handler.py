"""
Utility functions for high-precision decimal arithmetic.
"""
from decimal import Decimal, ROUND_HALF_UP, getcontext

# Set global precision safe for financial calculations
getcontext().prec = 28

def to_decimal(value: float | str | Decimal) -> Decimal:
    """
    Convert a value to a Decimal with safe type handling.
    
    Args:
        value: Input value (float, string, or Decimal)
        
    Returns:
        Decimal representation
    """
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))

def decimal_add(a: Decimal, b: Decimal) -> Decimal:
    """Safe addition."""
    return a + b

def decimal_sub(a: Decimal, b: Decimal) -> Decimal:
    """Safe subtraction."""
    return a - b

def decimal_div(a: Decimal, b: Decimal) -> Decimal:
    """Safe division."""
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def quantize_decimal(value: Decimal, places: int) -> Decimal:
    """
    Quantize a Decimal to specific number of places.
    
    Args:
        value: Decimal to quantize
        places: Number of decimal places (e.g., 4)
        
    Returns:
        Quantized Decimal
    """
    exponent = Decimal(f"1e-{places}")
    return value.quantize(exponent, rounding=ROUND_HALF_UP)

def safe_round_to_step(value: Decimal, step: Decimal) -> Decimal:
    """
    Round a value to the nearest multiple of a step.
    Useful for lot sizes (e.g., step=0.01).
    """
    if step == 0:
        return value
    return (value / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * step
