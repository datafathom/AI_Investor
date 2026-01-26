# Phase 71: Crypto Tax & Basis Tracking (FIFO/LIFO/HIFO)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax Team

---

## 📋 Overview

**Description**: Advanced cost-basis tracking for Crypto. "SpecID" allows selling the highest cost Bitcoin first (HIFO) to minimize taxes. Essential for high-frequency crypto activity.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 71

---

## 🎯 Sub-Deliverables

### 71.1 Multi-Method Basis Engine (FIFO/LIFO/HIFO) `[ ]`

**Acceptance Criteria**: Engine that calculates P&L using different accounting methods. Allow user to select per-asset.

| Component | File Path | Status |
|-----------|-----------|--------|
| Basis Engine | `services/tax/crypto_basis.py` | `[ ]` |

---

### 71.2 Gas Fee Deduction Logic `[ ]`

**Acceptance Criteria**: Ensure Gas Fees are correctly added to the Cost Basis of the acquired asset, or deducted as expense (depending on jurisdiction).

| Component | File Path | Status |
|-----------|-----------|--------|
| Gas Handler | `services/tax/gas_logic.py` | `[ ]` |

---

### 71.3 Defi Staking Income Classifier `[ ]`

**Acceptance Criteria**: Classify Staking Rewards/Airdrops as "Income" (taxed at entry) vs Capital Gains (taxed at sale).

| Component | File Path | Status |
|-----------|-----------|--------|
| Defi Classifier | `services/compliance/defi_tax.py` | `[ ]` |

---

### 71.4 Cross-Chain Bridge Tracking `[ ]`

**Acceptance Criteria**: Track assets bridging from ETH to Solana. Ensure basis carries over and isn't treated as a taxable sale (unless it is a wrap).

| Component | File Path | Status |
|-----------|-----------|--------|
| Bridge Tracker | `services/crypto/cross_chain.py` | `[ ]` |

### 71.5 Form 8949 Generator (Crypto) `[ ]`

**Acceptance Criteria**: Generate the specific IRS Form 8949 for Digital Assets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Form Gen | `services/reporting/crypto_8949.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax crypto-basis` | Show current basis | `[ ]` |
| `python cli.py tax optimize-method` | Suggest HIFO | `[ ]` |

---

*Last verified: 2026-01-25*
