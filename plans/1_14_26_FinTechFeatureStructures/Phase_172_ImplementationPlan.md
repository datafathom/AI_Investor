# Phase 172: Illiquid Asset Premium & Volatility Smoother

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Quantitative & Risk Team

---

## 📋 Overview

**Description**: Manage the "Illiquidity Premium" – the extra return investors demand for locking up capital. Also, address "Volatility Smoothing" (the fact that private assets aren't marked-to-market daily), which artificially lowers portfolio volatility. We must "unsmooth" returns to understand true risk.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch IX Phase 12

---

## 🎯 Sub-Deliverables

### 172.1 Illiquidity Premium Calculator (3-5% target) `[ ]`

**Acceptance Criteria**: Calculator to verify if a private deal is offering enough premium over public markets. If Corporate Bonds yield 5%, Private Credit should yield ~8-10% (3-5% premium).

#### Backend Implementation

```python
class PremiumCalculator:
    """
    Calculate required illiquidity premium.
    
    Formula:
    Required Return = RiskFree + MarketRisk + IlliquidityPremium
    """
    def calculate_premium(self, private_return: Decimal, public_benchmark_return: Decimal) -> PremiumResult:
        premium = private_return - public_benchmark_return
        is_sufficient = premium >= Decimal('0.03') # 3% Target
        return PremiumResult(premium=premium, is_sufficient=is_sufficient)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Premium Calculator | `services/private_markets/premium_calc.py` | `[ ]` |
| Benchmark Fetcher | `services/market/public_benchmark.py` | `[ ]` |

---

### 172.2 Return "Unsmoothing" Algorithm `[ ]`

**Acceptance Criteria**: Statistical method (e.g., Geltner Index) to estimate the "True" volatility of private assets by removing the lag effect of quarterly appraisals.

```python
class VolatilityUnsmoother:
    """
    Recover true volatility from smoothed returns.
    """
    def unsmooth_returns(self, smoothed_returns: list[Decimal], autocorrelation: Decimal) -> list[Decimal]:
        # True_t = (Smoothed_t - rho * Smoothed_t-1) / (1 - rho)
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Unsmoother Service | `services/risk/volatility_unsmoother.py` | `[ ]` |

---

### 172.3 Postgres Lock-Up Period Tracker `[ ]`

**Acceptance Criteria**: Track liquidity schedules. When does the lock-up end? When are redemption windows?

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE liquidity_terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL,
    
    -- Terms
    lockup_months INTEGER,
    redemption_frequency VARCHAR(20),  -- QUARTERLY, ANNUALLY, NONE
    notice_days INTEGER,               -- 45, 60, 90
    gate_percentage DECIMAL(5, 4),     -- Max 25% withdrawal per qtr
    
    -- Dates
    investment_date DATE,
    liquidity_available_date DATE GENERATED ALWAYS AS (investment_date + (lockup_months * INTERVAL '1 month')) STORED,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/172_liquidity_terms.sql` | `[ ]` |
| Terms Service | `services/private_markets/liquidity_terms.py` | `[ ]` |

---

### 172.4 True Sharpe Ratio (Unsmoothed) Service `[ ]`

**Acceptance Criteria**: Calculate a "True Sharpe" for private portfolios using the unsmoothed volatility. Usually much lower than the reported Sharpe.

| Component | File Path | Status |
|-----------|-----------|--------|
| True Sharpe Calc | `services/performance/true_sharpe.py` | `[ ]` |

---

### 172.5 Secondary Market Valuation Discount Estimator `[ ]`

**Acceptance Criteria**: Estimate the "Haircut" required to sell an illiquid asset immediately on the secondary market (e.g., 20% discount to NAV).

| Component | File Path | Status |
|-----------|-----------|--------|
| Discount Estimator | `services/valuation/secondary_market.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Premium Dashboard | `frontend2/src/components/PrivateMarkets/PremiumDash.jsx` | `[ ]` |
| Liquidity Calendar | `frontend2/src/components/Calendar/LiquiditySchedule.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py priv calc-premium` | Show premium | `[ ]` |
| `python cli.py priv unsmooth <id>` | Show true volatility | `[ ]` |

---

*Last verified: 2026-01-25*
