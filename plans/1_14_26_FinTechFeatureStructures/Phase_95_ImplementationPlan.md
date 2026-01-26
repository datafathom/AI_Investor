# Phase 95: Shipping & Logistics Early Warning System

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Alternative Data Team

---

## 📋 Overview

**Description**: Track goods moving. Baltic Dry Index (Raw materials), Container rates, Trucking tonnage. If trucking stops, the economy stops.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 95

---

## 🎯 Sub-Deliverables

### 95.1 Baltic Dry Index Monitor `[ ]`

**Acceptance Criteria**: Leading indicator for raw material demand.

| Component | File Path | Status |
|-----------|-----------|--------|
| BDI Mon | `services/market/baltic_dry.py` | `[ ]` |

---

### 95.2 Container Freight Rates (Shanghai-LA) `[ ]`

**Acceptance Criteria**: Track costs. High cost = Inflation. Low cost = Low Demand.

| Component | File Path | Status |
|-----------|-----------|--------|
| Freight Rates | `services/analysis/freight_cost.py` | `[ ]` |

---

### 95.3 Trucking Tonnage Index `[ ]`

**Acceptance Criteria**: ATA Tonnage Index. Domestic US health.

| Component | File Path | Status |
|-----------|-----------|--------|
| Trucking | `services/market/trucking_index.py` | `[ ]` |

---

### 95.4 Port Congestion Satellite Data `[ ]`

**Acceptance Criteria**: Count ships waiting at anchor (Long Beach/Rotterdam). Supply chain bottleneck indicator.

| Component | File Path | Status |
|-----------|-----------|--------|
| Port Sat | `services/ingestion/port_congestion.py` | `[ ]` |

### 95.5 FedEx/UPS Volume Proxy `[ ]`

**Acceptance Criteria**: Track volume guidance from major carriers.

| Component | File Path | Status |
|-----------|-----------|--------|
| Parcel Vol | `services/analysis/parcel_vol.py` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py ship prices` | Container rates | `[ ]` |
| `python cli.py ship congestion` | Ship queue count | `[ ]` |

---

*Last verified: 2026-01-25*
