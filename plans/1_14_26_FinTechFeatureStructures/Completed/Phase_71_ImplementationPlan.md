# Phase 71: Crypto Tax & Basis Tracking (FIFO/LIFO/HIFO)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax Team

---

## 📋 Overview

**Description**: Advanced cost-basis tracking for Crypto. "SpecID" allows selling the highest cost Bitcoin first (HIFO) to minimize taxes. Essential for high-frequency crypto activity.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 71

---

## 🎯 Sub-Deliverables

### 71.1 Multi-Method Basis Engine (FIFO/LIFO/HIFO) `[x]`

**Acceptance Criteria**: Engine that calculates P&L using different accounting methods. Allow user to select per-asset.

| Component | File Path | Status |
|-----------|-----------|--------|
| Basis Engine | `services/tax/crypto_basis.py` | `[x]` |

---

### 71.2 Gas Fee Deduction Logic `[x]`

**Acceptance Criteria**: Ensure Gas Fees are correctly added to the Cost Basis of the acquired asset, or deducted as expense (depending on jurisdiction).

| Component | File Path | Status |
|-----------|-----------|--------|
| Gas Handler | `services/tax/gas_logic.py` | `[x]` |

---

### 71.3 Defi Staking Income Classifier `[x]`

**Acceptance Criteria**: Classify Staking Rewards/Airdrops as "Income" (taxed at entry) vs Capital Gains (taxed at sale).

| Component | File Path | Status |
|-----------|-----------|--------|
| Defi Classifier | `services/compliance/defi_tax.py` | `[x]` |

---

### 71.4 Cross-Chain Bridge Tracking `[x]`

**Acceptance Criteria**: Track assets bridging from ETH to Solana. Ensure basis carries over and isn't treated as a taxable sale (unless it is a wrap).

| Component | File Path | Status |
|-----------|-----------|--------|
| Bridge Tracker | `services/crypto/cross_chain.py` | `[x]` |

### 71.5 Form 8949 Generator (Crypto) `[x]`

**Acceptance Criteria**: Generate the specific IRS Form 8949 for Digital Assets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Form Gen | `services/reporting/crypto_8949.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax crypto-basis` | Show current basis | `[x]` |
| `python cli.py tax optimize-method` | Suggest HIFO | `[x]` |

---

*Last verified: 2026-01-25*
