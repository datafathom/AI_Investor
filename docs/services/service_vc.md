# Backend Service: VC (The Deal Flow)

## Overview
The **VC Service** provides venture capital investment analysis tools, including deal scoring and contrarian opportunity detection.

## Core Components

### 1. Tier 1 Scorer (`tier1_scorer.py`)
- Scores deals based on team quality, market size, and traction.

### 2. Deal Aggregator (`deal_aggregator.py`)
- Aggregates deal flow from multiple syndicate sources.

### 3. Contrarian Detector (`contrarian_detector.py`)
- Identifies overlooked opportunities in unpopular sectors.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **VC Dashboard** | Deal Pipeline | `deal_aggregator` | **Missing** |
