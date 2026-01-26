# Phase 184: Global Exit Tax & Residency Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax & Legal Team

---

## 📋 Overview

**Description**: Manage the "Expatriation Tax" (Exit Tax) for clients renouncing US citizenship. Calculate the "Mark-to-Market" tax on all worldwide assets if Net Worth > $2M or Income > $190k.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 4

---

## 🎯 Sub-Deliverables

### 184.1 Exit Tax Service ($2M NW / $190k/yr threshold) `[ ]`

**Acceptance Criteria**: Logic to check "Covered Expatriate" status. If checks pass, trigger Exit Tax calculation.

```python
class ExpatriationTest:
    """
    Determine 'Covered Expatriate' status (IRC 877A).
    """
    def check_status(self, net_worth: Decimal, avg_tax_liability: Decimal) -> bool:
        test_1 = net_worth > 2_000_000
        test_2 = avg_tax_liability > 190_000 # Indexed for inflation
        return test_1 or test_2
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Status Checker | `services/tax/expat_status.py` | `[ ]` |
| Config | `config/tax_thresholds.py` | `[ ]` |

---

### 184.2 8-of-15 Years Residency Requirement Validator `[ ]`

**Acceptance Criteria**: Track "Long-Term Resident" status (Green Card Holders). If held for 8 of last 15 years, they are subject to Exit Tax too.

| Component | File Path | Status |
|-----------|-----------|--------|
| Residency Timer | `services/legal/residency_timer.py` | `[ ]` |

---

### 184.3 Postgres Global Exit Tax Rate Table (US 23.8%, France, Norway) `[ ]`

**Acceptance Criteria**: Database of exit taxes by country. It's not just the US; Norway, Canada, and others have departure taxes.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE exit_tax_rules (
    country_code VARCHAR(3) PRIMARY KEY,
    tax_name VARCHAR(100),
    rate DECIMAL(5, 4),
    threshold_amount DECIMAL(20, 2),
    treaty_relief_available BOOLEAN,
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/184_exit_tax.sql` | `[ ]` |

---

### 184.4 Unrealized Gains Mark-to-Market Assessor `[ ]`

**Acceptance Criteria**: The core calculation. Pretend all assets are sold on the day of expatriation. Calculate Capital Gains Tax on the phantom sale.

| Component | File Path | Status |
|-----------|-----------|--------|
| Phantom Sale Calc | `services/tax/phantom_sale.py` | `[ ]` |

---

### 184.5 2024 IRS Specified Threshold Validator `[ ]`

**Acceptance Criteria**: Auto-update thresholds ($866k exclusion amount for 2024) via API.

| Component | File Path | Status |
|-----------|-----------|--------|
| Threshold Updater | `services/external/irs_thresholds.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Renunciation Calculator | `frontend2/src/components/Tax/RenounceCalc.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py expat check-status` | Am I covered? | `[ ]` |
| `python cli.py expat calc-bill` | Estimate exit tax | `[ ]` |

---

*Last verified: 2026-01-25*
