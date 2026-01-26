# Phase 51: Multi-Asset Cryptographic Vaulting & Web3 GUI

> **Phase ID**: 51 | Status: `[ ]` Not Started
> Last Updated: 2026-01-18
> Strategic Importance: Integrates decentralized 'Metabolism' metrics (gas, liquidity) into the centralized homeostasis model.

---

## Overview

Interface for cold/hot wallet orchestration and DeFi position tracking.

---

## Sub-Deliverable 51.1: Hardware Wallet Connectivity Dashboard

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Web3/WalletDashboard.jsx` | Ledger/Trezor monitor |
| `[NEW]` | `frontend2/src/widgets/Web3/WalletDashboard.css` | Styling |
| `[NEW]` | `frontend2/src/stores/web3Store.js` | Web3 state management |
| `[NEW]` | `services/crypto/wallet_service.py` | Wallet connectivity |
| `[NEW]` | `web/api/web3_api.py` | REST endpoints |

### Verbose Acceptance Criteria

1. **WebSocket Connectivity**
   - [ ] > 99.9% uptime with automated retry logic
   - [ ] Connection status indicator
   - [ ] Multi-chain support (ETH, BTC, SOL)

2. **Security Masking**
   - [ ] Public keys masked by default
   - [ ] WebAuthn/OAuth 2.0 biometric reveal
   - [ ] Session timeout (5 min inactivity)

3. **Real-time Valuation**
   - [ ] Kafka-driven price feeds
   - [ ] Multi-exchange weighting (Binance, Coinbase, Kraken)
   - [ ] USD/EUR/BTC toggle

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `WalletDashboard.test.jsx` | Connection status, masking, valuation update |
| `web3Store.test.js` | State persistence, biometric flow mock |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/crypto/test_wallet_service.py` | `test_websocket_retry`, `test_multi_chain_balance`, `test_price_aggregation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 51.2: On-chain Liquidity Provider (LP) Position Tracker

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Web3/LPTracker.jsx` | LP position viewer |
| `[NEW]` | `frontend2/src/widgets/Web3/LPTracker.css` | Styling |
| `[NEW]` | `services/crypto/lp_tracker_service.py` | Impermanent loss calc |

### Verbose Acceptance Criteria

1. **Impermanent Loss Visualization**
   - [ ] D3.js chart: 'HODL Value' vs 'LP Value' over time
   - [ ] Percentage loss/gain display
   - [ ] Break-even marker

2. **Pool Drain Detection**
   - [ ] Abnormal slippage telemetry via Kafka
   - [ ] Auto-alert on pool imbalance
   - [ ] Exit recommendation

3. **Neo4j Mapping**
   - [ ] `LIQUIDITY_SOURCE` relationships to tokens
   - [ ] Correlation analysis edges
   - [ ] Graph visualization option

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `LPTracker.test.jsx` | IL chart renders, drain alert, graph toggle |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/crypto/test_lp_tracker_service.py` | `test_impermanent_loss_calc`, `test_pool_drain_detection`, `test_neo4j_mapping` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 51.3: Gas Fee Optimization & Speed Controller

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Web3/GasPulse.jsx` | Real-time Gwei monitor |
| `[NEW]` | `frontend2/src/widgets/Web3/GasPulse.css` | Styling |
| `[NEW]` | `services/crypto/gas_service.py` | Gas optimization |

### Verbose Acceptance Criteria

1. **Gwei Pulse Widget**
   - [ ] Real-time gas price display
   - [ ] Historical 24h moving average overlay
   - [ ] Color-coded urgency (low/medium/high)

2. **Meta-Transaction Builder**
   - [ ] Zustand-based transaction queue
   - [ ] Queue trades for gas troughs
   - [ ] Estimated savings display

3. **Spike Alerts**
   - [ ] Alert when gas > 3 std dev of 24h mean
   - [ ] Push notification option
   - [ ] Auto-pause pending transactions

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `GasPulse.test.jsx` | Pulse renders, queue works, spike alert |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/crypto/test_gas_service.py` | `test_gas_fetch`, `test_spike_detection`, `test_queue_optimization` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/portfolio/web3`

**Macro Task:** Decentralized Metabolism

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Web3

# Backend
.\venv\Scripts\python.exe -m pytest tests/crypto/ -v --cov=services/crypto
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/portfolio/web3
# Verify: Wallet connects (mock), LP tracker shows, gas pulse updates
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 51 detailed implementation plan |
