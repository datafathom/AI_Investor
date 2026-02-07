# Documentation: `test_lifestyle_economics.py` & `test_529_penalty.py`

## Overview
These tests cover the "Human" side of the financial OS: planning for lifestyle inflation (CLEW Index), generational wealth dilution, and the tax implications of specialized savings vehicles.

## Components Under Test
- `services.economics.clew_index_svc.CLEWIndexService`: Personal inflation for UHNW individuals.
- `services.planning.lifestyle_burn_svc.LifestyleBurnService`: Long-term burn rate projection.
- `services.estate.dilution_tracker_svc.DilutionTrackerService`: Generational wealth modeling.
- `services.tax.penalty_calculator_529.PenaltyCalculator529`: Education savings tax auditor.

## Key Test Scenarios

### 1. CLEW Index (Personal Inflation)
- **Goal**: Calculate the real cost of a high-net-worth lifestyle.
- **Assertions**: Correctly weights categories like Tuition (0.25) and Staff (0.15) to calculate a personal inflation rate (e.g., 4.75%) that typically exceeds the standard CPI.

### 2. Generational Dilution
- **Goal**: Map wealth survival across generations.
- **Assertions**: Correctly identifies "CLASS_DROP_RISK" if wealth dilution from multiple heirs is not offset by compounding growth (e.g., dropping below $10M per capita).

### 3. tax-Advantaged Auditing (529)
- **Goal**: Precise calculation of penalties for non-qualified withdrawals.
- **Assertions**: Correctly splits a withdrawal into principal (tax-free) and earnings (penalized at 10% + income tax), ensuring the client knows their exact net-to-hand capital.

## Holistic Context
Wealth management is about more than portfolio gains; it's about maintaining purchasing power across decades. These tests ensure the OS understands the complex interplay between inflation, family growth, and the IRS.
