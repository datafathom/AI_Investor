# Phase 50: Fixed Income & Yield Curve Visualization

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Frontend Team

---

## 📋 Overview

**Description**: Monitor the baseline "Cost of Money". Visualize the Yield Curve shifts (Steepening/Flattening) to protect capital preservation layers. If the curve inverts, recession risk rises.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 50

---

## 🎯 Sub-Deliverables

### 50.1 Bond Ladder Construction Interface `[ ]`

**Acceptance Criteria**: Implement a UI with draggable D3 bars for staggered maturity planning. Visual "Tetris" for bonds.

| Component | File Path | Status |
|-----------|-----------|--------|
| Ladder UI | `frontend2/src/components/Bonds/LadderBuilder.jsx` | `[ ]` |

---

### 50.2 Yield Curve Animation (Framer Motion) `[ ]`

**Acceptance Criteria**: Apply Framer Motion animations to visualize curve shifts over a rolling 12-month window. "Play" button to see the curve invert over time.

| Component | File Path | Status |
|-----------|-----------|--------|
| Curve Anim | `frontend2/src/components/Charts/CurveAnim.jsx` | `[ ]` |

---

### 50.3 Duration & Convexity Risk Gauges `[ ]`

**Acceptance Criteria**: Deploy gauges reflecting sensitivity to +/- 100bps rate shocks. High Duration = High Risk if rates rise.

| Component | File Path | Status |
|-----------|-----------|--------|
| Risk Gauges | `frontend2/src/components/Bonds/RiskGauges.jsx` | `[ ]` |

---

### 50.4 Kafka FRED Stream Integration `[ ]`

**Acceptance Criteria**: Integrate FRED API via Kafka topic `macro-fred-updates` with < 500ms lag monitoring.

| Component | File Path | Status |
|-----------|-----------|--------|
| Macro Stream | `services/ingestion/fred_stream.py` | `[ ]` |

---

### 50.5 Weighted Average Yield Display `[ ]`

**Acceptance Criteria**: Show the portfolio's aggregate yield ("Yield to Worst").

| Component | File Path | Status |
|-----------|-----------|--------|
| Yield Display | `frontend2/src/components/Bonds/YieldDisplay.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py curve animate` | Replay history | `[ ]` |
| `python cli.py bonds calc-dur` | Portfolio duration | `[ ]` |

---

*Last verified: 2026-01-25*
