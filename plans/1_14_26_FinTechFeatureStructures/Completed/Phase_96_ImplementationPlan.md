# Phase 96: Global Energy Security Monitor

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Macro Strategy Team

---

## 📋 Overview

**Description**: Track Oil/Gas reserves. SPR (strategic petroleum reserve) levels. OPEC production cuts. Energy is the master input to GDP.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 96

---

## 🎯 Sub-Deliverables

### 96.1 SPR Level Tracker `[x]`

**Acceptance Criteria**: US Strategic Petroleum Reserve inventory. Low SPR = Vulnerability.

| Component | File Path | Status |
|-----------|-----------|--------|
| SPR Track | `services/market/spr_levels.py` | `[x]` |

---

### 96.2 OPEC Production Quotas `[x]`

**Acceptance Criteria**: Track detailed compliance. "Saudi cut 1M bpd".

| Component | File Path | Status |
|-----------|-----------|--------|
| OPEC Mon | `services/analysis/opec_compliance.py` | `[x]` |

---

### 96.3 Crack Spread Monitor (Refining) `[x]`

**Acceptance Criteria**: Margin for refiners (gasoline - crude). High spread = Bullish Valero/Exxon.

| Component | File Path | Status |
|-----------|-----------|--------|
| Crack Spread | `services/market/crack_spread.py` | `[x]` |

---

### 96.4 Natural Gas Storage (EU/US) `[x]`

**Acceptance Criteria**: Storage inventory levels relative to 5-year avg. Crucial for winter heating shocks.

| Component | File Path | Status |
|-----------|-----------|--------|
| NatGas Store | `services/market/ng_storage.py` | `[x]` |

### 96.5 Green Energy Transition CapEx `[x]`

**Acceptance Criteria**: Track CapEx into Solar/Wind. Long term structural shift.

| Component | File Path | Status |
|-----------|-----------|--------|
| Green CapEx | `services/analysis/green_capex.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py energy spr` | Show US reserves | `[x]` |
| `python cli.py energy ng-inv` | Gas storage | `[x]` |

---

*Last verified: 2026-01-25*
