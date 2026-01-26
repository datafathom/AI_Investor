# Phase 12: Brokerage OAuth & Market Data
> **Phase ID**: 12
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement brokerage connectivity for live trading and market data feeds. This phase focuses on the OAuth flow (or API Key management) for platforms like Alpaca or Interactive Brokers (IBKR), enabling the AI to retrieve real-time portfolio balance, positions, and quotes.

## Objectives
- [ ] Add `alpaca-trade-api` and `plaid-python` (already added) for brokerage coverage.
- [ ] Create `BrokerageService` (backend) with support for:
    - **Native Execution**: Alpaca, Interactive Brokers (IBKR).
    - **Secured Aggregation**: Fidelity, Charles Schwab, Robinhood, E*TRADE, Vanguard (via Plaid/SnapTrade).
    - **Payment Processors**: PayPal, Stripe, Venmo, Square, Cash App.
- [ ] Implement AES-256 encryption for all stored API keys/tokens.
- [ ] Add API endpoints for institution search and connection.
- [ ] Create `InstitutionalConnectorWidget` (frontend) to handle all vendor types.
- [ ] Integrate connectivity status into the `BrokerageAccount` page.

## Files to Modify/Create
1.  `requirements.txt` (Add `alpaca-trade-api`)
2.  `services/brokerage/brokerage_service.py` **[NEW]**
3.  `web/api/brokerage_api.py` **[NEW]**
4.  `web/app.py` (Register Brokerage API)
5.  `frontend2/src/widgets/Brokerage/BrokerageConnectivityWidget.jsx` **[NEW]**
6.  `frontend2/src/pages/BrokerageAccount.jsx` (Integrate Widget)

## Technical Design

### Backend (`BrokerageService`)
- Uses `alpaca-trade-api` for Alpaca or a generic wrapper for multiple brokers.
- Stores credentials securely using the `SecretManager`.
- **Simulation Mode**: Fallback to mock positions and paper trading status if no API keys provided.
- `get_positions()`: Combine live positions with internal tracking for reconciliation.

### API
- Protected by `@login_required` and `@requires_role('trader')`.

### Frontend
- **BrokerageConnectivityWidget**: Allows users to input API keys or start an OAuth flow.
- Shows real-time connection status (Connected/Disconnected/Latency).
- Displays "Paper Trading" vs "Live" toggle indicators.

## Verification Plan

### Automated Tests
- `tests/system/test_brokerage_service.py`:
    - Mock Alpaca API responses.
    - Verify position retrieval and formatting.
    - Test credential validation logic.

### Manual Verification
1.  Navigate to `/portfolio/brokerage`.
2.  Connect a "Paper Trading" Alpaca account via the widget.
3.  Verify live positions and buying power appear correctly.
