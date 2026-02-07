# Documentation: `tests/api/test_compliance_api.py`

## Overview
This test suite validates the REST interface for the compliance system. It ensures that external applications can trigger compliance checks and generate regulatory reports via the API layer.

## API Endpoints Under Test
- `POST /api/v1/compliance/check`: Run real-time compliance evaluation on a transaction.
- `POST /api/v1/compliance/report/generate`: Generate historical regulatory or internal reports.

## Fixtures
- `mock_compliance_engine`: Mocks the core evaluation logic.
- `mock_reporting_service`: Mocks the PDF/JSON report generation layer.

## Test Scenarios

### 1. `test_check_compliance_success`
- **Goal**: Verify successful return of violations through the API.
- **Assertions**: Returns 200 OK with the list of violations encapsulated in the `data` field.

### 2. `test_check_compliance_missing_params`
- **Goal**: Ensure the API enforces schema strictness.
- **Assertions**: Returns 422 Unprocessable Entity when the `transaction` payload is missing.

### 3. `test_generate_report_success`
- **Goal**: Verify report generation request fulfillment.
- **Assertions**: Returns 200 OK with a generated `report_id`.

## Holistic Context
This API allows the Sovereign OS to be audited by third parties or integrated into larger financial ecosystems. Robust testing here ensures that compliance results are delivered accurately to the client layer.
