# CLI Command: test

## Description
Run test suites by category

## Main Help Output
```text

Command: test
Description: Run test suites by category

Available subcommands:
  all                  Run all tests across the entire application
  api                  Run API endpoint tests
  backend              Run all backend service tests
  frontend             Run frontend component tests
  integration          Run integration tests (APIs and frontend)
  list                 List all available test categories
  models               Run Pydantic model validation tests
  quick                Run quick smoke tests for critical paths
  unit                 Run all unit tests (services and models)


```

## Subcommands

### Subcommand: `test list`
List all available test categories

#### Help Output
```text

Command: test list
Description: List all available test categories


```

### Subcommand: `test all`
Run all tests across the entire application

#### Help Output
```text

Command: test all
Description: Run all tests across the entire application

Arguments:
  category             Test category (default: all) (Optional, Default: all)

Flags:
  -v, --verbose            Verbose output (Default: False)
  --coverage           Generate coverage report (Default: False)
  -n, --parallel           Run tests in parallel (Default: False)
  -x, --fail-fast          Stop on first failure (Default: False)
  --html               Generate HTML test report (Default: False)


```

### Subcommand: `test backend`
Run all backend service tests

#### Help Output
```text

Command: test backend
Description: Run all backend service tests

Arguments:
  category              (Optional, Default: backend)

Flags:
  -v, --verbose             (Default: False)
  --coverage            (Default: False)
  -n, --parallel            (Default: False)
  -x, --fail-fast           (Default: False)


```

### Subcommand: `test frontend`
Run frontend component tests

#### Help Output
```text

Command: test frontend
Description: Run frontend component tests

Arguments:
  category              (Optional, Default: frontend)

Flags:
  -v, --verbose             (Default: False)
  --coverage            (Default: False)


```

### Subcommand: `test api`
Run API endpoint tests

#### Help Output
```text

Command: test api
Description: Run API endpoint tests

Arguments:
  category              (Optional, Default: api)

Flags:
  -v, --verbose             (Default: False)
  --coverage            (Default: False)
  -n, --parallel            (Default: False)


```

### Subcommand: `test models`
Run Pydantic model validation tests

#### Help Output
```text

Command: test models
Description: Run Pydantic model validation tests

Arguments:
  category              (Optional, Default: models)

Flags:
  -v, --verbose             (Default: False)
  --coverage            (Default: False)


```

### Subcommand: `test quick`
Run quick smoke tests for critical paths

#### Help Output
```text

Command: test quick
Description: Run quick smoke tests for critical paths

Arguments:
  category              (Optional, Default: quick)

Flags:
  -v, --verbose             (Default: False)


```

### Subcommand: `test unit`
Run all unit tests (services and models)

#### Help Output
```text

Command: test unit
Description: Run all unit tests (services and models)

Arguments:
  category              (Optional, Default: unit)

Flags:
  -v, --verbose             (Default: False)
  --coverage            (Default: False)


```

### Subcommand: `test integration`
Run integration tests (APIs and frontend)

#### Help Output
```text

Command: test integration
Description: Run integration tests (APIs and frontend)

Arguments:
  category              (Optional, Default: integration)

Flags:
  -v, --verbose             (Default: False)
  --coverage            (Default: False)


```

