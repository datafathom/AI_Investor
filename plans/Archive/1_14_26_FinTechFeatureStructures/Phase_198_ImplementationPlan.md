# Phase 198: Bear Market Defensive Positioning Protocol

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading & Risk Team

---

## 📋 Overview

**Description**: Automated defense mechanisms. When "Regime Change" is detected (Bull to Bear), automatically shift portfolio posture. Reduce Beta, Increase Quality, Hedge Tails. Don't wait for human panic.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 18

---

## 🎯 Sub-Deliverables

### 198.1 200-Day Moving Average Regime Detector `[ ]`

**Acceptance Criteria**: Classic trend filter. SPY < 200 SMA = "Risk Off". SPY > 200 SMA = "Risk On".

```python
class RegimeDetector:
    def detect_regime(self, ticker: str = 'SPY') -> Regime:
        price = self.market.get_price(ticker)
        sma_200 = self.market.get_sma(ticker, 200)
        return Regime.RISK_OFF if price < sma_200 else Regime.RISK_ON
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Regime Detector | `services/strategies/regime_detector.py` | `[ ]` |

---

### 198.2 Automated Beta Reduction (Shift to Low Vol) `[ ]`

**Acceptance Criteria**: If Risk Off, auto-rotate from High Beta (Tech/Discretionary) to Low Beta (Consumer Staples/Utilities/Healthcare).

| Component | File Path | Status |
|-----------|-----------|--------|
| Beta Reducer | `services/trading/beta_reducer.py` | `[ ]` |

---

### 198.3 Cash Raising Triggers (Stop-Loss logic) `[ ]`

**Acceptance Criteria**: Trailing Stop logic. If portfolio drops 10%, sell 10% to cash. If drops 20%, sell another 20%. Preserve capital to buy the bottom.

| Component | File Path | Status |
|-----------|-----------|--------|
| Stop Loss Engine | `services/trading/trailing_stop.py` | `[ ]` |

---

### 198.4 Quality Factor Tilt (Profitability/Low Leverage) `[ ]`

**Acceptance Criteria**: In bear markets, Quality performs best. Factor tilt towards high ROE, low Debt-to-Equity.

| Component | File Path | Status |
|-----------|-----------|--------|
| Quality Filter | `services/strategies/quality_tilt.py` | `[ ]` |

---

### 198.5 "Keep the Lights On" Dividend Income Overlay `[ ]`

**Acceptance Criteria**: Shift to Dividend Aristocrats. Ensure cash flow continues even if asset prices drop, preventing the need to sell principal at lows.

| Component | File Path | Status |
|-----------|-----------|--------|
| Dividend Overlay | `services/portfolio/dividend_safety.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Defense Control | `frontend2/src/components/Risk/DefenseControl.jsx` | `[ ]` |
| Regime Indicator | `frontend2/src/components/Charts/RegimeLight.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py defense status` | Show current regime | `[ ]` |
| `python cli.py defense activate` | Manual override | `[ ]` |

---

*Last verified: 2026-01-25*
