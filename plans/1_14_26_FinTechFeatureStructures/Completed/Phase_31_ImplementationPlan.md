# Phase 31: Position Size Calculator API Integration

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading Team

---

## 📋 Overview

**Description**: Integrate the "Cheat Code" position size calculator logic to eliminate human error and ensure mathematical discipline. The system must automatically calculate the exact lot size based on account balance, risk percentage (e.g., 1%), and stop-loss distance.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 31

---

## 🎯 Sub-Deliverables

### 31.1 Sizing Formula Microservice `[x]`

**Acceptance Criteria**: Implement the formula: `(Balance * Risk%) / (StopPrice - EntryPrice) * TickValue`. Handle all currency conversions (e.g., Account in USD, trade in GBP/JPY).

```python
class PositionSizer:
    def calculate_size(self, balance: Decimal, risk_pct: Decimal, entry: Decimal, stop: Decimal, pair: str) -> LotSize:
        risk_amount = balance * risk_pct
        stop_distance = abs(entry - stop)
        tick_value = self.market.get_tick_value(pair)
        
        raw_size = risk_amount / (stop_distance * tick_value)
        return self.normalize_to_broker_limits(raw_size)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sizing Service | `services/trading/sizer.py` | `[x]` |
| Calculator API | `web/api/trading/calculate_size.py` | `[x]` |

---

### 31.2 Cross-Currency Conversion Logic `[x]`

**Acceptance Criteria**: Ensure the service automatically handles cross-currency conversions. If Account is USD and pair is EUR/GBP, the pip value depends on GBP/USD rate.

| Component | File Path | Status |
|-----------|-----------|--------|
| Rate Converter | `services/finance/fx_converter.py` | `[x]` |

---

### 31.3 Broker Limit Normalization `[x]`

**Acceptance Criteria**: Ensure calculated size respects broker limits (Min Lot 0.01, Max Lot 100). Round down to nearest valid step to avoid "Invalid Order" rejections.

| Component | File Path | Status |
|-----------|-----------|--------|
| Normalizer | `services/trading/lot_normalizer.py` | `[x]` |

---

### 31.4 Frontend Calculator Widget `[x]`

**Acceptance Criteria**: Expose the calculator via the AI_Investor GUI for manual trade validation. Auto-fill current balance and price.

| Component | File Path | Status |
|-----------|-----------|--------|
| React Widget | `frontend2/src/components/Trading/SizeCalc.jsx` | `[x]` |

---

### 31.5 Audit Log of Sizing Parameters `[x]`

**Acceptance Criteria**: Log all input parameters (Balance, Risk %, SL) for every calculation to ensure full auditability.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sizing Log | `services/logging/sizing_audit.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py size calc <pair> <stop>` | Get lots | `[x]` |
| `python cli.py size verify <id>` | Audit calc | `[x]` |

---

*Last verified: 2026-01-25*
