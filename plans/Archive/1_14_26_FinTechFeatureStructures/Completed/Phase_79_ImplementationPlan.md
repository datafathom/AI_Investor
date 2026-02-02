# Phase 79: Venture Capital Portfolio Tracker

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Alternative Data Team

---

## 📋 Overview

**Description**: Specific tracker for Startup investments (SAFE, Convertible Notes). These are high risk, 10-year lockups. Need to track "Post-Money Valuation" caps and dilution.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 79

---

## 🎯 Sub-Deliverables

### 79.1 SAFE Note Calculator `[x]`

**Acceptance Criteria**: Calculate ownership %. Input: Investment Amount, Val Cap, Discount, Pre-Money Val of next round.

| Component | File Path | Status |
|-----------|-----------|--------|
| SAFE Calc | `services/valuation/safe_calc.py` | `[x]` |

---

### 79.2 Startup Portfolio Grid `[x]`

**Acceptance Criteria**: Grid UI showing all startup bets. Columns: "Vintage Year", "Sector", "Initial Inv", "Current Est Val", "MOIC" (Multiple on Invested Capital).

| Component | File Path | Status |
|-----------|-----------|--------|
| Grid UI | `frontend2/src/components/Assets/VCGrid.jsx` | `[x]` |

---

### 79.3 Dilution Simulator (Pro-Rata) `[x]`

**Acceptance Criteria**: Simulate dilution. "If they raise Series B at $40M pre, and you don't exercise Pro-Rata, your stake goes from 1.0% to 0.8%".

| Component | File Path | Status |
|-----------|-----------|--------|
| Dilution Sim | `services/simulation/dilution.py` | `[x]` |

---

### 79.4 QSBS Tax Eligibility Checker `[x]`

**Acceptance Criteria**: Track 5-year holding period for "Qualified Small Business Stock" (QSBS) section 1202 exclusion (0% federal tax).

| Component | File Path | Status |
|-----------|-----------|--------|
| QSBS Tracker | `services/tax/qsbs_track.py` | `[x]` |

### 79.5 Carta/Pulley Integration (Email Parsing) `[x]`

**Acceptance Criteria**: Ingest update emails from Carta/Pulley to auto-update valuations. (Regex parsing).

| Component | File Path | Status |
|-----------|-----------|--------|
| Parser | `services/ingestion/carta_parse.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py vc add-safe` | New investment | `[x]` |
| `python cli.py vc check-qsbs` | Eligibility | `[x]` |

---

*Last verified: 2026-01-25*
