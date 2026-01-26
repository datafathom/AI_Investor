# Phase 26: Stop Loss Distance Optimizer

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Automate the placement of stop-loss orders based on logic-based market structure (Swing Lows) and ATR-adjusted volatility. No more arbitrary "20 pip stops". The market structure dictates the stop, and the Position Size Calculator regulates the risk.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 26

---

## 🎯 Sub-Deliverables

### 26.1 'Smart Money' Structural Level Finder `[ ]`

**Acceptance Criteria**: Algorithm to find the nearest valid Swing Low (for Longs) or Swing High (for Shorts) within a reasonable timeframe (e.g., last 20 candles).

```python
class StructureScanner:
    def find_stop_level(self, direction: str, candles: list[Candle]) -> float:
        if direction == 'LONG':
            return self.find_recent_swing_low(candles)
        else:
            return self.find_recent_swing_high(candles)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Structure Scanner | `services/analysis/structure_scanner.py` | `[ ]` |

---

### 26.2 ATR Volatility Padding Logic `[ ]`

**Acceptance Criteria**: Implement ATR (Average True Range) padding. Stop Loss = Swing Low - (1.5 * ATR). This prevents getting stopped out by random noise.

| Component | File Path | Status |
|-----------|-----------|--------|
| ATR Calculator | `services/indicators/atr_calc.py` | `[ ]` |
| Padding Logic | `services/strategies/stop_padding.py` | `[ ]` |

---

### 26.3 Position Size Integration & Validation `[ ]`

**Acceptance Criteria**: Verify that the calculated stop-loss distance is automatically injected into the Position Size Calculator. Block trades where the stop is too tight (High Risk of noise stop) or too wide (Tiny position size).

| Component | File Path | Status |
|-----------|-----------|--------|
| Size Integrator | `services/trading/size_integrator.py` | `[ ]` |

---

### 26.4 Neo4j Stop-Loss Logic Logger `[ ]`

**Acceptance Criteria**: Log the specific 'Structure Level ID' from Neo4j utilized for every stop-loss placement decision for audit trails.

```cypher
(:OBSERVATION {id: "Trade_123"})-[:USED_STOP_ANCHOR]->(:CANDLE {index: 1045, type: "SWING_LOW"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Logger | `services/neo4j/stop_logger.py` | `[ ]` |

---

### 26.5 Frontend Structure Visualizer `[ ]`

**Acceptance Criteria**: Display horizontal lines on the chart showing where the "Suggested Stop" is.

| Component | File Path | Status |
|-----------|-----------|--------|
| Stop Visualizer | `frontend2/src/components/Charts/StopVisualizer.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py stops suggest <ticker>` | Get optimal SL | `[ ]` |
| `python cli.py stops verify` | Check logic | `[ ]` |

---

*Last verified: 2026-01-25*
