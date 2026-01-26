# Phase 122: Sharpe Ratio Microservice

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative Team

---

## 📋 Overview

**Description**: Implement the classic measure of risk-adjusted returns using standard deviation and the risk-free rate.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 122.1 Sharpe Ratio Calculator Microservice `[ ]`

**Acceptance Criteria**: Develop a microservice to calculate the 'Sharpe Ratio' using the formula: (Portfolio Return - Risk-Free Rate) / Standard Deviation.

#### Backend Implementation

```python
from decimal import Decimal
from typing import List
import numpy as np

class SharpeRatioCalculator:
    """
    Sharpe Ratio = (Rp - Rf) / σp
    
    Where:
    - Rp = Portfolio return (annualized)
    - Rf = Risk-free rate (e.g., 10-Year Treasury)
    - σp = Standard deviation of portfolio returns (annualized)
    """
    
    def calculate(self, returns: List[float], risk_free_rate: float) -> float:
        """Calculate Sharpe Ratio from daily returns."""
        if len(returns) < 30:
            raise ValueError("Insufficient data: need at least 30 data points")
        
        # Annualize returns (assuming 252 trading days)
        mean_return = np.mean(returns) * 252
        std_dev = np.std(returns) * np.sqrt(252)
        
        if std_dev == 0:
            return 0.0
        
        sharpe = (mean_return - risk_free_rate) / std_dev
        return round(sharpe, 4)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sharpe Calculator | `services/quantitative/sharpe_calculator.py` | `[ ]` |
| Returns Processor | `services/quantitative/returns_processor.py` | `[ ]` |
| API Endpoint | `web/api/metrics/sharpe.py` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Sharpe Calculator | `tests/unit/test_sharpe_calculator.py` | `[ ]` |
| Integration: API | `tests/integration/test_sharpe_api.py` | `[ ]` |

---

### 122.2 Risk-Free Rate Data Storage `[ ]`

**Acceptance Criteria**: Implement a Postgres table to store daily 'Risk-Free Rate' data based on current 10-Year Treasury Bond yields.

#### Database Schema

```sql
CREATE TABLE risk_free_rates (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    rate_10y DECIMAL(8, 6) NOT NULL,  -- 10-Year Treasury
    rate_2y DECIMAL(8, 6),            -- 2-Year Treasury
    rate_3m DECIMAL(8, 6),            -- 3-Month Treasury
    source VARCHAR(50) DEFAULT 'FRED',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rfr_date ON risk_free_rates(date DESC);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/122_risk_free_rates.sql` | `[ ]` |
| FRED API Client | `services/external/fred_client.py` | `[ ]` |
| Rate Ingestion | `services/rate_ingestion_service.py` | `[ ]` |

---

### 122.3 Portfolio Volatility Analyzer `[ ]`

**Acceptance Criteria**: Create a 'Portfolio Volatility' analyzer to provide the denominator (Standard Deviation) for the Sharpe calculation.

#### Backend Implementation

```python
class VolatilityAnalyzer:
    """Calculate portfolio volatility using various methods."""
    
    def calculate_std_dev(self, returns: List[float], 
                          annualize: bool = True) -> float:
        """Calculate standard deviation of returns."""
        std = np.std(returns, ddof=1)  # Sample std dev
        if annualize:
            std *= np.sqrt(252)  # Annualize
        return std
    
    def calculate_downside_dev(self, returns: List[float], 
                                target: float = 0.0) -> float:
        """Calculate downside deviation (for Sortino)."""
        downside = [r for r in returns if r < target]
        if not downside:
            return 0.0
        return np.std(downside, ddof=1) * np.sqrt(252)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Volatility Analyzer | `services/quantitative/volatility_analyzer.py` | `[ ]` |
| Statistics Utils | `utils/statistics.py` | `[ ]` |

---

### 122.4 Sharpe Ratio Grading System `[ ]`

**Acceptance Criteria**: Build a logic layer to flag Sharpe ratios: >1.0 (Good), >2.0 (Very Good), and >3.0 (Exceptional).

#### Grading Logic

| Sharpe Range | Grade | Color | Description |
|--------------|-------|-------|-------------|
| < 0.0 | Poor | Red | Negative risk-adjusted return |
| 0.0 - 1.0 | Below Average | Orange | Returns don't justify risk |
| 1.0 - 2.0 | Good | Yellow | Acceptable risk-adjusted return |
| 2.0 - 3.0 | Very Good | Green | Strong risk-adjusted return |
| > 3.0 | Exceptional | Blue | Outstanding performance |

| Component | File Path | Status |
|-----------|-----------|--------|
| Sharpe Grader | `services/quantitative/sharpe_grader.py` | `[ ]` |
| Grade Config | `config/sharpe_grades.py` | `[ ]` |

---

### 122.5 Upside Volatility Warning System `[ ]`

**Acceptance Criteria**: Implement a warning system for Sharpe ratios artificially lowered by 'Upside Volatility' (identifying the formula flaw).

#### Backend Implementation

```python
class UpsideVolatilityDetector:
    """
    Detect when Sharpe ratio is unfairly penalized by upside volatility.
    
    The Sharpe ratio flaw: it treats upside and downside volatility equally,
    but investors only truly care about downside risk.
    """
    
    def detect_upside_penalty(self, returns: List[float]) -> dict:
        upside = [r for r in returns if r > 0]
        downside = [r for r in returns if r < 0]
        
        upside_vol = np.std(upside) if upside else 0
        downside_vol = np.std(downside) if downside else 0
        
        if upside_vol > downside_vol * 1.5:
            return {
                'warning': True,
                'message': 'Sharpe penalized by high upside volatility',
                'recommendation': 'Consider Sortino ratio instead',
                'upside_vol': upside_vol,
                'downside_vol': downside_vol
            }
        return {'warning': False}
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Upside Detector | `services/quantitative/upside_volatility_detector.py` | `[ ]` |
| Warning Service | `services/alerts/sharpe_warning_service.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 122.1 Sharpe Calculator | `[ ]` | `[ ]` |
| 122.2 Risk-Free Rate Storage | `[ ]` | `[ ]` |
| 122.3 Volatility Analyzer | `[ ]` | `[ ]` |
| 122.4 Grading System | `[ ]` | `[ ]` |
| 122.5 Upside Warning | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sharpe <portfolio_id>` | Calculate Sharpe ratio | `[ ]` |
| `python cli.py rfr-update` | Update risk-free rates | `[ ]` |
| `python cli.py volatility <portfolio_id>` | Analyze volatility | `[ ]` |

---

## 📦 Dependencies

- Phase 139: Risk-Free Rate Ingestion Service
- Phase 3: TimescaleDB (price data)

---

*Last verified: 2026-01-25*
