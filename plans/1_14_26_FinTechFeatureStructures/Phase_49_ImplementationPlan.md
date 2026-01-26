# Phase 49: Advanced Portfolio Performance Attribution (Brinson-Fachler UI)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Performance Team

---

## 📋 Overview

**Description**: Decompose portfolio returns against benchmarks to determine if performance is driven by skill (Alpha) or exposure (Beta). Did we beat the market because we picked good stocks (Selection Effect) or because we overweighted Tech (Allocation Effect)?

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 49

---

## 🎯 Sub-Deliverables

### 49.1 Brinson-Fachler Model Implementation `[ ]`

**Acceptance Criteria**: Implement the standard Brinson model.
`Active Return = Allocation Effect + Selection Effect + Interaction Effect`.

```python
class BrinsonModel:
    def calculate(self, portfolio, benchmark):
        # Allocation = Sum((Wp - Wb) * Rb)
        # Selection = Sum(Wb * (Rp - Rb))
        # Interaction = Sum((Wp - Wb) * (Rp - Rb))
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| BF Model | `services/analysis/brinson_model.py` | `[ ]` |

---

### 49.2 Sector Allocation Attribution Widgets `[ ]`

**Acceptance Criteria**: Implement Frontend Widgets showing effects per GICS sector. "You made money in Tech (Selection) but lost in Energy (Allocation)."

| Component | File Path | Status |
|-----------|-----------|--------|
| Sector Widget | `frontend2/src/components/Analysis/SectorAttrib.jsx` | `[ ]` |

---

### 49.3 Diverging Bar Charts (D3.js) `[ ]`

**Acceptance Criteria**: Utilize D3.js diverging bar charts with hex-scales interpolated for color-blind accessibility to show +/- contributions.

| Component | File Path | Status |
|-----------|-----------|--------|
| D3 Chart | `frontend2/src/components/Charts/DivergingBar.jsx` | `[ ]` |

---

### 49.4 Real-Time Benchmark Comparison `[ ]`

**Acceptance Criteria**: Support real-time comparison against S&P 500, Nasdaq, and Custom Index benchmarks (< 50ms hydration).

| Component | File Path | Status |
|-----------|-----------|--------|
| Benchmark Service | `services/market/benchmark_feed.py` | `[ ]` |

### 49.5 Interaction Effect Heatmap `[ ]`

**Acceptance Criteria**: Develop a Heatmap visualizing the combined impact of allocation and selection.

| Component | File Path | Status |
|-----------|-----------|--------|
| Heatmap | `frontend2/src/components/Charts/AttribHeatmap.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py attrib run` | Run Brinson model | `[ ]` |
| `python cli.py attrib sector <name>` | Drill down | `[ ]` |

---

*Last verified: 2026-01-25*
