# Backend Service: Quantitative (The Quant Lab)

## Overview
The **Quantitative Service** is the mathematical engine of the platform. It houses 21 specialized calculators for generating alpha, assessing risk-adjusted returns, and detecting market anomalies. It enables the system to grade its own performance (Sharpe, Alpha) and identify structural market risks (Passive Bubble, Reflexivity).

## Core Components (Selected)

### 1. Alpha Calculator (`alpha_calculator.py`)
- **Simple Alpha**: `Portfolio Return - Benchmark Return`.
- **Jensen's Alpha**: Risk-adjusted outperformance accounting for Beta, using the CAPM formula.

### 2. Sharpe Ratio Calculator (`sharpe_calculator.py`)
- **Formula**: `(Rp - Rf) / σp`
- Annualizes daily returns (252 trading days) and volatility.

### 3. Reflexivity Engine (`reflexivity_engine.py`)
- **Passive Saturation Check**: Flags tickers where "Big Three" (BlackRock, Vanguard, State Street) hold > 40% of shares, indicating extreme fragility to index rebalancing flows.
- **Inelastic Flow Impact**: Models how passive inflows move prices non-linearly.

### Other Key Modules
- `sortino_calculator.py`: Sharpe variant that only penalizes *downside* volatility.
- `correlation_calculator.py`: Tracks portfolio diversification.
- `rolling_metrics.py`: Time-windowed performance snapshots.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategist** | Alpha/Beta Dashboard | `alpha_calculator.calculate_jensens_alpha()` | **Implemented** (`StrategistAlphabeta.jsx`) |
| **Portfolio Analytics** | Performance Radar | `sharpe_calculator.calculate()` | **Implemented** (`AdvancedPortfolioAnalytics.jsx`) |
| **Risk Monitor** | Reflexivity Alert | `reflexivity_engine.check_passive_saturation()` | **Implicit** (Feeds into Risk Dashboard) |

## Dependencies
- `numpy`: Foundation for all statistical calculations (mean, std, sqrt).
- `decimal`: Used in `reflexivity_engine.py` for precise percentage calculations.

## Usage Examples

### Calculating Jensen's Alpha
```python
from services.quantitative.alpha_calculator import AlphaCalculator

calc = AlphaCalculator()

# My portfolio returned 15%, S&P 500 returned 10%
# Risk-free rate is 2%, my Beta is 1.1
alpha = calc.calculate_jensens_alpha(
    portfolio_ret=0.15,
    benchmark_ret=0.10,
    rf_rate=0.02,
    beta=1.1
)
print(f"Jensen's Alpha: {alpha:.2%}") # Outperformance vs. expected
```

### Calculating Sharpe Ratio
```python
from services.quantitative.sharpe_calculator import SharpeRatioCalculator

calc = SharpeRatioCalculator()

daily_returns = [0.001, -0.002, 0.003, 0.001, -0.001] # Sample
sharpe = calc.calculate(daily_returns, risk_free_rate=0.02)

print(f"Sharpe Ratio: {sharpe}")
```

### Checking Passive Bubble Risk
```python
from services.quantitative.reflexivity_engine import ReflexivityEngine

engine = ReflexivityEngine()

# AAPL: Big Three own 6B shares, 15B total outstanding
report = engine.check_passive_saturation("AAPL", 6_000_000_000, 15_000_000_000)

print(f"Passive Ownership: {report['passive_ownership_pct']}%")
print(f"Reflexivity Risk: {report['inelasticity_rank']}")
```
