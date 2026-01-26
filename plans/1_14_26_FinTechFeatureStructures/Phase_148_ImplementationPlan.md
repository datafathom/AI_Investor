# Phase 148: Special Needs Trust & Benefit Preservation Logic

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Estate Planning Team

---

## 📋 Overview

**Description**: Manage Special Needs Trusts (SNT) to provide for beneficiaries with disabilities *without* disqualifying them from government benefits like SSI (Supplemental Security Income) and Medicaid. Strict rules prevent "Cash" distributions for food/shelter.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch VIII Phase 8

---

## 🎯 Sub-Deliverables

### 148.1 Non-Disqualifying Supplemental Payout Filter `[ ]`

**Acceptance Criteria**: Filter allow/deny on distributions. Direct payments for food/rent reduce SSI benefits. Payments to *vendors* for electronics, therapy, vacations are allowed.

```python
class SNTDistributionFilter:
    """
    Filter SNT distributions to preserve benefits.
    
    Allowed (Vendor Pay): Phone bill, Internet, Medical, Travel, Education.
    Problematic (Cash/In-Kind): Cash to beneficiary, Grocery gift cards, Rent payments (ISM reduction).
    """
    
    def validate_payment(
        self,
        payee_type: str,       # VENDOR or BENEFICIARY
        expense_category: str  # SHELTER, FOOD, MEDICAL, LIFESTYLE
    ) -> ValidationResult:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Distribution Filter | `services/estate/snt_filter.py` | `[ ]` |
| Vendor Payment Sys | `services/payment/vendor_direct.py` | `[ ]` |

---

### 148.2 Medicaid/Social Security Limit Schema `[ ]`

**Acceptance Criteria**: Store current asset/income limits for SSI/Medicaid qualification to ensure trust assets don't accidentally count against them.

| Component | File Path | Status |
|-----------|-----------|--------|
| Benefit Limits | `config/govt_benefits_limits.py` | `[ ]` |
| Qualification Check | `services/compliance/benefit_check.py` | `[ ]` |

---

### 148.3 Benefit Eligibility Threshold Gate `[ ]`

**Acceptance Criteria**: Automatic lock preventing any distribution that would push the beneficiary's personal checking account over the $2,000 resource limit.

| Component | File Path | Status |
|-----------|-----------|--------|
| Resource Monitor | `services/estate/resource_monitor.py` | `[ ]` |

---

### 148.4 Neo4j Special Needs Beneficiary Node `[ ]`

**Acceptance Criteria**: Flag beneficiaries in Neo4j as "Special Needs" to automatically enforce SNT logic on any inheritance they receive.

#### Neo4j Schema

```cypher
(:PERSON {
    name: "Beneficiary",
    is_special_needs: true,
    receives_ssi: true,
    receives_medicaid: true
})

// Inheritance redirection
(:ESTATE)-[:BEQUEATHS]->(:SPECIAL_NEEDS_TRUST)-[:BENEFITS]->(:PERSON)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| SNT Graph Service | `services/neo4j/snt_graph.py` | `[ ]` |

---

### 148.5 Distribution Risk Alert for Trustee `[ ]`

**Acceptance Criteria**: Alert the trustee if a requested distribution ("Rent Payment") will cause a reduction in the beneficiary's SSI check (ISM rule).

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Alert Service | `services/alerts/snt_risk.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Trustee Dashboard | `frontend2/src/components/Estate/TrusteeDashboard.jsx` | `[ ]` |
| Impact Warning | `frontend2/src/components/Alerts/BenefitImpact.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py snt validate <category>` | Check expense category | `[ ]` |
| `python cli.py snt check-limits` | Check resource limits | `[ ]` |

---

*Last verified: 2026-01-25*
