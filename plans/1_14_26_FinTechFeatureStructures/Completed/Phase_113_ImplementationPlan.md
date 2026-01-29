# Phase 113: Russell 2000 'English Football Pyramid' Logic

> **Status**: `[x]` Completed | **Owner**: Quantitative Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Phase 13

## 📋 Overview
**Description**: Model the Russell 2000 reconstitution dynamics as an "English Football Pyramid" where companies are promoted/relegated between indices, addressing negative selection bias in small-cap indices.

---

## 🎯 Sub-Deliverables

### 113.1 Neo4j Promotion/Demotion State Machine `[x]`
```cypher
(:COMPANY)-[:PROMOTED_TO {date: date(), from_index: "Russell 2000"}]->(:INDEX:RUSSELL_1000)
(:COMPANY)-[:RELEGATED_FROM {date: date(), to_index: "Russell 2000"}]->(:INDEX:RUSSELL_1000)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| State Machine Service | `services/neo4j/index_state_machine.py` | `[x]` |
| Reconstitution Tracker | `services/market/reconstitution_tracker.py` | `[x]` |

### 113.2 Negative Selection Bias Filter `[x]`
**Acceptance Criteria**: Filter and flag companies negatively selected into small-cap indices after outgrowing success.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bias Filter | `services/analysis/negative_selection_filter.py` | `[x]` |
| Quality Scorer | `services/analysis/quality_scorer.py` | `[x]` |

### 113.3 Postgres Laggard Stock Entry Log `[x]`
Track stocks entering indices due to poor performance from larger indices.

### 113.4 Equal vs. Cap Weighted Comparison Engine `[x]`
Compare equal-weighted vs. cap-weighted performance to highlight concentration effects.

| Component | File Path | Status |
|-----------|-----------|--------|
| Weighting Comparator | `services/quantitative/weighting_comparator.py` | `[x]` |

### 113.5 Asset Class Agnostic Recommendation Engine `[x]`
Recommend optimal index exposure based on market conditions without bias.

---

## 📊 Phase Status: `[ ]` NOT STARTED
