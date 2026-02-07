# Backend Service: Indicators

## Overview
The **Indicators Service** provides the platform's technical analysis and signal generation layer. It specializes in volatility-based metrics that help traders and automated agents determine historical and current market ranges. Its primary tool is the **ATR (Average True Range) Calculator**, which is essential for placing "Noise-Resistant" stop-loss orders in volatile markets.

## Core Components

### 1. ATR Calculator (`atr_calc.py`)
A quantitative utility for measurement of price volatility.
- **Average True Range Logic**: Computes the ATR over a configurable period (default: 14) by analyzing the range between high, low, and previous close for each candle. 
- **Volatility-Adjusted Stop Padding**: Provides a precision tool for risk management. Instead of using arbitrary percentages, it calculates stop-loss levels based on market volatility (e.g., placing a stop 1.5x ATR away from a swing high or low). This ensures that trades are not "stopped out" by normal intraday price fluctuations.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Technical Indicators Chart | `atr_calc.calculate_atr()` |
| **Trading Terminal** | "Padded Stop" Assistant | `atr_calc.get_padded_stop()` |
| **Risk Station** | Volatility Heatmap | `atr_calc.calculate_atr()` |
| **Order Ticket** | Smart Stop Level Slider | `atr_calc.get_padded_stop()` |

## Dependencies
- `decimal`: Used for precision financial calculations within the stop-padding logic.
- `logging`: Records the calculation of significant volatility shifts.

## Usage Examples

### Calculating ATR for Stop-Loss Placement
```python
from services.indicators.atr_calc import ATRCalculator

calc = ATRCalculator()

# Mock 14-period candle data
candles = [
    {"high": 105, "low": 95, "close": 100},
    {"high": 110, "low": 102, "close": 108},
    # ... (12 more candles)
]

atr = calc.calculate_atr(candles=candles, period=14)

# Place a Long stop 1.5x ATR below a swing low of $102
stop_price = calc.get_padded_stop(
    swing_level=102.0,
    atr=atr,
    direction="LONG",
    padding_mult=1.5
)

print(f"Current ATR: {atr:.4f}")
print(f"Volatility-Adjusted Stop Price: ${stop_price}")
```

### Dynamic Risk Padding for Short Positions
```python
from services.indicators.atr_calc import ATRCalculator

atr = 2.45 # Current volatility measure
swing_high = 450.50

# Place a Short stop 2.0x ATR ABOVE the swing high
padded_stop = ATRCalculator.get_padded_stop(
    swing_level=swing_high,
    atr=atr,
    direction="SHORT",
    padding_mult=2.0
)

print(f"Padded Short Stop: ${padded_stop}")
```
