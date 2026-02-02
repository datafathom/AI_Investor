# Phase 142: Revocable vs. Irrevocable Control & Tax Gating

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax & Legal Team

---

## 📋 Overview

**Description**: Implement the critical logic distinguishing Revocable Living Trusts (RLT) from Irrevocable Trusts. This gate controls tax treatment (Grantor tax vs. Trust tax), asset protection status (available to creditors vs. protected), and modification rights.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 2

---

## 🎯 Sub-Deliverables

### 142.1 Revocable Trust Modification Flag `[x]`

**Acceptance Criteria**: System flag allowing full modification (add/remove assets, change beneficiaries) for Revocable Trusts, while locking these actions for Irrevocable Trusts without specific legal workflows.

#### Backend Implementation

```python
class TrustModificationGate:
    """
    Control modification rights based on trust type.
    
    Revocable:
    - Grantor has full control (invest, withdraw, amend).
    - Assets count toward Grantor's estate.
    
    Irrevocable:
    - Grantor surrenders control.
    - Assets removed from estate (Tax reduction).
    - Modifications require 'Decanting' or court order.
    """
    
    def can_modify(self, trust_id: UUID, user_id: UUID, action: str) -> bool:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Modification Gate | `services/legal/modification_gate.py` | `[x]` |
| Permission Check | `services/auth/trust_permission.py` | `[x]` |

---

### 142.2 Irrevocable Clawback Prevention Gate `[x]`

**Acceptance Criteria**: Strictly prevent "clawback" (taking assets back) from Irrevocable Trusts, which would invalidate their estate tax exclusion status.

| Component | File Path | Status |
|-----------|-----------|--------|
| Clawback Prevention | `services/compliance/clawback_preventer.py` | `[x]` |
| Audit Log | `services/audit/trust_access_log.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Locked Asset Badge | `frontend2/src/components/Badges/LockedAsset.jsx` | `[x]` |
| Operation Block Modal | `frontend2/src/components/Modals/OperationBlock.jsx` | `[x]` |

---

### 142.3 Estate Tax Exclusion Status Analyzer `[x]`

**Acceptance Criteria**: Analyze and track which assets are successfully excluded from the taxable estate based on Valid Irrevocable status.

| Component | File Path | Status |
|-----------|-----------|--------|
| Exclusion Analyzer | `services/tax/estate_exclusion.py` | `[x]` |
| Estate Value Calc | `services/tax/estate_value_calc.py` | `[x]` |

---

### 142.4 Asset Protection Score for Irrevocable `[x]`

**Acceptance Criteria**: Calculate a score (0-100) indicating how well-protected assets are from creditors based on trust structure and jurisdiction (e.g., Nevada Asset Protection Trust).

| Component | File Path | Status |
|-----------|-----------|--------|
| Protection Scorer | `services/risk/asset_protection_score.py` | `[x]` |
| Jurisdiction Evaluator | `services/legal/jurisdiction_eval.py` | `[x]` |

---

### 142.5 Postgres Probate Avoidance Status Trigger `[x]`

**Acceptance Criteria**: Track "funding status" of trusts. A trust only avoids probate if assets are actually titled in the trust's name. Trigger alerts for unfunded assets.

#### Postgres Schema

```sql
CREATE TABLE trust_funding_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trust_id UUID NOT NULL,
    asset_id UUID NOT NULL,
    
    -- Status
    is_titled_correctly BOOLEAN DEFAULT FALSE,
    titling_verification_date DATE,
    
    -- Risk
    probate_risk_level VARCHAR(20),        -- HIGH (Not funded), LOW (Funded)
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Funding Monitor | `services/estate/funding_monitor.py` | `[x]` |
| Probate Alert | `services/alerts/probate_risk.py` | `[x]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py trust check-funding` | Check funding status | `[x]` |
| `python cli.py trust estate-tax` | Calc estate tax exposure | `[x]` |

---

*Last verified: 2026-01-25*
