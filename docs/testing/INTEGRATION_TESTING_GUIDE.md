# Integration Testing Guide

## Overview

This guide covers integration testing for the AI Investor platform, focusing on testing complete workflows and component interactions.

## Test Structure

Integration tests are located in `tests/integration/` and cover:

1. **Legal Document Acceptance Flow** (`test_legal_acceptance_flow.py`)
   - Document listing
   - Document retrieval
   - User acceptance tracking
   - Acceptance history
   - Document update checking

2. **User Onboarding Flow** (`test_onboarding_flow.py`)
   - Onboarding status
   - Step progression
   - Preference management
   - Completion and skipping

3. **Secrets Management** (`test_secrets_management.py`)
   - Environment variable fallback
   - Vault integration
   - AWS Secrets Manager integration
   - Secret masking

4. **Database Migration System** (`test_migration_system.py`)
   - Migration creation
   - Migration validation
   - Status tracking
   - Rollback capabilities

## Running Integration Tests

### Run All Integration Tests

```bash
pytest tests/integration/ -v
```

### Run Specific Test Suite

```bash
# Legal documents
pytest tests/integration/test_legal_acceptance_flow.py -v

# Onboarding
pytest tests/integration/test_onboarding_flow.py -v

# Secrets management
pytest tests/integration/test_secrets_management.py -v

# Migrations
pytest tests/integration/test_migration_system.py -v
```

### Run with Coverage

```bash
pytest tests/integration/ --cov=web --cov=services --cov-report=html
```

## Test Requirements

### Environment Setup

1. **Database**: PostgreSQL test database
2. **Redis**: For caching tests (optional)
3. **Environment Variables**: Test configuration

### Test Database Setup

```bash
# Create test database
createdb ai_investor_test

# Run migrations
python scripts/database/migrate.py up
```

## Writing Integration Tests

### Example: Testing a Complete Flow

```python
import pytest
from flask import Flask
from web.api.your_api import your_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(your_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_complete_flow(client):
    # Step 1: Initial state
    response = client.get('/api/v1/endpoint')
    assert response.status_code == 200
    
    # Step 2: Perform action
    response = client.post('/api/v1/endpoint', json={'data': 'value'})
    assert response.status_code == 200
    
    # Step 3: Verify result
    response = client.get('/api/v1/endpoint')
    assert response.status_code == 200
    data = response.get_json()
    assert data['data'] == 'value'
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Clean up test data after each test
3. **Mocking**: Mock external services (databases, APIs)
4. **Assertions**: Test both success and error cases
5. **Coverage**: Aim for high coverage of integration paths

## CI/CD Integration

Integration tests run automatically in CI:

```yaml
# .github/workflows/ci.yml
- name: Run Integration Tests
  run: pytest tests/integration/ -v --cov
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check test database exists
   - Verify connection string
   - Ensure migrations are run

2. **Import Errors**
   - Check PYTHONPATH
   - Verify all dependencies installed

3. **Test Failures**
   - Check test logs
   - Verify mock setup
   - Ensure test data is clean

## Next Steps

- Add more integration test suites
- Expand test coverage
- Add performance integration tests
- Add security integration tests
