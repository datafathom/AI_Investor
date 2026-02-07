# Documentation: `tests/estate/test_estate_planning_service.py`

## Overview
This test suite covers the high-level `EstatePlanningService`, which manages the creation of estate plans and the calculation of potential estate tax liabilities.

## Service Under Test
- `services.estate.estate_planning_service.EstatePlanningService`

## Fixtures
- `service`: `EstatePlanningService` instance with mocked portfolio and cache dependencies.

## Test Scenarios

### 1. `test_create_estate_plan` (Async)
- **Goal**: Verify the end-to-end creation of an estate plan with multiple beneficiaries.
- **Assertions**:
    - Result is a valid `EstatePlan` object.
    - Beneficiary count matches input.

### 2. `test_calculate_estate_tax` (Async)
- **Goal**: Verify that estate tax estimates are correctly calculated for high-net-worth values.
- **Assertions**:
    - An estate value of $15M (above current federal exemption) results in a positive tax value.

## Holistic Context
The `EstatePlanningService` is the primary interface for users to define their legacy. These tests ensure the structural integrity of the plans created and the accuracy of the tax optimization advice provided by the system.
