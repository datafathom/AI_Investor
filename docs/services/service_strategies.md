# Backend Service: Strategies (The Playbook)

## Overview
The **Strategies Service** contains **14 pre-built trading strategies** that the platform can deploy. These range from regime-aware allocation to political alpha (Pelosi tracking) to risk parity. Each strategy is a modular "recipe" that the Strategy Execution Engine can run.

## Core Components (Selected)

### 1. Regime Detector (`regime_detector.py`)
- **Trend Filter**: Uses SPY vs. 200-day SMA to classify market regime.
- **Volatility Filter**: Uses VIX level to confirm regime.
- **Regimes**: BULL (above SMA, low VIX), BEAR (below SMA or high VIX), TRANSITION.

### 2. Other Key Strategies
- `pelosi_copy.py`: Tracks and mirrors congressional trade disclosures.
- `risk_parity.py`: Allocates based on volatility contribution.
- `quality_tilt.py`: Overweights high-quality stocks.
- `smart_rebalance.py`: Intelligent portfolio rebalancing.
- `zone_filter.py`: Technical support/resistance-based filtering.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategy Builder** | Regime Selector | `regime_detector.detect_current_regime()` | **Implemented** |
| **Political Alpha** | Pelosi Tracker | `pelosi_copy` | **Implemented** (`PoliticalAlpha.jsx`) |

## Usage Example

```python
from services.strategies.regime_detector import RegimeDetector

detector = RegimeDetector()

regime = detector.detect_current_regime("SPY")

print(f"Current Regime: {regime['name']}")
print(f"Confidence: {regime['confidence']}")
print(f"SPY Position: {regime['spy_pos']}")
print(f"Risk-Off Mode: {regime['is_risk_off']}")
```
