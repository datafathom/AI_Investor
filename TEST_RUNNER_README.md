# Test Runner CLI - User Guide

## Overview

The test runner is fully integrated into the unified CLI system (`cli.py`). All test commands are available directly through `python cli.py`. This makes it easy to run specific subsets of tests during development.

## Quick Start

```bash
# List all available test categories
python cli.py test list

# Run all tests
python cli.py test all

# Run backend service tests
python cli.py test backend

# Run frontend component tests
python cli.py test frontend

# Run API endpoint tests
python cli.py test api

# Run with coverage report
python cli.py test backend --coverage

# Run specific category
python cli.py test-category backend-phase1 --coverage --verbose

# Run any test category directly
python cli.py test-category api-trading --coverage
python cli.py test-category models-core -v
python cli.py test-category quick
```

## Available Categories

### Backend Services

- `backend` - All backend service tests (Phases 1-4)
- `backend-phase1` - Critical services (analytics, optimization, risk, tax)
- `backend-phase2` - Core features (options, trading, planning, etc.)
- `backend-phase3` - Supporting features (news, watchlist, research, etc.)
- `backend-phase4` - Platform features (AI, ML, integrations, etc.)

### Frontend

- `frontend` - All frontend React component tests

### API Endpoints

- `api` - All API endpoint tests
- `api-analytics` - Analytics and attribution APIs
- `api-trading` - Trading and brokerage APIs
- `api-payments` - Payment processing APIs
- `api-crypto` - Cryptocurrency and blockchain APIs
- `api-social` - Social media and sentiment APIs
- `api-integrations` - Third-party integration APIs
- `api-notifications` - Notification and communication APIs
- `api-auth` - Authentication and OAuth APIs
- `api-financial` - Financial planning and management APIs
- `api-ai` - AI, ML, and automation APIs
- `api-platform` - Platform and enterprise APIs
- `api-market` - Market data and analysis APIs
- `api-risk` - Risk management and analysis APIs
- `api-tax` - Tax optimization and reporting APIs
- `api-other` - Miscellaneous APIs

### Models

- `models` - All Pydantic model validation tests
- `models-core` - Core business logic models
- `models-financial` - Financial planning and management models
- `models-platform` - Platform and infrastructure models
- `models-ai` - AI and machine learning models
- `models-social` - Social trading and community models
- `models-other` - Other model tests

### Combined Suites

- `all` - Run all tests across the entire application
- `unit` - All unit tests (services and models)
- `integration` - Integration tests (APIs and frontend)
- `quick` - Quick smoke tests for critical paths

## Command Options

### Basic Options

```bash
# Verbose output
python run_tests.py backend -v

# Generate coverage report
python run_tests.py backend --coverage

# Run tests in parallel (requires pytest-xdist)
python run_tests.py backend --parallel

# Stop on first failure
python run_tests.py backend -x

# Generate HTML test report
python run_tests.py backend --html
```

### Advanced Options

```bash
# Run tests with specific markers
python run_tests.py backend -m unit -m slow

# Combine options
python run_tests.py api-trading -v --coverage --html
```

## Examples

### Development Workflow

```bash
# Quick check before committing
python run_tests.py quick

# Test your specific feature area
python run_tests.py api-trading -v

# Full test suite with coverage
python run_tests.py all --coverage
```

### CI/CD Integration

```bash
# Run all tests in parallel
python run_tests.py all --parallel

# Run with HTML report for artifacts
python run_tests.py all --html --coverage
```

### Debugging

```bash
# Run specific category with verbose output
python run_tests.py backend-phase1 -v -x

# Run with specific markers
python run_tests.py backend -m unit
```

## Coverage Reports

When using `--coverage`, the tool generates:

- **Terminal output**: Coverage summary with missing lines
- **HTML report**: Detailed coverage report in `htmlcov/` directory
- **XML report**: Coverage data in `coverage.xml` (for CI/CD)

View HTML report:
```bash
# After running with --coverage
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## Test Markers

Tests can be marked with pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.async` - Async tests

Filter by markers:
```bash
python run_tests.py backend -m unit
python run_tests.py api -m "not slow"
```

## Tips

1. **Use `quick` for fast feedback** during development
2. **Use `--coverage` regularly** to track coverage metrics
3. **Use `-x` for debugging** to stop on first failure
4. **Use `--parallel` for speed** when running large suites
5. **Use `--html` for detailed reports** to share with team

## Troubleshooting

### Tests not found
- Ensure you're in the project root directory
- Check that test paths exist in the category definition

### Import errors
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

### Coverage not working
- Ensure `pytest-cov` is installed: `pip install pytest-cov`
- Check that source paths are correct in `pytest.ini`

### Parallel execution issues
- Install `pytest-xdist`: `pip install pytest-xdist`
- Some tests may not be thread-safe

## Integration with IDEs

### VS Code
Add to `.vscode/settings.json`:
```json
{
  "python.testing.pytestArgs": [
    "--verbose"
  ],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

### PyCharm
Configure pytest as test runner and use the categories as test configurations.

## Contributing

To add a new test category, edit `run_tests.py` and add to `TEST_CATEGORIES` dictionary:

```python
'new-category': {
    'name': 'New Category Name',
    'paths': ['tests/path1', 'tests/path2'],
    'description': 'Description of what this category tests'
}
```
