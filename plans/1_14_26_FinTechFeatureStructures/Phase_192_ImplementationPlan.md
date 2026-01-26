# Phase 192: Advisor 'Career Risk' & Defensive Incentive Model

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: HR & Performance Team

---

## 📋 Overview

**Description**: Quantify "Career Risk" (Agency Risk). Investment Managers often herd into the same assets because "it's better to fail conventionally than succeed unconventionally." If they buy a popular stock and it drops, they keep their job. If they buy a contrarian stock and it drops, they get fired.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 12

---

## 🎯 Sub-Deliverables

### 192.1 Herding Behavior Detection (Active Share) `[ ]`

**Acceptance Criteria**: Calculate "Active Share". If a manager charges 1% fees but owns 95% of the S&P 500 components, they are a "Closet Indexer" avoiding career risk.

```python
class HerdingDetector:
    """
    Detect Closet Indexing.
    """
    def calculate_active_share(self, portfolio: Portfolio, benchmark: Index) -> float:
        # Sum of absolute differences in weights / 2
        # < 60% = Closet Indexer
        # > 80% = True Active
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Active Share Calc | `services/performance/active_share.py` | `[ ]` |

---

### 192.2 "Window Dressing" Pattern Recognition `[ ]`

**Acceptance Criteria**: Detect "Window Dressing". Managers buying winners just before Quarter End to show them on the client report ("See, we own Nvidia!"), masking that they didn't own it during the rally.

| Component | File Path | Status |
|-----------|-----------|--------|
| Window Dressing Check | `services/compliance/window_dressing.py` | `[ ]` |

---

### 192.3 Incentive Structure Alignment Score `[ ]`

**Acceptance Criteria**: Score the fee structure. AUM Fee = High Career Risk (Don't lose assets). Performance Fee = High Risk Taking (Swing for fences). 3-Year Rolling Bonus = Balanced.

| Component | File Path | Status |
|-----------|-----------|--------|
| Structure Scorer | `services/analysis/incentive_score.py` | `[ ]` |

---

### 192.4 Neo4j Advisor ↔ Peer Group Allocation `[ ]`

**Acceptance Criteria**: Graph comparison. Compare advisor's holdings to their peer group. High overlap = High Herding.

```cypher
(:ADVISOR {id: "A"})-[:ALLOCATES]->(:ASSET)
(:ADVISOR {id: "B"})-[:ALLOCATES]->(:ASSET)

// Jaccard Similarity of holdings
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Peer Graph Service | `services/neo4j/peer_graph.py` | `[ ]` |

---

### 192.5 Client Firing Threshold Simulator `[ ]`

**Acceptance Criteria**: Model the "Pain Point". How much underperformance (Duration and Magnitude) before a client fires the manager? Managers optimize to stay *just* above this line.

| Component | File Path | Status |
|-----------|-----------|--------|
| Firing Simulator | `services/simulation/client_retention.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Manager Assessment | `frontend2/src/components/Manager/SkillAssessment.jsx` | `[ ]` |
| Active Share Gauge | `frontend2/src/components/Charts/ActiveShare.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py manager check-herd` | Calc active share | `[ ]` |
| `python cli.py manager window-dress` | Audit quarter end | `[ ]` |

---

*Last verified: 2026-01-25*
