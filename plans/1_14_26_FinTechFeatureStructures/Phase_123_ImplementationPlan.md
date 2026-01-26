# Phase 123: Sortino Ratio Downside Volatility Service

> **Status**: `[ ]` Not Started | **Owner**: Quantitative Team
> **Source**: JIRA_PLANNING_JSON_2.txt - Epoch VII Phase 3

## 📋 Overview
**Description**: Implement the Sortino Ratio calculator that focuses on downside risk only, providing a more accurate risk-adjusted return metric for asymmetric return distributions.

---

## 🎯 Sub-Deliverables

### 123.1 Sortino Calculator (Downside Std Dev) `[ ]`

**Acceptance Criteria**: Calculate Sortino Ratio using downside deviation instead of total standard deviation.

```python
class SortinoCalculator:
    """
    Sortino Ratio = (Portfolio Return - Risk-Free Rate) / Downside Deviation
    
    Key Difference from Sharpe:
    - Only considers negative volatility (losses)
    - Ignores upside volatility (gains)
    - Better for asymmetric return distributions
    """
    
    def calculate_downside_deviation(
        self,
        returns: list[Decimal],
        target_return: Decimal = Decimal('0')
    ) -> Decimal:
        """Calculate volatility of returns below target."""
        pass
    
    def calculate_sortino_ratio(
        self,
        returns: list[Decimal],
        risk_free_rate: Decimal,
        target_return: Decimal = Decimal('0')
    ) -> Decimal:
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sortino Calculator | `services/quantitative/sortino_calculator.py` | `[ ]` |
| Downside Deviation | `services/quantitative/downside_deviation.py` | `[ ]` |
| API Endpoint | `web/api/portfolio/sortino.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Sortino Widget | `frontend2/src/components/Performance/SortinoWidget.jsx` | `[ ]` |
| Downside Risk Chart | `frontend2/src/components/Charts/DownsideRiskChart.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Sortino Calculator | `tests/unit/test_sortino_calculator.py` | `[ ]` |
| Unit: Downside Deviation | `tests/unit/test_downside_deviation.py` | `[ ]` |
| Integration: Full Pipeline | `tests/integration/test_sortino_pipeline.py` | `[ ]` |

---

### 123.2 Postgres Drawdown Events Log `[ ]`

```sql
CREATE TABLE drawdown_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL,
    
    -- Drawdown Details
    peak_date DATE NOT NULL,
    peak_value DECIMAL(20, 2) NOT NULL,
    trough_date DATE,
    trough_value DECIMAL(20, 2),
    recovery_date DATE,
    
    -- Metrics
    drawdown_pct DECIMAL(8, 6) NOT NULL,
    duration_days INTEGER,
    recovery_days INTEGER,
    
    -- Classification
    severity VARCHAR(20),     -- MINOR (<5%), MODERATE (5-10%), SEVERE (>10%)
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('drawdown_events', 'peak_date');
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Drawdown Logger | `services/performance/drawdown_logger.py` | `[ ]` |
| Recovery Tracker | `services/performance/recovery_tracker.py` | `[ ]` |

### 123.3 Sharpe vs. Sortino Comparison Report `[ ]`
Generate comparative reports showing when Sortino provides better insight than Sharpe.

| Component | File Path | Status |
|-----------|-----------|--------|
| Comparison Reporter | `services/reporting/sharpe_vs_sortino.py` | `[ ]` |

### 123.4 Upside Volatility Ignore Logic `[ ]`
Implement logic that correctly ignores positive volatility in Sortino calculations.

### 123.5 Bear Market Historical Verification `[ ]`
Verify Sortino effectiveness using historical bear market data (2008, 2020, 2022).

| Component | File Path | Status |
|-----------|-----------|--------|
| Historical Verifier | `services/backtesting/sortino_backtest.py` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED
