# Phase 72: Private Equity & Illiquid Asset Manager

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Alternative Data Team

---

## 📋 Overview

**Description**: Manage assets that don't have a ticker. Private Equity, Venture Capital, Art, Classic Cars. "Mark to Market" manually or via appraisal. Track "Capital Calls" and "Committed Capital".

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 72

---

## 🎯 Sub-Deliverables

### 72.1 Manual Asset Entry Portal `[ ]`

**Acceptance Criteria**: UI to create custom assets. "Series A Investment in Stripe". Fields: Cost Basis, Date, committed_capital, called_capital.

| Component | File Path | Status |
|-----------|-----------|--------|
| Entry UI | `frontend2/src/components/Assets/PrivateEntry.jsx` | `[ ]` |

---

### 72.2 Capital Call Tracker `[ ]`

**Acceptance Criteria**: Track "Dry Powder". If I committed $100k and paid $20k, I have a $80k liability that could be called any time. This reduces "true" liquid cash.

| Component | File Path | Status |
|-----------|-----------|--------|
| Liability Tracker | `services/risk/capital_calls.py` | `[ ]` |

---

### 72.3 Valuation Update Log (Mark-to-Model) `[ ]`

**Acceptance Criteria**: Log valuation updates. "Stripe valued at $60B". Update portfolio NAV. Store in `valuation_history` table.

| Component | File Path | Status |
|-----------|-----------|--------|
| Valuation Log | `services/accounting/private_val.py` | `[ ]` |

---

### 72.4 J-Curve Visualization `[ ]`

**Acceptance Criteria**: Visualize the J-Curve effect (initial negative returns due to fees, followed by harvesting).

| Component | File Path | Status |
|-----------|-----------|--------|
| J-Curve Chart | `frontend2/src/components/Charts/JCurve.jsx` | `[ ]` |

### 72.5 Secondaries Market Scraper (Links) `[ ]`

**Acceptance Criteria**: Scrape secondary marketplaces (Forge, EquityZen) to find "Indicative Pricing" for private shares.

| Component | File Path | Status |
|-----------|-----------|--------|
| Scraper | `services/ingestion/secondaries.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py private add <name>` | Create asset | `[ ]` |
| `python cli.py private update-val` | Mark to market | `[ ]` |

---

*Last verified: 2026-01-25*
