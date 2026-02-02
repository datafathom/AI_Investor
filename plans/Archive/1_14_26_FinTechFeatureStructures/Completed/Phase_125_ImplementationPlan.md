# Phase 125: REIT 85-90% Payout & FCF Monitor

> **Status**: `[x]` Completed | **Owner**: Real Estate Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 5

## 📋 Overview
**Description**: Monitor REIT distribution requirements (85-90% payout) and Free Cash Flow coverage to assess dividend sustainability.

---

## 🎯 Sub-Deliverables

### 125.1 Net Earnings/Dividend Payout Kafka Consumer `[x]`

```json
{
    "topic": "reit-payout-metrics",
    "schema": {
        "reit_id": "uuid",
        "ticker": "string",
        "ffo": "decimal",              // Funds From Operations
        "affo": "decimal",             // Adjusted FFO
        "dividend_paid": "decimal",
        "payout_ratio": "decimal",
        "coverage_ratio": "decimal",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Payout Consumer | `services/kafka/reit_payout_consumer.py` | `[x]` |
| FFO Calculator | `services/reits/ffo_calculator.py` | `[x]` |

### 125.2 85-90% Payout Rule Validator `[x]`
Validate REITs meet IRS distribution requirements.

| Component | File Path | Status |
|-----------|-----------|--------|
| Payout Validator | `services/reits/payout_validator.py` | `[x]` |

### 125.3 Multiple-to-Dividend/FCF Valuation Logic `[x]`
Value REITs based on FFO multiples rather than P/E.

| Component | File Path | Status |
|-----------|-----------|--------|
| FFO Valuator | `services/reits/ffo_valuator.py` | `[x]` |

### 125.4 Cash Holding Violation Alert `[x]`
Alert when REITs hold excessive cash (potential loss of REIT status).

### 125.5 Dividend Yield Tracking by Sector `[x]`
Track and compare yields across REIT sectors.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sector Yield Tracker | `services/reits/sector_yield_tracker.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED
