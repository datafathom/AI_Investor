# Phase 91: Weather Data & Agri-Commodity Alpha

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Alternative Data Team

---

## 📋 Overview

**Description**: Ingest weather data (NOAA). Predict Agri-Commodity prices (Wheat, Corn, Coffee). "Drought in Brazil = Buy Coffee Futures."

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 91

---

## 🎯 Sub-Deliverables

### 91.1 NOAA/API Weather Ingestion `[x]`

**Acceptance Criteria**: Ingest weather forecast for key growing regions (US Midwest, Brazil, Ukraine).

| Component | File Path | Status |
|-----------|-----------|--------|
| Weather Ingest | `services/ingestion/noaa_feed.py` | `[x]` |

---

### 91.2 Crop Yield Forecast Model `[x]`

**Acceptance Criteria**: Model impact of precipitation/temp on yield. Historical regression.

| Component | File Path | Status |
|-----------|-----------|--------|
| Yield Model | `services/analysis/crop_yield.py` | `[x]` |

---

### 91.3 Commodity-Weather Correlation `[x]`

**Acceptance Criteria**: Neo4j map: `(:REGION {name: "Iowa"})-[:GROWS]->(:COMMODITY {name: "Corn"})`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Graph Map | `services/neo4j/agri_map.py` | `[x]` |

---

### 91.4 El Nino / La Nina Flag `[x]`

**Acceptance Criteria**: Global weather oscillation flag. Adjusts long-term forecasts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Oscillation | `services/analysis/el_nino.py` | `[x]` |

### 91.5 Live Weather Map Overlay `[x]`

**Acceptance Criteria**: Map UI showing drought severity index overlay on growing regions.

| Component | File Path | Status |
|-----------|-----------|--------|
| Weather overlay | `frontend2/src/components/Maps/WeatherAgri.jsx` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py weather check <region>` | Forecast | `[x]` |
| `python cli.py weather predict-corn` | Signal | `[x]` |

---

*Last verified: 2026-01-25*
