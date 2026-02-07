# Documentation: `test_position_sizer.py`, `test_sharpe_calculator.py`, `test_alpha_calculator.py`

## Overview
These tests validate the core mathematical libraries used for portfolio performance, risk-adjusted returns, and trade execution sizing.

## Components Under Test
- `services.risk.position_sizer.PositionSizer`: Calculates lot sizes based on pip risk and account equity.
- `services.quantitative.sharpe_calculator.SharpeRatioCalculator`: Calculates risk-adjusted returns (Sharpe).
- `services.quantitative.alpha_calculator.AlphaCalculator`: Calculates Jensen's Alpha and simple alpha vs. benchmarks.

## Key Test Scenarios

### 1. Position Sizing Rules
- **Goal**: Verify the "1% risk" standard and currency-specific scaling.
- **Assertions**:
    - $100k account with 20 pip SL on EUR/USD correctly sizes to 5.0 lots.
    - USD/JPY scaling correctly handles different pip values.
    - System enforces a minimum 10-pip "Safety Stop" if a smaller one is requested.

### 2. Risk Metrics (Sharpe & Alpha)
- **Goal**: Verify the accuracy of institutional math.
- **Assertions**:
    - Sharpe Ratio correctly reflects 1.25 for a stable positive return stream.
    - Jensen's Alpha correctly identifies outperformance (0.8%) given a specific Beta and Risk-Free rate.
    - Handles edge cases like zero volatility (returns Sharpe 0.0) without crashing.

## Holistic Context
These calculators are the "precision optics" of the AI Investor. Even a small error in position sizing or alpha calculation could lead to unintended leverage or incorrect performance assessment.
