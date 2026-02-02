# Phase 44: Index Over-concentration Alert System

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Monitor the portfolio for hidden risks where individual stock holdings mirror the broad index. If you own AAPL *and* large amounts of QQQ (which is 10% AAPL), your concentration risk is magnified.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 44

---

## 🎯 Sub-Deliverables

### 44.1 Overlapping Holdings Identifier `[x]`

**Acceptance Criteria**: Identify overlapping holdings. Query ETF constituent data to find weight overlap.

```python
class OverlapScanner:
    def scan(self, portfolio: Portfolio) -> OverlapReport:
        # Decompose ETFs into constituents
        # Sum weights of underlying stocks
        # Report total exposure per ticker
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Scanner | `services/risk/overlap_scanner.py` | `[x]` |

---

### 44.2 Tech Concentration Alert (>35%) `[x]`

**Acceptance Criteria**: Alert the Warden if the top 5 technology companies (Mag 7) exceed 35% of total aggregate exposure (Direct + ETF).

| Component | File Path | Status |
|-----------|-----------|--------|
| Tech Alert | `services/alerts/tech_concentration.py` | `[x]` |

---

### 44.3 Negative Selection Bias Calc `[x]`

**Acceptance Criteria**: Calculate "Negative Selection Bias" for holdings within the Russell 2000 index (e.g., holding Zombie companies via the index).

| Component | File Path | Status |
|-----------|-----------|--------|
| Bias Calc | `services/analysis/negative_bias.py` | `[x]` |

---

### 44.4 De-concentration Suggestions `[x]`

**Acceptance Criteria**: Implement automated suggestions. "Sell AAPL stock to reduce overlap with QQQ holdings."

| Component | File Path | Status |
|-----------|-----------|--------|
| Suggestion Engine | `services/strategies/deconcentrate.py` | `[x]` |

### 44.5 Compliance Audit Log `[x]`

**Acceptance Criteria**: Log all 'Index Overlap' alerts to the compliance audit log with sector breakdown.

| Component | File Path | Status |
|-----------|-----------|--------|
| Audit Log | `services/logging/concentration_log.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py risk scan-overlap` | Find dupes | `[x]` |
| `python cli.py risk check-tech` | Mag 7 exposure | `[x]` |

---

*Last verified: 2026-01-25*
