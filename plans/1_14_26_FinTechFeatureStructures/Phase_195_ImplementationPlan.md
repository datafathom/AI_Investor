# Phase 195: The 'Great Taking' & Security Entitlement Ledger

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Legal & Risk Team

---

## 📋 Overview

**Description**: Address the "Security Entitlement" risk (UCC Article 8). In a systemic collapse, shares held at a broker are legally "general unsecured claims". This phase implements a "Direct Registration System" (DRS) conduit to move shares from "Street Name" (Cede & Co) to the client's own name on the issuer's books (Transfer Agent).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 15

---

## 🎯 Sub-Deliverables

### 195.1 Indirect-Holding Risk Analyzer (UCC Article 8) `[ ]`

**Acceptance Criteria**: Analyze custodian risk. Is the custodian re-hypothecating assets? What is their credit rating?

```python
class CustodianRiskAssessor:
    """
    Evaluate counterparty risk of custodians.
    """
    def assess_risk(self, custodian: str) -> RiskReport:
        cds_spread = self.market.get_cds_spread(custodian)
        rehypothecation_limit = self.legal.get_rehypothecation_limit(custodian)
        
        return RiskReport(
            default_probability=cds_spread.implied_prob,
            asset_segregation_status="MIXED"
        )
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Assessor | `services/risk/custodian_risk.py` | `[ ]` |

---

### 195.2 Direct Registration System (DRS) Conduit `[ ]`

**Acceptance Criteria**: Automated workflow to DRS shares (e.g., move GME from Fidelity to Computershare).

| Component | File Path | Status |
|-----------|-----------|--------|
| DRS Manager | `services/custody/drs_manager.py` | `[ ]` |

---

### 195.3 "Not Your Keys, Not Your Coins" Crypto Custody `[ ]`

**Acceptance Criteria**: Apply the same logic to Crypto. Flag assets on centralized exchanges (Coinbase) as "At Broker Risk". Verify Cold Storage addresses.

| Component | File Path | Status |
|-----------|-----------|--------|
| Crypto Custody | `services/crypto/custody_verifier.py` | `[ ]` |

---

### 195.4 Client Asset Segregation Auditor `[ ]`

**Acceptance Criteria**: Verify "Fully Paid Lending" settings. Ensure client assets are NOT being lent out to short sellers without implicit consent.

| Component | File Path | Status |
|-----------|-----------|--------|
| Segregation Auditor | `services/compliance/segregation_audit.py` | `[ ]` |

---

### 195.5 "Street Name" vs. "Beneficial Owner" Visualizer `[ ]`

**Acceptance Criteria**: UI showing the legal chain of title. Client -> Broker -> DTCC -> Cede & Co.

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Ownership Chain | `frontend2/src/components/Legal/OwnershipChain.jsx` | `[ ]` |
| DRS Status | `frontend2/src/components/Custody/DRSStatus.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py custody check-risk` | Audit broker risk | `[ ]` |
| `python cli.py custody init-drs` | Start transfer | `[ ]` |

---

*Last verified: 2026-01-25*
