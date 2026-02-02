# Phase 184: Global Exit Tax & Residency Logic

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Tax & Legal Team

---

## 📋 Overview

**Description**: Expatriation Tax (Exit Tax) management for UHNW transitions.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 4

---

## 🎯 Sub-Deliverables

### 184.1 Exit Tax Service ($2M NW / $190k/yr threshold) `[x]`

**Acceptance Criteria**: Check Covered Expatriate status (IRC 877A).

| Component | File Path | Status |
|-----------|-----------|--------|
| Status Checker | `services/tax/exit_tax_service.py` | `[x]` |
| Config | `config/tax_thresholds.py` | `[x]` |

---

### 184.2 8-of-15 Years Residency Requirement Validator `[x]`

**Acceptance Criteria**: Track long-term residency.

| Component | File Path | Status |
|-----------|-----------|--------|
| Residency Timer | `services/legal/residency_timer.py` | `[x]` |

---

### 184.3 Postgres Global Exit Tax Rate Table `[x]`

**Acceptance Criteria**: Database of exit taxes (US, Norway, etc).

| Component | File Path | Status |
|-----------|-----------|--------|
| DB Table | `services/tax/exit_tax_service.py` | `[x]` |

---

### 184.4 Unrealized Gains Mark-to-Market Assessor `[x]`

**Acceptance Criteria**: Phantom sale calculation.

| Component | File Path | Status |
|-----------|-----------|--------|
| Phantom Sale Calc | `services/tax/exit_tax_service.py` | `[x]` |

---

### 184.5 2024 IRS Specified Threshold Validator `[x]`

**Acceptance Criteria**: 2024 inflation-adjusted thresholds.

| Component | File Path | Status |
|-----------|-----------|--------|
| Threshold Updater | `services/tax/exit_tax_service.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py expat check-status` | Am I covered? | `[x]` |
| `python cli.py expat calc-bill` | Estimate exit tax | `[x]` |

---

*Last verified: 2026-01-30*

