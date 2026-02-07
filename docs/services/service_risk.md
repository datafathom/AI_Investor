# Backend Service: Risk (The Control Tower)

## Overview
The **Risk Service** is the largest and most critical service in the platform, with **45 specialized modules** designed to protect capital. It enforces hard limits on trading activity, monitors portfolio health in real-time, and automatically halts operations when thresholds are breached.

## Core Components (Selected)

### 1. Circuit Breaker (`circuit_breaker.py`)
The Emergency Brake.
- **Global Kill Switch**: Halts ALL trading immediately upon manual trigger.
- **Portfolio Freeze**: Automatically freezes trading if daily drawdown exceeds -3%.
- **Asset Kill Switch**: Halts trading on a specific asset if it drops >10% from its high.

### 2. Stress Testing Service (`stress_testing_service.py`)
- Simulates portfolio behavior under historical crash scenarios (2008, COVID, Black Monday).

### 3. Margin Service (`margin_service.py`)
- Calculates buying power and tracks margin usage to prevent forced liquidations.

### 4. Position Sizer (`position_sizer.py`)
- Implements Kelly Criterion and volatility-scaled position sizing.

### Other Key Modules
- `geopolitical_risk_svc.py`: Tracks exposure to politically unstable regions.
- `concentration_detector.py`: Flags when a single position dominates the portfolio.
- `liquidity_validator.py`: Ensures trades can be executed without excessive slippage.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Risk Dashboard** | Kill Switch Control | `circuit_breaker.is_halted()` | **Implemented** (`MissionControl.jsx`) |
| **Trade Ticket** | Position Sizer | `position_sizer.calculate_size()` | **Implemented** |
| **Stress Testing** | Scenario Analyzer | `stress_testing_service` | **Implemented** (`StressTest.jsx`) |

## Usage Example

```python
from services.risk.circuit_breaker import get_circuit_breaker

breaker = get_circuit_breaker()

# Check if trading is halted
if breaker.is_halted():
    print(f"Trading is HALTED. Reason: {breaker.freeze_reason}")
else:
    # Check daily P&L
    daily_pnl = -0.025 # -2.5%
    is_frozen = breaker.check_portfolio_freeze(daily_pnl)
    if not is_frozen:
        print("Trading is active.")

# Manual emergency halt
breaker.trigger_global_kill_switch("Flash crash detected manually.")
```
