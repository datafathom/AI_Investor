# Runners: Domain and Agent Task Runners

## Overview
Domain runners are thin, standardized wrappers used to execute specific financial or organizational tasks in isolation. They are primarily used for testing specific agent capabilities or performing manual overrides.

## Key Categories

### Financial Strategy Runners
- `risk_runner.py`: Executes risk assessment models for portfolios.
- `hedging_runner.py`: Runs hedging optimization algorithms.
- `pe_runner.py` / `vc_runner.py`: Executes deal analysis for Private Equity and Venture Capital.

### Legal and Compliance Runners
- `rule144_runner.py`: Validates trades against SEC Rule 144 constraints.
- `fatca_runner.py`: verify tax compliance for international institutional clients.
- `privacy_runner.py`: triggers data anonymity and privacy audits for sensitive records.

### Operations and HR Runners
- `hr_runner.py`: manages internal agent role assignments and performance tracking.
- `deployment_runner.py`: specialized domain logic for multi-cloud deployment strategies.

## Architecture
All domain runners inherit from a common base or follow a standardized pattern:
1. Load Domain Context (Portfolio ID, Client ID).
2. Initialize the relevant Service or Agent.
3. Call the target method (`analyze`, `optimize`, `verify`).
4. Log results to the `UnifiedActivityService`.

## Status
**Essential (Functional)**: provides the necessary granularity for testing and executing high-stakes financial logic in a controlled environment.
