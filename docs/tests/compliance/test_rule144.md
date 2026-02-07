# Documentation: `tests/compliance/test_rule144.py`

## Overview
This test suite verifies the functionality of the `InsiderTradingService`, specifically focusing on SEC Rule 144 compliance. It ensures that the system correctly calculates sellable volumes for insiders and validates trade compliance against lock-up periods and volume limits.

## Service Under Test
- `services.compliance.insider_trading_svc.InsiderTradingService`

## Fixtures
- `svc`: Initializes a fresh instance of the `InsiderTradingService`.

## Test Scenarios

### 1. `test_calculate_sellable_volume`
- **Goal**: Verify that the maximum sellable volume is calculated correctly based on the greater of 1% of outstanding shares or the average weekly trading volume.
- **Assertions**:
    - When 1% of shares (100k) > avg volume (50k), limit is 100k.
    - When avg volume (150k) > 1% of shares (100k), limit is 150k.

### 2. `test_check_lockup_status`
- **Goal**: Ensure the service correctly identifies whether a security is currently within a lock-up period.
- **Assertions**:
    - A future expiry date returns `is_locked=True` and `can_sell=False`.
    - A past expiry date returns `is_locked=False` and `can_sell=True`.

### 3. `test_validate_sale_compliance`
- **Goal**: Perform an end-to-end validation of a proposed sale against all Rule 144 constraints.
- **Assertions**:
    - A sale within volume limits and outside lock-up is `compliant`.
    - A sale during a lock-up period is rejected.
    - A sale exceeding calculated volume limits is rejected.

## Holistic Context
Rule 144 is a cornerstone of SEC compliance for restricted and controlled securities. These tests prevent illegal insider sales, protecting the firm from severe regulatory penalties and reputational damage.
