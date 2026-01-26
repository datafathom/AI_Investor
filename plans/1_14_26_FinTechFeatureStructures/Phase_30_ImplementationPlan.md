# Phase 30: Asset 'Starvation' Prevention Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Risk Management Team

---

## 📋 Overview

**Description**: Monitor and prevent margin call events. "Starvation" occurs when an asset (or account) runs out of maintenance margin. The system must act *before* the broker liquidates the position at a bad price.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 30

---

## 🎯 Sub-Deliverables

### 30.1 Real-Time 'Distance to Liquidation' Calc `[ ]`

**Acceptance Criteria**: Calculate "Distance to Liquidate" (%) for the top 5 largest positions every 10 seconds.
Formula: `(CurrentPrice - LiqPrice) / CurrentPrice`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Margin Calc | `services/risk/margin_calc.py` | `[ ]` |

---

### 30.2 'Red Pulse' Danger Zone Alert `[ ]`

**Acceptance Criteria**: Trigger a 'Red Pulse' visual alert in the Warden console when the total margin buffer drops below 15.0%.

| Component | File Path | Status |
|-----------|-----------|--------|
| Alert Service | `services/alerts/margin_alert.py` | `[ ]` |
| Frontend Pulse | `frontend2/src/components/Warden/RedPulse.jsx` | `[ ]` |

---

### 30.3 Prioritized De-leveraging Sequence `[ ]`

**Acceptance Criteria**: Configure a prioritized list for the ProtectorAgent. If margin is breached, which asset goes first? (Usually lowest conviction or highest volatility).

```python
class DeleverageSequencer:
    def get_kill_list(self, positions: list[Position]) -> list[Position]:
        # Sort by: 1. Volatility (High first), 2. PnL (Losers first)
        return sorted(positions, key=lambda p: (p.vol, -p.pnl), reverse=True)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sequencer | `services/risk/deleverage.py` | `[ ]` |

---

### 30.4 Margin Check Audit Log `[ ]`

**Acceptance Criteria**: Audit every margin-check event and store the results in the Postgres security log to prove the system was watching.

| Component | File Path | Status |
|-----------|-----------|--------|
| Audit Log | `services/logging/margin_audit.py` | `[ ]` |

---

### 30.5 Margin Stress Simulator `[ ]`

**Acceptance Criteria**: Tool to simulate: "If SPY drops 5%, what happens to my margin?".

| Component | File Path | Status |
|-----------|-----------|--------|
| Simulator | `services/simulation/margin_stress.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py margin check` | Current margin % | `[ ]` |
| `python cli.py margin simulate <drop_pct>` | Stress test | `[ ]` |

---

*Last verified: 2026-01-25*
