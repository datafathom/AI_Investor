# Phase 56: Multi-Currency Cash Management & FX Conversion

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Treasury Team

---

## 📋 Overview

**Description**: Manage global liquidity. If you buy a Japanese Stock, you need JPY. Optimizing the conversion (FX Rate) and holding multi-currency balances allows for "Jurisdictional Arbitrage" and hedging against USD collapse.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 56

---

## 🎯 Sub-Deliverables

### 56.1 Global Cash Pulse Widget `[x]`

**Acceptance Criteria**: Implement a Global Cash Balance 'Pulse' Widget updating FX rates from `fx-stream-global` every 10s. Show Total Value in Base Currency (USD).

| Component | File Path | Status |
|-----------|-----------|--------|
| Widget | `frontend2/src/components/Treasury/CashPulse.jsx` | `[x]` |

---

### 56.2 Carry Trade Heatmap `[x]`

**Acceptance Criteria**: Configure 'Heat' indicators for currencies with high overnight interest rates (e.g., BRL, MXN) vs Funding Currencies (JPY, CHF) for potential Carry Trades.

| Component | File Path | Status |
|-----------|-----------|--------|
| Heatmap | `frontend2/src/components/Treasury/CarryHeat.jsx` | `[x]` |

---

### 56.3 Iceberg Order FX Interface `[x]`

**Acceptance Criteria**: Develop a Limit-Order FX Interface supporting 'Iceberg' orders to minimize market impact when converting large sums.

| Component | File Path | Status |
|-----------|-----------|--------|
| Order Interface | `frontend2/src/components/Trading/FXOrder.jsx` | `[x]` |

---

### 56.4 Currency Exposure Risk Guard `[x]`

**Acceptance Criteria**: Integrate Risk Guardrails to prevent unauthorized currency exposure exceeding 15% of the portfolio (unless explicitly hedging).

| Component | File Path | Status |
|-----------|-----------|--------|
| Exposure Guard | `services/risk/fx_guard.py` | `[x]` |

---

### 56.5 Idle Cash Deployment Suggestions `[x]`

**Acceptance Criteria**: Identify idle cash and suggest high-yield deployment (MMFs, T-Bills) when cash balance > $50,000 in any single currency.

| Component | File Path | Status |
|-----------|-----------|--------|
| Idle Sweeper | `services/treasury/idle_sweeper.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py fx convert <amount>` | Execute spot | `[x]` |
| `python cli.py fx check-exposure` | Show risk | `[x]` |

---

*Last verified: 2026-01-25*
