# Phase 52: Tax-Advantaged Strategy & Harvesting UI

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Tax Team

---

## 📋 Overview

**Description**: Automate the execution of tax-alpha opportunities. The UI for "Tax Loss Harvesting". User reviews suggestions and clicks "Execute" to swap assets and book the loss.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 52

---

## 🎯 Sub-Deliverables

### 52.1 Unrealized Loss Identification Grid `[ ]`

**Acceptance Criteria**: Deploy a grid UI sorting positions by "Harvestable Loss". Query Postgres for 30-day buy-side history (Wash-Sale Protection).

| Component | File Path | Status |
|-----------|-----------|--------|
| Loss Grid | `frontend2/src/components/Tax/HarvestGrid.jsx` | `[ ]` |

---

### 52.2 Automated Harvesting Toggle (OAuth Bio) `[ ]`

**Acceptance Criteria**: Implement a global 'Automated Harvesting Toggle' requiring secondary OAuth 2.0 biometric confirmation (High Security Action).

| Component | File Path | Status |
|-----------|-----------|--------|
| Secure Toggle | `frontend2/src/components/Settings/SecureToggle.jsx` | `[ ]` |

---

### 52.3 Capital Gains Countdown (Short vs Long) `[ ]`

**Acceptance Criteria**: Develop a visual countdown for assets approaching 'Long-Term' status (365 days). "Hold for 12 more days to save 15% tax."

| Component | File Path | Status |
|-----------|-----------|--------|
| Countdown | `frontend2/src/components/Tax/TermCountdown.jsx` | `[ ]` |

---

### 52.4 Tax Savings Alpha Display `[ ]`

**Acceptance Criteria**: Calculate 'Tax Savings Alpha' per position based on marginal tax rate presets. Show "You saved $450" next to the execute button.

| Component | File Path | Status |
|-----------|-----------|--------|
| Alpha Calc | `services/analysis/tax_alpha_display.py` | `[ ]` |

---

### 52.5 CPA Export (CSV) `[ ]`

**Acceptance Criteria**: Export IRS-compliant CSV files (8949 format) formatted for direct CPA ingestion/TurboTax with SHA-256 integrity hashes.

| Component | File Path | Status |
|-----------|-----------|--------|
| Exporter | `services/reporting/cpa_export.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py tax export-csv` | Gen report | `[ ]` |
| `python cli.py tax auto-harvest` | Run batch (if enabled) | `[ ]` |

---

*Last verified: 2026-01-25*
