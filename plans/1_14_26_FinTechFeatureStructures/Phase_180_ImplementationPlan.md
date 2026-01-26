# Phase 180: Transition to Advanced Global Risk & Geopolitics

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Core Architecture Team

---

## 📋 Overview

**Description**: Bridge Epoch IX (UHNW) to Epoch X (Global Risk). As wealthy families diversify globally, they face new risks: Geopolitics, FATCA, Currency Wars, and Systemic Fragility. This phase prepares the data layer for global macro analysis.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 20

---

## 🎯 Sub-Deliverables

### 180.1 UHNW Dashboard → Global Risk Link `[ ]`

**Acceptance Criteria**: Expand the UHNW dashboard to include a "Global Risk Map". Click on a country to see exposure (Assets, Currency, Legal Risk).

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Aggregator | `services/reporting/global_risk_agg.py` | `[ ]` |
| Geo API | `web/api/risk/geo_exposure.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Global Map View | `frontend2/src/components/Maps/GlobalRiskMap.jsx` | `[ ]` |

---

### 180.2 Kafka Bridge to Phase 181 (Volatility) `[ ]`

**Acceptance Criteria**: Establish Kafka topics for macro events. "War Declared", "Currency Devaluation", "Sanctions Imposed".

#### Kafka Topic

```json
{
    "topic": "global-macro-events",
    "schema": {
        "event_type": "GEOPOLITICAL",
        "country": "CN",
        "severity": "HIGH",
        "description": "Port blockade initiated",
        "timestamp": "timestamp"
    }
}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Macro Event Producer | `services/kafka/macro_producer.py` | `[ ]` |

---

### 180.3 Unified "Total Wealth" + "Total Risk" View `[ ]`

**Acceptance Criteria**: The ultimate view. Wealth (Assets - Liabilities) overlayed with Risk (VaR, tail risk).

| Component | File Path | Status |
|-----------|-----------|--------|
| Unified View Service | `services/reporting/unified_view.py` | `[ ]` |

---

### 180.4 Multi-Currency Ledger Prep `[ ]`

**Acceptance Criteria**: Ensure all ledgers can handle multi-currency. Store values in "Local Currency" and "Reporting Currency" (USD).

| Component | File Path | Status |
|-----------|-----------|--------|
| FX Converter | `services/finance/fx_converter.py` | `[ ]` |
| Ledger Update | `migrations/180_multi_currency_prep.sql` | `[ ]` |

---

### 180.5 Completion Audit for Epoch IX `[ ]`

**Acceptance Criteria**: Automated audit. Verify all Epoch IX systems (SFO, PE, VC, PPLI) are online and integrated.

| Component | File Path | Status |
|-----------|-----------|--------|
| Audit Script | `scripts/audits/epoch_ix_audit.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py bridge global-status` | Check Epoch X readiness | `[ ]` |
| `python cli.py bridge audit-epoch-ix` | Run full completion audit | `[ ]` |

---

*Last verified: 2026-01-25*
