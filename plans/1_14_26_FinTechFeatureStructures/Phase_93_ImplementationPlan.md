# Phase 93: Labor Market & Wage Inflation Tracker

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Macro Strategy Team

---

## 📋 Overview

**Description**: Track Jobs, Wages, and Claims. "Wage-Price Spiral" risk. If wages rise, inflation sticks. If unemployment spikes, recession is here.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 93

---

## 🎯 Sub-Deliverables

### 93.1 NFP/Unemployment Rate Stream `[ ]`

**Acceptance Criteria**: Ingest BLS data (Non-Farm Payrolls). Zero lag.

| Component | File Path | Status |
|-----------|-----------|--------|
| BLS Stream | `services/ingestion/bls_jobs.py` | `[ ]` |

---

### 93.2 Wage Growth Spiral Detector `[ ]`

**Acceptance Criteria**: Monitor Average Hourly Earnings (AHE). If > 4% YoY, Inflation is sticky.

| Component | File Path | Status |
|-----------|-----------|--------|
| Wage Monitor | `services/analysis/wage_spiral.py` | `[ ]` |

---

### 93.3 Job Openings (JOLTS) Quits Rate `[ ]`

**Acceptance Criteria**: "The Great Resignation". High Quits = Confident Workers = Inflation. Low Quits = Fear.

| Component | File Path | Status |
|-----------|-----------|--------|
| JOLTS Mon | `services/analysis/jolts_data.py` | `[ ]` |

---

### 93.4 Indeed/LinkedIn Hiring Strength `[ ]`

**Acceptance Criteria**: Scrape job postings count. "Tech hiring is down 20%".

| Component | File Path | Status |
|-----------|-----------|--------|
| Job Board Scraper | `services/ingestion/job_boards.py` | `[ ]` |

### 93.5 Initial Jobless Claims Visualizer `[ ]`

**Acceptance Criteria**: Weekly claims chart. The leading indicator of recession.

| Component | File Path | Status |
|-----------|-----------|--------|
| Claims Viz | `frontend2/src/components/Macro/Claims.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py labor status` | Show NFP | `[ ]` |
| `python cli.py labor check-wage` | Inflation risk | `[ ]` |

---

*Last verified: 2026-01-25*
