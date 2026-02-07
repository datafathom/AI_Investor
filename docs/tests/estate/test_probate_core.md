# Documentation: `tests/estate/test_probate_core.py`

## Overview
This test suite focuses on the financial and legal mechanics of probate, primarily using California statutory guidelines. It verifies fee calculations and intestacy (succession) logic.

## Services Under Test
- `services.estate.probate_fee_calc.ProbateFeeCalculator`
- `services.legal.intestacy_logic.IntestacyLogic`

## Fixtures
- `fee_calc`: Instance of `ProbateFeeCalculator`.
- `intestacy`: Instance of `IntestacyLogic`.

## Test Scenarios

### 1. `test_probate_fee_calculation_ca`
- **Goal**: Verify that California statutory probate fees are computed correctly based on estate value.
- **Assertions**:
    - For a $1.5M estate, the attorney fee is $28,000.
    - Total statutory cost (attorney + executor) is $56,000.

### 2. `test_intestacy_logic_spouse_only`
- **Goal**: Verify succession when there is a spouse but no children or parents.
- **Assertions**:
    - 100% of the estate is distributed to the Spouse.

### 3. `test_intestacy_logic_spouse_and_child`
- **Goal**: Verify 50/50 split of separate property between a spouse and one child.
- **Assertions**:
    - Spouse receives $500k.
    - Child 1 receives $500k.

## Holistic Context
Probate is often the most expensive part of estate administration. These tests ensure the accuracy of "cost-of-death" projections, allowing users to see the immediate ROI of setting up a Living Trust to bypass these fees.
