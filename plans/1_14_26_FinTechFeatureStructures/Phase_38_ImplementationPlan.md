# Phase 38: 401k/IRA Tax-Wrapper Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Wealth Planning Team

---

## 📋 Overview

**Description**: Implement management logic for tax-advantaged accounts (Traditional IRA, Roth IRA, 401k) to optimize long-term wealth preservation. Understanding "Asset Location" (bonds in IRA, stocks in Roth) is key.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 38

---

## 🎯 Sub-Deliverables

### 38.1 Traditional vs. Roth Simulator `[ ]`

**Acceptance Criteria**: Configure logic for Traditional vs. Roth IRA tax-deferred growth simulations. Input: Current Tax Rate vs Projected Retirement Tax Rate.

```python
class TaxSimulator:
    def compare(self, contribution: float, years: int, return_rate: float, current_tax: float, future_tax: float):
        # Calc Traditional (Pre-tax growth, taxed at exit)
        # Calc Roth (Post-tax entry, tax-free exit)
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Sim | `services/planning/tax_sim.py` | `[ ]` |

---

### 38.2 IRS Contribution Limiter (2024/2025) `[ ]`

**Acceptance Criteria**: Implement automated contribution limiters. e.g., $7,000 for IRA, $23,000 for 401k. Prevent "Over-contribution" alerts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Limit Checker | `services/compliance/irs_limits.py` | `[ ]` |

---

### 38.3 Employer Match Tracker `[ ]`

**Acceptance Criteria**: Verify tracking of employer matching contributions within the 401k integration module. This is 100% ROI.

| Component | File Path | Status |
|-----------|-----------|--------|
| Match Tracker | `services/planning/match_tracker.py` | `[ ]` |

---

### 38.4 Backdoor Roth Feasibility Checker `[ ]`

**Acceptance Criteria**: Logic to check if user exceeds income phase-out limits ($146k single) and suggest "Backdoor Roth" conversion workflow.

| Component | File Path | Status |
|-----------|-----------|--------|
| Backdoor Logic | `services/planning/backdoor_roth.py` | `[ ]` |

---

### 38.5 Postgres Entity Management Schema `[ ]`

**Acceptance Criteria**: Persist all tax-wrapper metadata in Postgres.

#### Postgres Schema

```sql
CREATE TABLE tax_wrappers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    type VARCHAR(20), -- IRA_ROTH, IRA_TRAD, 401K
    custodian VARCHAR(50),
    ytd_contribution DECIMAL(12, 2),
    employer_match_ytd DECIMAL(12, 2),
    
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/38_tax_wrappers.sql` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax check-limit` | Show remaining contrib | `[ ]` |
| `python cli.py tax sim-roth` | Run comparison | `[ ]` |

---

*Last verified: 2026-01-25*
