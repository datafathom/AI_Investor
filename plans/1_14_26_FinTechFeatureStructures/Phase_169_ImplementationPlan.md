# Phase 169: SFO Privacy & Secrecy Obfuscation Layer

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Security Team

---

## 📋 Overview

**Description**: Implement expert-level privacy features for Single Family Offices (SFOs). Wealthy families often require "Stealth Wealth" – obscuring ownership via LLCs, preventing data sharing, and compartmentalizing access for staff (e.g., the Nanny's payroll admin shouldn't see potential kidnapping-risk data like Net Worth).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 9

---

## 🎯 Sub-Deliverables

### 169.1 Lack of Transparency API Sharing Block `[ ]`

**Acceptance Criteria**: "Black Hole" mode. Block all external API sharing (Mint, Plaid aggregation) for SFO accounts to prevent data aggregation by third parties.

| Component | File Path | Status |
|-----------|-----------|--------|
| API Blocker | `services/security/api_blocker.py` | `[ ]` |
| Data Policy Config | `config/security/data_sharing.json` | `[ ]` |

---

### 169.2 Paper Trail Obfuscation (Non-Custodian Assets) `[ ]`

**Acceptance Criteria**: Allow "Manual Entry" or "Private Ledger" assets that do not sync with custodians, keeping them off the grid of electronic discovery systems where legally permissible.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE dark_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sfo_id UUID NOT NULL,
    asset_name VARCHAR(255),           -- "Project X"
    estimated_value DECIMAL(20, 2),
    
    -- Security
    is_encrypted BOOLEAN DEFAULT TRUE,
    encryption_key_id UUID,            -- Hardware token ID
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/169_dark_assets.sql` | `[ ]` |
| Dark Asset Service | `services/sfo/dark_asset_service.py` | `[ ]` |

---

### 169.3 Postgres Personal Record Vault (Family-Only) `[ ]`

**Acceptance Criteria**: Encrypted vault for sensitive docs (Passports, Wills, Medical Records) accessible *only* by Family Members, hidden from Staff.

| Component | File Path | Status |
|-----------|-----------|--------|
| Vault Service | `services/security/vault_service.py` | `[ ]` |
| Encryption Wrapper | `services/security/encryption.py` | `[ ]` |

---

### 169.4 Neo4j In-House Manager Independence Node `[ ]`

**Acceptance Criteria**: Map "In-House" managers vs "External". In-house (employees) have strict NDAs and privacy controls logged in the graph.

```cypher
(:STAFF {name: "In-House Counsel"})-[:SIGNED_NDA {
    level: "TOP_SECRET",
    expiry: date("2099-01-01")
}]->(:FAMILY_OFFICE)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| NDA Graph Service | `services/neo4j/nda_graph.py` | `[ ]` |

---

### 169.5 SFO vs. MFO Privacy Advantage Score `[ ]`

**Acceptance Criteria**: Score comparing the privacy of SFO (100% control, no data leaks) vs. MFO (Shared infrastructure, theoretical leak risk).

| Component | File Path | Status |
|-----------|-----------|--------|
| Privacy Scorer | `services/analysis/privacy_score.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Privacy Dashboard | `frontend2/src/components/SFO/PrivacyDash.jsx` | `[ ]` |
| Access Control Matrix | `frontend2/src/components/Admin/AccessMatrix.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sfo lockdown` | Enable full privacy mode | `[ ]` |
| `python cli.py sfo audit-access` | Show who viewed what | `[ ]` |

---

*Last verified: 2026-01-25*
