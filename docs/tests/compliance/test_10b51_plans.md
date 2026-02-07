# Documentation: `tests/compliance/test_10b51_plans.py`

## Overview
This test suite validates the lifecycle of 10b5-1 selling plans, which allow major shareholders to sell stock at predetermined times to avoid insider trading allegations. It covers plan creation, revision validation, and fiduciary execution.

## Services Under Test
- `services.compliance.selling_plan_service.SellingPlanService`
- `services.compliance.fiduciary_execution_layer.FiduciaryExecutionLayer`

## Fixtures
- `plan_svc`: Instance of `SellingPlanService`.
- `fid_layer`: Instance of `FiduciaryExecutionLayer`.

## Test Scenarios

### 1. `test_create_selling_plan`
- **Goal**: Verify that a 10b5-1 plan can be initialized with a specific schedule and parameters.
- **Assertions**:
    - User ID and ticker match input.
    - Schedule length matches the provided dates.
    - Shares per execution interval are correctly calculated.

### 2. `test_validate_plan_revision`
- **Goal**: Enforce restrictions on when a 10b5-1 plan can be modified.
- **Assertions**:
    - Revisions are blocked during blackout periods.
    - Revisions are blocked if the user possesses Material Non-Public Information (MNPI).
    - Standard revisions are allowed when neither condition is met.

### 3. `test_fiduciary_execution`
- **Goal**: Verify that the fiduciary layer can execute trades on behalf of the plan and log justifications.
- **Assertions**:
    - Execution returns the correct number of shares.
    - Fiduciary attestation is included in the result.
    - Non-timing justifications are successfully logged.

## Holistic Context
10b5-1 plans provide an "affirmative defense" against insider trading. High-fidelity testing of these plans ensures executive transactions remain legally sound and automated without manual interference that could void the defense.
