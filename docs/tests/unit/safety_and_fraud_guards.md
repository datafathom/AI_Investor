# Documentation: `test_asset_kill_switch.py` & `test_anti_madoff_guard.py`

## Overview
These tests validate the "Critical Safety" layer of the AI Investor, specifically automated liquidation triggers and fraud detection patterns.

## Components Under Test
- `services.risk.asset_kill_switch.AssetKillSwitch`: Automated emergency fund protection.
- `services.fraud.anti_madoff_guard.AntiMadoffGuard`: Fraud and ponzi-scheme pattern detection.

## Key Test Scenarios

### 1. Asset Kill Switch (10% Drawdown)
- **Goal**: Protect capital from free-falling assets.
- **Assertions**: 
    - `ThresholdMonitor` correctly identifies 5% and 10% drawdowns for both LONG and SHORT positions (accounting for inverse math).
    - `AssetKillSwitch` correctly identifies and flags EUR/USD for liquidation when it crosses the 11% loss mark, while leaving stable positions untouched.

### 2. Fraud Detection (Anti-Madoff)
- **Goal**: Identify "too-good-to-be-true" return patterns.
- **Assertions**:
    - `detect_return_striation` correctly flags a string of identical positive monthly returns (e.g., exactly 0.8% every month) as a likely fraud signal.
    - `validate_statement_source` prevents spoofing by checking that the reported broker (e.g., SCHWAB) matches the known data source.

## Holistic Context
These guardrails are what make the AI Investor "Sovereign". It doesn't just trade; it actively defends the user's capital against both market crashes and predatory external actors by applying strict statistical and identity audits to every data point.
