# Documentation: `tests/unit/test_stop_loss_logic.py`

## Overview
This test suite covers the "Sentinel" and "Removal Blocker" logic. It is a critical safety layer that prevents both the AI and manual users from removing risk protections once a trade is live.

## Components Under Test
- `services.risk.stop_loss_sentinel.StopLossSentinel`: Real-time price monitoring vs. SL.
- `services.risk.sl_removal_blocker.SLRemovalBlocker`: Guardrail against removing or loosening stop losses.

## Key Test Scenarios

### 1. Sentinel Execution
- **Goal**: Ensure the sentinel detects the moment a price touches or exceeds a stop loss.
- **Assertions**: 
    - Correctly triggers `True` when price hits the SL for both LONG and SHORT positions.
    - Remains `False` while price is favorable.

### 2. Removal & Loosening Blockers
- **Goal**: Prevent "Loss Aversion" psychology (moving SL further away when losing).
- **Assertions**:
    - **FORBIDDEN**: Attempting to remove a stop loss (setting to `None`) is rejected.
    - **ILLEGAL_MOVE**: Moving a stop loss further away (e.g., $1.0800 to $1.0750 on a LONG) is blocked.
    - **LEGAL_TIGHTEN**: Moving a stop loss closer to the current price (reducing risk) is allowed.

## Holistic Context
These tests enforce the system's "Discipline". By making it programmaticly impossible to loosen a stop loss, the Sovereign OS eliminates the "Just one more pip" bias that often professionalizes human traders into significant losses.
