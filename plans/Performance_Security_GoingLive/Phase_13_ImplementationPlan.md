# Phase 13: Live Order Execution Router
> **Phase ID**: 13
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Develop the core execution engine responsible for routing orders to live brokerages. This service integrates the strategy signals with the `BrokerageService` while enforcing the security safeties established in Phase Group B (Risk Limits, MFA, and the Kill Switch).

## Objectives
- [ ] Implement `ExecutionService` (backend) for order lifecycle management.
- [ ] Create order routing logic for REST/FIX protocols (via `alpaca-trade-api`).
- [ ] **Safety Integration**:
    - Check Kill Switch status before every order.
    - Validate against `RiskService` limits.
    - Require MFA for orders above a specific "High Value" threshold.
- [ ] Implement API endpoint `POST /api/v1/execution/order`.
- [ ] Create `OrderExecutionStatus` widget (frontend).
- [ ] Integrate with existing `TradeConfirmationModal`.

## Files to Modify/Create
1.  `services/brokerage/execution_service.py` **[NEW]**
2.  `web/api/brokerage_api.py` (Add order endpoints)
3.  `frontend2/src/components/AI_Investor/Execution/OrderExecutionStatus.jsx` **[NEW]**
4.  `frontend2/src/components/Modals/TradeConfirmationModal.jsx` (Integrate with backend)

## Technical Design

### Backend (`ExecutionService`)
- Responsible for: `place_order()`, `cancel_order()`, `get_order_status()`.
- **Pre-Flight Checks**:
    - `SecurityGateway`: Ensure not rate-limited.
    - `KillSwitch`: Abort if system is frozen.
    - `RiskService`: Check "Max Position Size" and "Daily Loss Limit".
- **Execution Flow**:
    1. Receive order request.
    2. Run pre-flight checks.
    3. (Optional) Check for MFA if large size.
    4. Call `BrokerageService` to send order to Alpaca/Market.
    5. Emit status update via Kafka/SocketIO.

### UI
- **OrderExecutionStatus**: A real-time log of orders placed by the AI, showing their status (Pending, Filled, Rejected, Cancelled).
- **Confirmation Flow**: Update the existing modal to send the `POST /api/v1/execution/order` request.

## Verification Plan

### Automated Tests
- `tests/system/test_execution_router.py`:
    - Test order routing with mock Alpaca client.
    - Test Kill Switch blocking order placement.
    - Test Risk Limit rejection.

### Manual Verification
1.  Trigger a trade from the UI.
2.  Verify the "Pre-Flight Check" animation appears.
3.  Confirm the order appears in the "Live Portal" position list (simulated/paper).
4.  Engage Kill Switch and attempt another trade; verify it is blocked.
