# Institutional Position Sizing Standards

This document defines the mathematical models used by the AI_Investor platform to calculate and enforce risk management.

## 1. The Core Formula (1% Rule)

All trades must limit total financial risk to **1% (0.01)** of the current account equity.

$$RiskAmount = Equity \times 0.01$$

The position size (in standard lots) is derived from the stop loss distance:

$$Lots = \frac{RiskAmount}{StopLossPips \times PipValuePerLot}$$

### Variable Definitions:
- **Equity**: Total account balance adjusted for floating PnL.
- **StopLossPips**: The distance from entry to the hard stop loss.
- **PipValuePerLot**: 
  - For Major USD pairs (e.g. EUR/USD): **$10.00**
  - For JPY pairs: Variable, typically **$6.50 - $10.00** depending on the USD/JPY rate.

---

## 2. Risk Regimes

The system dynamically adjusts the `MaxRisk` parameter based on market volatility:

| Regime | Max Risk % | Trigger Condition |
| :--- | :--- | :--- |
| **Normal** | 1.0% | Standard Volatility |
| **Conservative** | 0.5% | VIX > 25 or News Embargo |
| **Ultra-Safe** | 0.25% | Circuit Breaker Active / Equity Recovery |

---

## 3. Numeric Precision

To prevent floating-point drift:
1. All inputs are converted to `Decimal` types.
2. Final lot sizes are rounded to the nearest **0.01 (Micro-lot)**.
3. Stop Loss distances are floor-capped at **10.0 pips** to prevent over-leveraged high-frequency 'scalping' traps.
