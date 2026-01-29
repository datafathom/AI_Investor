# Phase 68: Derivatives Income Engine (Covered Calls)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading Team

---

## 📋 Overview

**Description**: Systematize the generation of income from existing holdings. Use Covered Calls to "Rent out" stocks. Target 15-30 delta calls to generate 0.5% - 1.0% monthly yield on top of stock appreciation.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 68

---

## 🎯 Sub-Deliverables

### 68.1 Covered Call Opportunity Scanner `[x]`

**Acceptance Criteria**: Scan portfolio for "Call-able" positions (Lots > 100 shares). Calculate potential premium at 30 Delta / 30 DTE.

```python
class CallScanner:
    def scan_opportunities(self, portfolio):
        # Filter for 100+ share lots
        # Fetch Option Chain
        # Return list of proposed contracts
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Scanner | `services/options/call_scanner.py` | `[x]` |

---

### 68.2 IV Rank Filter (>50%) `[x]`

**Acceptance Criteria**: Only sell calls when Implied Volatility (IV) is high (Price is expensive). If IV Rank < 20%, skipping is better (Don't sell cheap insurance).

| Component | File Path | Status |
|-----------|-----------|--------|
| IV Filter | `services/options/iv_filter.py` | `[x]` |

---

### 68.3 Assignment Risk Calculator `[x]`

**Acceptance Criteria**: Calculate the probability of shares getting called away. "There is a 20% chance you lose your AAPL shares."

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Calc | `services/analysis/assignment_risk.py` | `[x]` |

---

### 68.4 Yield Boost Dashboard `[x]`

**Acceptance Criteria**: Dashboard showing "Extra Income Generated" via Options. "You added +$500 to your dividends this month."

| Component | File Path | Status |
|-----------|-----------|--------|
| Dashboard | `frontend2/src/components/Options/IncomeDash.jsx` | `[x]` |

### 68.5 Auto-Roll Logic (Theta Harvesting) `[x]`

**Acceptance Criteria**: Logic to "Roll" the position. If the call is challenged, buy it back and sell the next month out at a higher strike to collect more credit.

| Component | File Path | Status |
|-----------|-----------|--------|
| Roll Logic | `services/strategies/roll_logic.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py opt scan` | List candidates | `[x]` |
| `python cli.py opt check-roll <id>` | Suggest defense | `[x]` |

---

*Last verified: 2026-01-25*
