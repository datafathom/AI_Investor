# Phase 10: Banking Connectivity (Plaid Link)
> **Phase ID**: 10
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement banking connectivity using the Plaid API. This allows users to securely link their bank accounts, enabling the AI to track real-world transactions and balances. For this phase, we will implement the Link flow, token exchange, and a basic account synchronization service (simulated for demo purposes if API keys are missing).

## Objectives
- [ ] Add `plaid-python` to `requirements.txt`.
- [ ] Create `BankingService` (backend) to interface with Plaid.
- [ ] Implement API endpoints:
    - `POST /api/v1/banking/plaid/create-link-token`
    - `POST /api/v1/banking/plaid/exchange-public-token`
    - `GET /api/v1/banking/accounts`
- [ ] Create `PlaidLinkWidget` (frontend) to trigger the Link flow.
- [ ] Handle simulated Plaid webhooks for transaction updates.

## Files to Modify/Create
1.  `requirements.txt` (Add `plaid-python`)
2.  `services/banking/banking_service.py` **[NEW]**
3.  `web/api/banking_api.py` **[NEW]**
4.  `web/app.py` (Register Banking API)
5.  `frontend2/src/widgets/Banking/PlaidLinkWidget.jsx` **[NEW]**
6.  `frontend2/src/pages/CashFlowDashboard.jsx` (Add Widget)

## Technical Design

### Backend (`BankingService`)
- Uses `plaid-python` client.
- Stores `access_tokens` securely (linked to `user_id` in Postgres).
- **Simulation Mode**: If `PLAID_CLIENT_ID` is missing, return fallback mock tokens for the demo.
- `sync_transactions()`: Fetch transactions from Plaid and emit via Kafka/SocketIO.

### API
- Protected by `@login_required`.
- Role check: `trader` or `admin`.

### Frontend
- Uses `react-plaid-link` (or a custom wrapper).
- Displays "Connect Bank" button.
- Shows connected accounts and real-time balances.

## Verification Plan

### Automated Tests
- `tests/system/test_banking_service.py`:
    - Mock Plaid API responses.
    - Verify token exchange logic.
    - Verify account retrieval.

### Manual Verification
1.  Navigate to `/cash-flow` (or relevant page).
2.  Click "Connect Bank".
3.  Complete simulated Plaid Link flow.
4.  Verify balance appears in the widget.
