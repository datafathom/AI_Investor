# Documentation: `tests/integration/test_broker_integration.py`

## Overview
This integration test validates "Phase 24: Broker Integration". It ensures that the execution layer can successfully communicate with brokerage providers, query balances, and manage order lifecycles.

## Components Under Test
- `services.execution.broker_service.get_broker`: Factory for brokerage clients.
- `MockBroker`: The default testing implementation.

## Test Workflow

### `run_test_broker`
1. **Authentication**: Verifies that the broker client can establish a secure session.
2. **Balance Check**: Queries the available cash balance to ensure the data channel is two-way.
3. **Order Placement**: Executes a simulated `BUY` order for 5 shares of `NVDA`.
4. **Position Verification**: Retrieves the account's current holdings to confirm that the executed order is now reflected in the inventory.

## Success Criteria
- Authentication returns `SUCCESS`.
- Cash balance is numeric and formatted correctly.
- NVDA position exists and matches the executed quantity.

## Holistic Context
This test verifies the "Exhale" or "Action" part of the platform. It ensures that when the AI decides to trade, it can actually reach the marketplace and that the state of the account is correctly synchronized post-trade.
