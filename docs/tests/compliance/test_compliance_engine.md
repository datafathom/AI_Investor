# Documentation: `tests/compliance/test_compliance_engine.py`

## Overview
This test suite provides comprehensive coverage for the core `ComplianceEngine`, which is responsible for evaluating transactions against a dynamic set of regulatory and internal rules.

## Service Under Test
- `services.compliance.compliance_engine.ComplianceEngine`

## Fixtures
- `service`: `ComplianceEngine` instance with a mocked cache service.
- `mock_transaction`: A standard trading transaction payload (AAPL buy).

## Test Scenarios

### 1. `test_check_compliance` (Async)
- **Goal**: Verify that a transaction passing all rules returns no violations.
- **Assertions**:
    - Result is an empty list when `_evaluate_rule` returns `False`.

### 2. `test_check_compliance_with_violation` (Async)
- **Goal**: Verify that failing a rule correctly generates a `ComplianceViolation` object.
- **Assertions**:
    - Result contains one violation when `_evaluate_rule` returns `True`.
    - The returned object is an instance of `ComplianceViolation`.

### 3. `test_get_violations` (Async)
- **Goal**: Verify the retrieval of existing violations from the persistent store.
- **Assertions**:
    - Result matches the mocked data returned from the database layer.

## Holistic Context
The `ComplianceEngine` is the final gatekeeper for all trades. These tests ensure the engine can both identify legitimate trades and catch prohibited ones, serving as the primary automated defense against compliance breaches.
