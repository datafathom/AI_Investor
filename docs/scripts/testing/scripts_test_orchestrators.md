# Script: run_e2e_tests.sh / run_load_tests.sh

## Overview
These shell scripts provide standard entry points for executing heavy-duty testing suites in a local or CI environment.

## Core Functionality

### [run_e2e_tests.sh](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/testing/run_e2e_tests.sh)
- **Playwright Integration**: bootstraps and runs the Playwright E2E test suite located in the `frontend2` directory.
- **Config Management**: handles environment variables for BASE_URL, API_URL, and test credentials.
- **Filtering**: supports `--grep` for running specific subsets of tests.

### [run_load_tests.sh](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/testing/run_load_tests.sh)
- **Locust/k6 Orchestration**: triggers performance tests against the backend API to simulate realistic user traffic and measure service breaking points.

## Usage
```bash
./scripts/testing/run_e2e_tests.sh --headed
```

## Status
**Essential (Testing)**: standardizes the execution of long-running test suites across different developer machines and deployment environments.
