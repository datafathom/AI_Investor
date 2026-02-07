# Script: gen_task_batches.py

## Overview
`gen_task_batches.py` is an infrastructure-as-code utility that organizes API endpoints into logical "verification batches" for parallel or sequential testing.

## Core Functionality
- **Grouping Logic**: Groups endpoints by their functional domain (e.g., Onboarding, Analytics, Execution).
- **Metadata Generation**: Produces a JSON manifest that maps each endpoint to its expected HTTP method, parameters, and required authentication level. This manifest is used by automated test runners like `verify_batch_1.py`.

## Status
**Essential (Testing Infrastructure)**: Forms the foundation of the tiered testing strategy, allowing for efficient verification of large groups of endpoints.
