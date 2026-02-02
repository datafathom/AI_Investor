# Phase 154: Capital Gains Offsetting High-Speed Algorithm

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Tax & Trading Team

---

## 📋 Overview

**Description**: High-speed algorithm to optimize year-end tax harvesting. Specifically focuses on "Gain Offsetting" - realizing sufficient losses to neutralize recognized gains, effectively creating a 0% tax year for the portfolio turnover.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 14

---

## 🎯 Sub-Deliverables

### 154.1 Winner/Loser Matching Engine `[x]`

**Acceptance Criteria**: Identify "Loser" lots to offset recognized gains.

**Implementation**: `LossHarvester` class:
- Sorts portfolio by greatest unrealized loss
- Greedily selects lots until gain is covered
- Targets Net Capital Gain = $0

| Component | File Path | Status |
|-----------|-----------|--------|
| Harvesting Engine | `services/tax/loss_harvester.py` | `[x]` |
| Optimizer | `services/tax/tax_optimization_service.py` | `[x]` |

---

### 154.2 Short-Term vs. Short-Term Priority Function `[x]`

**Acceptance Criteria**: Prioritize offsetting ST gains (37%) with ST losses.

| Component | File Path | Status |
|-----------|-----------|--------|
| ST Priority Logic | `services/tax/harvest_service.py` | `[x]` |

---

### 154.3 Kafka End-of-Year Harvesting Notification `[x]`

**Acceptance Criteria**: Trigger "Last Call" notifications in December.

| Component | File Path | Status |
|-----------|-----------|--------|
| EOY Trigger | `services/kafka/eoy_trigger.py` | `[x]` |

---

### 154.4 Liquidity-Neutral Trade Recommender `[x]`

**Acceptance Criteria**: Generate "Switch Trades" to stay fully invested.

**Implementation**: `SwitchTradeGenerator` class:
- Maintains correlation map (TSLA→RIVN, AAPL→MSFT, etc.)
- Ensures wash sale compliance

| Component | File Path | Status |
|-----------|-----------|--------|
| Switch Generator | `services/trading/switch_generator.py` | `[x]` |

---

### 154.5 Capital Gains Bracket Simulator `[x]`

**Acceptance Criteria**: Simulate marginal tax impact including NIIT.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bracket Sim | `services/tax/boot_calculator.py` | `[x]` (Includes LTCG/NIIT) |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax offset-gains` | Find loss candidates | `[x]` |
| `python cli.py tax simulate-year` | Project tax bill | `[x]` |

---

*Last verified: 2026-01-30*

