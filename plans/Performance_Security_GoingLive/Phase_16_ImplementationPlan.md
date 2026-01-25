# Phase 16: Multi-Currency Settlement System
> **Phase ID**: 16
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement a robust settlement engine to handle multi-currency accounts and foreign exchange (FX) conversions. This allows the AI Investor to manage portfolios across different global markets (e.g., USD, EUR, JPY) while providing a unified reporting currency.

## Objectives
- [ ] Implement `SettlementService` (backend) for currency conversion and balance management.
- [ ] Integrate a real-time (or near real-time) FX rates provider (e.g., via Alpaca or specialized FX API).
- [ ] Add API endpoints:
    - `GET /api/v1/settlement/rates`
    - `POST /api/v1/settlement/convert`
    - `GET /api/v1/settlement/balances`
- [ ] Create `SettlementDashboard` widget (frontend).
- [ ] Integrate into the `BrokerageAccount` page.

## Files to Modify/Create
1.  `services/brokerage/settlement_service.py` **[NEW]**
2.  `web/api/settlement_api.py` **[NEW]**
3.  `web/app.py` (Register Settlement API)
4.  `frontend2/src/widgets/Brokerage/SettlementDashboard.jsx` **[NEW]**
5.  `frontend2/src/pages/BrokerageAccount.jsx` (Integrate Widget)

## Technical Design

### Backend (`SettlementService`)
- Manages sub-balances for various currencies.
- **FX Provider**: Fetch rates via Alpaca (if available) or a common free FX API (simulated/cached).
- **Accounting**: Handle "T+2" settlement logic simulations (optional for demo, primary focus is balance conversion).

### API
- `GET /rates`: Provides conversion rates relative to a base currency (e.g., USD).
- `POST /convert`: Simulates an FX trade within the account.

### Frontend
- **SettlementDashboard**: Shows a breakdown of cash by currency, recent FX trades, and a "Quick Convert" tool.
- Visualizes currency weightings (USD vs EUR vs JPY).

## Verification Plan

### Automated Tests
- `tests/system/test_settlement_service.py`:
    - Test currency conversion math.
    - Test rate fetching/caching logic.
    - Test balance aggregation across multiple currencies.

### Manual Verification
1.  Navigate to the Brokerage Account page.
2.  Locate the Settlement widget.
3.  Simulate a conversion from USD to EUR.
4.  Verify total equity remains correct in the reporting currency.
