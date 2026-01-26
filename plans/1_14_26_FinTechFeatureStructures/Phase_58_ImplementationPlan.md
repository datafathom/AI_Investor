# Phase 58: Estate Planning & Inheritance Protocol Wizard

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Legal & Tech Team

---

## 📋 Overview

**Description**: Extend the life of the financial ecosystem beyond the primary warden via succession logic and the "Dead Man's Switch". If I die, does the AI know who gets the keys?

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 58

---

## 🎯 Sub-Deliverables

### 58.1 Dead Man's Switch Heartbeat `[ ]`

**Acceptance Criteria**: Implement the 'Time to Trigger' countdown visualizer. User must login every 30/90 days or a "Check In" email is sent. If no response -> Trigger Protocol.

| Component | File Path | Status |
|-----------|-----------|--------|
| Heartbeat Service | `services/security/heartbeat.py` | `[ ]` |

---

### 58.2 Beneficiary Allocation Tree `[ ]`

**Acceptance Criteria**: Develop a Beneficiary Asset Allocation Tree with drag-and-drop percentage balance checking. "Wife: 50%, Kids: 25% each".

| Component | File Path | Status |
|-----------|-----------|--------|
| Tree UI | `frontend2/src/components/Estate/BeneficiaryTree.jsx` | `[ ]` |

---

### 58.3 Trust Structure Graph (Neo4j) `[ ]`

**Acceptance Criteria**: Configure the Trust/Entity Legal Structure Visualizer in Neo4j. `(USER)-[:GRANTOR_OF]->(TRUST)-[:BENEFICIARY]->(CHILD)`.

```cypher
(:TRUST {name: "Dynasty Trust"})-[:PROTECTS]->(:ASSET {symbol: "AAPL"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Trust Graph | `services/neo4j/trust_structure.py` | `[ ]` |

---

### 58.4 Multi-Sig Key Reveal Protocol `[ ]`

**Acceptance Criteria**: Verify multi-sig encryption of beneficiary private keys (Shamir's Secret Sharing). Keys are revealed *only* upon switch activation.

| Component | File Path | Status |
|-----------|-----------|--------|
| Key Sharding | `services/crypto/shamir_secret.py` | `[ ]` |

### 58.5 Estate Tax Simulator `[ ]`

**Acceptance Criteria**: Simulate the estate tax impact ($13.6M exemption). Calcluate "Death Tax" liability based on current net worth.

| Component | File Path | Status |
|-----------|-----------|--------|
| Tax Sim | `services/tax/estate_tax.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py estate check-in` | Reset heartbeat | `[ ]` |
| `python cli.py estate trigger-test` | Sim death protocol | `[ ]` |

---

*Last verified: 2026-01-25*
