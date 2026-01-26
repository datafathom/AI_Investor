# Phase 47: 401k Employer Match Maximizer

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Wealth Planning Team

---

## 📋 Overview

**Description**: Ensure the system captures all available 'Free Money' from institutional employer matching programs. Never leave match dollars on the table.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 47

---

## 🎯 Sub-Deliverables

### 47.1 Match Config Portal `[ ]`

**Acceptance Criteria**: Configuration portal for entering employer matching percentages (e.g., "50% match up to 6% of salary") and caps.

| Component | File Path | Status |
|-----------|-----------|--------|
| Config UI | `frontend2/src/components/Settings/EmployerMatch.jsx` | `[ ]` |

---

### 47.2 Contribution Optimizer `[ ]`

**Acceptance Criteria**: Verify that the 401k contribution schedule maximizes the capture. e.g., if match is per-pay-period, don't max out early in the year or you lose the match for later months ("True-Up" risk).

```python
class ContributionScheduler:
    def optimize_schedule(self, salary, match_rule, pay_periods):
        # Calculate amount per period to ensure full match
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Optimizer | `services/planning/match_optimizer.py` | `[ ]` |

---

### 47.3 Missed Match Alert `[ ]`

**Acceptance Criteria**: Alert the Warden if projected contributions for the year fall below the threshold to get the full match.

| Component | File Path | Status |
|-----------|-----------|--------|
| Missed Match | `services/alerts/missed_match.py` | `[ ]` |

---

### 47.4 Match ROI Calculator `[ ]`

**Acceptance Criteria**: Calculate the annual ROI of the match. (e.g., 50% instant return on the first 6%). Needs to be shown in Total Return.

| Component | File Path | Status |
|-----------|-----------|--------|
| ROI Calc | `services/analysis/match_roi.py` | `[ ]` |

### 47.5 Postgres Contribution Schedule Storage `[ ]`

**Acceptance Criteria**: Store contribution schedules in the entity management tables in Postgres.

| Component | File Path | Status |
|-----------|-----------|--------|
| Schedule Db | `services/storage/contrib_schedule.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py match optimize` | Get schedule | `[ ]` |
| `python cli.py match status` | Show captured % | `[ ]` |

---

*Last verified: 2026-01-25*
