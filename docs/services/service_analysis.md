# Backend Service: Analysis

## Overview
The **Analysis Service** is the most extensive component of the AI Investor platform, containing 84 specialized modules for financial modeling, market research, and performance evaluation. It provides the analytical backbone for the system's decision-making across all asset classes.

## Primary Analytical Pillars

### 1. Performance Attribution & Evaluation
This pillar decomposes portfolio performance to identify the true sources of alpha (manager skill) versus beta (market exposure).
- **Attribution Service (`attribution_service.py`)**: Implements the **Brinson-Fachler model** to decompose active returns into Allocation, Selection, and Interaction effects. It supports GICS sector-level benchmarking against the S&P 500 and NASDAQ.
- **Alpha Attributor (`alpha_attributor.py`)**: Specifically calculates non-market-related excess returns.
- **Manager Ranker (`manager_ranker.py`)**: Quantitatively ranks internal agent performance.

### 2. Backtesting & Monte Carlo Simulation
Provides rigorous testing for trading strategies before they are deployed in live or demo environments.
- **Backtest Engine (`backtest_engine.py`)**: The core execution engine for historical simulations.
- **Monte Carlo Service (`monte_carlo_service.py`)**: Implements **Geometric Brownian Motion (GBM)** simulations to calculate ruin probability, max drawdowns, and "Pain Index" metrics. It features "Hype-Adjusted Drift" to simulate the impact of social media trends on asset paths.
- **Genetic Distillery (`genetic_distillery.py`)**: Uses evolutionary algorithms to optimize strategy parameters and prevent over-fitting.

### 3. Macro & Economic Analysis
Aggregates global data to detect business cycle shifts and geopolitical risks.
- **Macro Service (`macro_service.py`)**: Integrates with **FRED (Federal Reserve Economic Data)** to fetch real-time CPI, GDP, and unemployment metrics for world-map visualization.
- **Global M2 Tracker (`global_m2.py`)**: Monitors global money supply liquidity.
- **OPEC Compliance (`opec_compliance.py`)**: Tracks commodity-specific political risks in the energy sector.

### 4. Quantitative Metrics & Modeling
Mathematical models for structural market analysis.
- **Factor Service (`factor_service.py`)**: Decomposes returns into known factors like Value, Momentum, and Size.
- **FFT & HMM Engines (`fft_engine.py`, `hmm_engine.py`)**: Uses Fast Fourier Transforms and Hidden Markov Models to detect cyclicality and market regime shifts.
- **GEX & Zero Gamma (`gex_calc.py`, `zero_gamma.py`)**: Calculates Gamma Exposure and option-driven market structure levels.

### 5. Sentiment & "Political Alpha"
Alternative data sources that provide an edge through non-traditional information flow.
- **Congress Tracker (`congress_tracker.py`)**: Correlates congressional stock disclosures with lobbying activity to generate a **Political Alpha Signal**.
- **YouTube & TikTok Analyzers (`youtube_transcript_analyzer.py`)**: Extracts sentiment and trend data from social media transcripts.
- **Earnings Sentiment (`earnings_sentiment.py`)**: Analyzes transcript sentiment from corporate earnings calls.

### 6. Technical Analysis & Structure
- **Technical Analysis Service (`technical_analysis_service.py`)**: Provides **50+ technical indicators** (RSI, MACD, Bollinger Bands, ATR, etc.) and pattern recognition logic (Flags, Triangles, Head & Shoulders).
- **Supply/Demand Zones (`supply_demand_zones.py`)**: Automatically identifies institutional "Order Blocks" and structural accumulation/distribution levels.

## Dependencies
- `pandas` & `numpy`: Core data manipulation.
- `random` & `math`: Statistical simulations.
- `services.data.fred_service`: External economic data provider.
- `services.system.api_governance`: Resource rate-limiting for data providers.

## Usage Examples

### Running a Monte Carlo GBM Simulation
```python
from services.analysis.monte_carlo_service import get_monte_carlo_service

mc = get_monte_carlo_service()
result = mc.run_gbm_simulation(initial_value=100000, ticker="SPY", days=30)

print(f"Ruin Probability: {result.ruin_probability:.2%}")
print(f"Expected Final Value: ${result.mean_final:,.2f}")
```

### Calculating Portfolio Attribution
```python
from services.analysis.attribution_service import AttributionService, DateRange

attr = AttributionService()
period = DateRange(start="2025-01-01", end="2025-12-31")
report = await attr.calculate_brinson_attribution("my-portfolio", "sp500", period)

print(f"Total Active Return: {report.total_active_return} bps")
print(f"Selection Effect: {report.total_selection_effect} bps")
```
