# Phase 39: Emergency Fund 'Moat' Maintenance

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Strategy Team

---

## 📋 Overview

**Description**: Ensure a 3-month to 3-year liquid cash buffer is maintained as a protective moat for the financial ecosystem. This prevents forced selling of long-term assets during short-term crises.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 39

---

## 🎯 Sub-Deliverables

### 39.1 Dynamic Moat Sizing (Expense Based) `[x]`

**Acceptance Criteria**: Define 'Moat' size dynamically based on monthly expense parameters entered by the user. (e.g., $5k expenses * 6 months = $30k Target).

| Component | File Path | Status |
|-----------|-----------|--------|
| Moat Calc | `services/planning/moat_calc.py` | `[x]` |

---

### 39.2 Cash Reserve Monitor API `[x]`

**Acceptance Criteria**: Monitor liquid cash reserves across all linked banking and brokerage accounts via API. Exclude invested assets.

| Component | File Path | Status |
|-----------|-----------|--------|
| Reserve Monitor | `services/banking/reserve_monitor.py` | `[x]` |

---

### 39.3 'Moat Breach' Alert `[x]`

**Acceptance Criteria**: Trigger a 'Moat Breach' alert if cash reserves drop below the survival threshold.

| Component | File Path | Status |
|-----------|-----------|--------|
| Breach Alert | `services/alerts/moat_breach.py` | `[x]` |

---

### 39.4 Automated Sweep Replenishment `[x]`

**Acceptance Criteria**: Implement automated 'Sweep' logic to replenish the moat using excess trading profits from the SearcherAgent if the moat is low.

```python
class MoatSweeper:
    def check_and_sweep(self):
        current_moat = self.monitor.get_cash()
        target = self.calc.get_target()
        if current_moat < target:
            self.searcher.redirect_profits(amount=target - current_moat)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweeper | `services/banking/sweeper.py` | `[x]` |

---

### 39.5 Zen Mode 'Days of Survival' Widget `[x]`

**Acceptance Criteria**: Visualize the 'Days of Survival' metric prominently in the Zen Mode dashboard.

| Component | File Path | Status |
|-----------|-----------|--------|
| Survival Widget | `frontend2/src/components/Dashboard/Survival.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py moat status` | Show coverage | `[x]` |
| `python cli.py moat set-target <months>` | Update goal | `[x]` |

---

*Last verified: 2026-01-25*
