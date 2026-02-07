# Documentation: `tests/estate/test_snt_core.py`

## Overview
This test suite validates the logic for Special Needs Trusts (SNT). It ensures that distributions do not disqualify beneficiaries from government benefits (like SSI/Medicaid) by filtering prohibited expenses and monitoring asset limits.

## Services Under Test
- `services.estate.snt_filter.SNTDistributionFilter`
- `services.estate.resource_monitor.ResourceMonitor`

## Fixtures
- `snt_filter`: Instance of `SNTDistributionFilter`.
- `monitor`: Instance of `ResourceMonitor`.

## Test Scenarios

### 1. `test_snt_filter_allowed_vendor`
- **Goal**: Verify that medical/rehabilitation payments made directly to vendors are permitted.
- **Assertions**:
    - Status is `ALLOWED`.
    - Risk level is `LOW`.

### 2. `test_snt_filter_blocked_food`
- **Goal**: Verify that payments for food/groceries trigger a warning due to "In-Kind Support and Maintenance" (ISM) rules.
- **Assertions**:
    - Status is `WARNING`.
    - Risk level is `HIGH`.

### 3. `test_resource_monitor_risk`
- **Goal**: Verify that asset levels near the $2,000 SSI limit trigger warnings.
- **Assertions**:
    - An asset level of $1,900 is technically within limit but triggers a `WARNING` recommendation.

## Holistic Context
SNT compliance is extremely high-stakes; a single incorrect distribution can terminate a beneficiary's life-sustaining benefits. These tests provide the algorithmic safety net required to automate trust administrations safely.
