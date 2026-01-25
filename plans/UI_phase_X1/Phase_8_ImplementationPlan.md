# Phase 8: Multi-Asset Cryptographic Vaulting & Web3 GUI

> **Phase 51** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Integrates decentralized 'Metabolism' metrics (gas, liquidity) into the centralized homeostasis model.

---

## Overview

Interface for cold/hot wallet orchestration and DeFi position tracking. Bridges the gap between traditional finance and decentralized protocols.

---

## Sub-Deliverable 51.1: Hardware Wallet Connectivity Dashboard

### Description
Secure interface for Ledger/Trezor balance monitoring without exposing private keys.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Crypto/WalletDashboard.jsx` | Main dashboard |
| `[NEW]` | `frontend2/src/widgets/Crypto/WalletDashboard.css` | Dashboard styling |
| `[NEW]` | `frontend2/src/widgets/Crypto/WalletCard.jsx` | Individual wallet card |
| `[NEW]` | `frontend2/src/services/blockchainService.js` | Blockchain node connections |
| `[NEW]` | `frontend2/src/stores/cryptoStore.js` | Zustand store for crypto |

### Verbose Acceptance Criteria

1. **WebSocket Blockchain Connectivity**
   - [ ] Maintain connections to Ethereum, Bitcoin, Polygon nodes
   - [ ] Target uptime: >99.9%
   - [ ] Auto-reconnect logic with exponential backoff
   - [ ] Connection status indicator per chain

2. **Security: Masked Public Keys**
   - [ ] Public keys masked by default: `0x1234...abcd`
   - [ ] Zustand state encrypts addresses in memory
   - [ ] Biometric/PIN interaction required to reveal full address
   - [ ] "Copy" button only available after reveal

3. **Real-time USD Valuation**
   - [ ] Kafka-driven price feeds from Phase 6
   - [ ] Update balances in real-time
   - [ ] 24h change percentage with green/red indicator
   - [ ] Support multi-currency display (USD, EUR, BTC)

4. **Multi-Wallet Support**
   - [ ] Add multiple hardware wallets
   - [ ] Label wallets: "Cold Storage", "Trading", etc.
   - [ ] Aggregate total across all wallets
   - [ ] Group by blockchain network

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/crypto/wallets` | GET/POST | List/add wallet addresses |
| `/api/v1/crypto/balances` | GET | Current balances with USD value |
| `/ws/crypto-prices` | WS | Real-time price stream |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `WalletDashboard.test.jsx` | Renders wallets, handles connection status, balance updates |
| `WalletCard.test.jsx` | Mask/reveal toggle, copy functionality |
| `blockchainService.test.js` | Connection logic, reconnect behavior |
| `cryptoStore.test.js` | State encryption, wallet CRUD |

### Test Coverage Target: **85%** (security-critical)

---

## Sub-Deliverable 51.2: On-chain Liquidity Provider (LP) Position Tracker

### Description
Visualizes impermanent loss and yield generation for DEX positions like Uniswap, Curve, Balancer.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Crypto/LPTracker.jsx` | LP position widget |
| `[NEW]` | `frontend2/src/widgets/Crypto/LPTracker.css` | Widget styling |
| `[NEW]` | `frontend2/src/widgets/Crypto/ImpermanentLossChart.jsx` | IL visualization |
| `[NEW]` | `frontend2/src/services/defiService.js` | DeFi protocol integration |

### Verbose Acceptance Criteria

1. **HODL vs LP Value Visualization**
   - [ ] D3.js dual-line chart comparing strategies
   - [ ] "HODL Value": What tokens would be worth if just held
   - [ ] "LP Value": Actual value in liquidity pool
   - [ ] Difference = Impermanent Loss (or Gain)

2. **Pool Drain Event Detection**
   - [ ] Monitor for abnormal slippage telemetry
   - [ ] Alert on sudden liquidity drops >20%
   - [ ] "Pool Drain Warning" notification
   - [ ] Historical drain events marked on chart

3. **Neo4j Relationship Mapping**
   - [ ] LP nodes mapped with `LIQUIDITY_SOURCE` relationships
   - [ ] Connect LP positions to underlying token nodes
   - [ ] Query: "Which tokens are exposed via LP?"
   - [ ] Visualize as mini force-directed graph

4. **Yield Tracking**
   - [ ] Display earned fees over time
   - [ ] APY calculation based on historical performance
   - [ ] Compare to "Risk-Free Rate" (T-Bill yield)
   - [ ] Net yield = Fees - Impermanent Loss

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `LPTracker.test.jsx` | LP positions render, IL calculation correct |
| `ImpermanentLossChart.test.jsx` | Chart renders both lines, updates on data change |
| `defiService.test.js` | Pool data fetching, drain detection logic |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 51.3: Gas Fee Optimization & Speed Controller

### Description
Monitoring network congestion as a 'System Metabolism' check, preventing overpaying for transactions.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Crypto/GasPulse.jsx` | Gas monitoring widget |
| `[NEW]` | `frontend2/src/widgets/Crypto/GasPulse.css` | Widget styling |
| `[NEW]` | `frontend2/src/widgets/Crypto/TransactionQueue.jsx` | Pending tx queue |
| `[NEW]` | `frontend2/src/hooks/useGasPrice.js` | Gas price hook |

### Verbose Acceptance Criteria

1. **Real-time Gwei Pulse Widget**
   - [ ] Current gas price prominently displayed
   - [ ] Historical average overlay (7-day, 30-day)
   - [ ] Speed tiers: Slow (10min), Standard (5min), Fast (1min)
   - [ ] Animated pulse effect synced to block time

2. **Meta-Transaction Builder**
   - [ ] Zustand-based queue for pending transactions
   - [ ] Queue low-priority trades during gas troughs
   - [ ] "Execute All" when gas drops below threshold
   - [ ] Priority ordering within queue

3. **Gas Spike Alerts**
   - [ ] Alert when gas exceeds 3 standard deviations
   - [ ] Historical spike analysis
   - [ ] "Wait" recommendation when spike detected
   - [ ] Notification integration (toast + optional push)

4. **Cost Estimator**
   - [ ] Estimate USD cost for common operations
   - [ ] Swap, LP deposit/withdraw, NFT mint
   - [ ] Comparison to historical costs

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `GasPulse.test.jsx` | Displays current gas, historical overlay works |
| `TransactionQueue.test.jsx` | Queue CRUD operations, execute all logic |
| `useGasPrice.test.js` | Updates on new data, spike detection |

### Test Coverage Target: **80%**

---

## Widget Registry Entries

```javascript
{
  id: 'wallet-dashboard',
  name: 'Crypto Wallet Dashboard',
  component: lazy(() => import('../../widgets/Crypto/WalletDashboard')),
  category: 'Crypto',
  defaultSize: { width: 500, height: 400 }
},
{
  id: 'lp-tracker',
  name: 'LP Position Tracker',
  component: lazy(() => import('../../widgets/Crypto/LPTracker')),
  category: 'Crypto',
  defaultSize: { width: 550, height: 400 }
},
{
  id: 'gas-pulse',
  name: 'Gas Fee Monitor',
  component: lazy(() => import('../../widgets/Crypto/GasPulse')),
  category: 'Crypto',
  defaultSize: { width: 350, height: 300 }
}
```

---

## Route Integration

**Route:** `/strategist/crypto`

**Macro Task:** The Strategist

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |
