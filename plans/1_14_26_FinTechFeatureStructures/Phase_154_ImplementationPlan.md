# Phase 154: Capital Gains Offsetting High-Speed Algorithm

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax & Trading Team

---

## 📋 Overview

**Description**: High-speed algorithm to optimize year-end tax harvesting. Specifically focuses on "Gain Offsetting" - realizing sufficient losses to neutralize recognized gains, effectively creating a 0% tax year for the portfolio turnover.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 14

---

## 🎯 Sub-Deliverables

### 154.1 Winner/Loser Matching Engine `[ ]`

**Acceptance Criteria**: Identify "Loser" lots that can be sold to offset "Winner" lots that were sold earlier in the year (or need to be sold for rebalancing).

#### Backend Implementation

```python
class LossHarvester:
    """
    Match Gains and Losses to minimize liability.
    
    Goal: Net Capital Gain = $0 (or -$3,000).
    """
    def find_offset_candidates(
        self,
        target_loss_amount: Decimal,
        portfolio: Portfolio
    ) -> list[TaxLot]:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Harvesting Engine | `services/tax/loss_harvester.py` | `[ ]` |
| Optimizer | `services/tax/offset_optimizer.py` | `[ ]` |

---

### 154.2 Short-Term vs. Short-Term Priority Function `[ ]`

**Acceptance Criteria**: Prioritize offsetting Short-Term Capital Gains (taxed at 37%+) with Short-Term Losses first, as this saves more money than offsetting Long-Term Gains (taxed at 20%).

| Component | File Path | Status |
|-----------|-----------|--------|
| ST Priority Logic | `services/tax/priority_logic.py` | `[ ]` |

---

### 154.3 Kafka End-of-Year Harvesting Notification `[ ]`

**Acceptance Criteria**: Trigger "Last Call" notifications in December for any remaining unrealized losses that could offset YTD gains.

| Component | File Path | Status |
|-----------|-----------|--------|
| EOY Trigger | `services/kafka/eoy_trigger.py` | `[ ]` |

---

### 154.4 Liquidity-Neutral Trade Recommender `[ ]`

**Acceptance Criteria**: Generate "Switch Trades" (Sell Coke / Buy Pepsi) to realize tax loss while staying fully invested in the market (Liquidity Neutral).

| Component | File Path | Status |
|-----------|-----------|--------|
| Switch Generator | `services/trading/switch_generator.py` | `[ ]` |

---

### 154.5 Capital Gains Bracket Simulator (15%/20%/23.8%) `[ ]`

**Acceptance Criteria**: Simulate the marginal tax impact of selling winners, including the 3.8% NIIT (Obamacare) tax for high earners.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bracket Sim | `services/tax/bracket_sim.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax offset-gains` | Find loss candidates | `[ ]` |
| `python cli.py tax simulate-year` | Project tax bill | `[ ]` |

---

*Last verified: 2026-01-25*
