# Documentation: `tests/unit/test_protector_agent.py`

## Overview
This test suite validates the "Protector Agent", a specialized autonomous entity dedicated to downside protection and system-wide emergency halts.

## Agent Under Test
- `agents.protector_agent.ProtectorAgent`

## Key Safety Mechanisms Tested

### 1. Global Kill Switch
- **Goal**: Verify that a manual emergency signal stops all activity.
- **Assertions**: Presence of `STOP_ALL_TRADING=TRUE` in environment triggers a `HALT_ALL` response.

### 2. VIX Spike (Bunker Mode)
- **Goal**: Protect the portfolio during extreme market turbulence.
- **Assertions**: VIX level > 30 triggers `ENTER_BUNKER_MODE`.

### 3. Max Drawdown Halt
- **Goal**: Enforce hard risk limits on total capital loss.
- **Assertions**: A drawdown exceeding the 2% threshold (e.g., 3%) triggers `MAX_DRAWDOWN_HALT`, providing the calculated drawdown percentage in the result.

## Holistic Context
The Protector Agent is the ultimate "safety valve". These tests are critical because they cover the logic that prevents catastrophic financial loss during market anomalies or systemic failures.
