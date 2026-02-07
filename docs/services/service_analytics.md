# Backend Service: Analytics

## Overview
The **Analytics Service** is responsible for deep-dive quantitative analysis of portfolio performance and risk. It transforms raw holding and trade data into actionable insights through sophisticated attribution models, risk decomposition frameworks, and secure performance reporting.

## Core Engines

### 1. Performance Attribution Engine (`performance_attribution_service.py`)
This engine decomposes portfolio returns to identify whether gains were driven by market timing (allocation) or asset selection.
- **Methodology**: 
    - **Modified Dietz**: Calculates time-weighted returns.
    - **Brinson-Fachler Model**: Decomposes active returns into Allocation, Selection, and Interaction effects.
- **Features**:
    - **Benchmark Comparison**: Real-time relative performance against indices like SPY or QQQ.
    - **Hierarchical Drill-down**: Analyze performance by Asset Class, Sector, Geography, or individual Holding.
    - **Contribution Analysis**: Ranks every position by its absolute and percentage contribution to the total P&L.

### 2. Risk Decomposition Engine (`risk_decomposition_service.py`)
Provides a multi-dimensional view of portfolio volatility and the potential for extreme losses.
- **Methodology**:
    - **Factor Models**: Decomposes risk into Fama-French factors (Market, Size, Value, Momentum, Quality).
    - **Concentration Analysis**: Calculates the **Herfindahl-Hirschman Index (HHI)** to detect over-concentration in specific holdings or sectors.
    - **Tail Risk**: Computes **Value at Risk (VaR)** and **Conditional Value at Risk (CVaR)** using historical simulations.
- **Features**:
    - **Correlation Matrix**: Analyzes inter-holding relationships to determine diversification ratios.
    - **Marginal Risk Contribution**: Identifies which specific assets are adding the most to the portfolio's overall volatility profile.

### 3. Alpha Reporting Service (`alpha_reporting.py`)
Generates secure, high-integrity performance summaries for audit and review.
- **Role**: Synthesizes the output of the attribution and risk engines into summarized EOD (End-of-Day) reports.
- **Security**: Features a **Sovereign PGP-simulated encryption layer** (using Fernet) to ensure performance data is secured before transmission or storage.
- **Metrics**: Highlights "MVP Agents" and "Laggard Sectors" to provide a quick executive snapshot.

## Dependencies
- `pandas` & `numpy`: Heavy-duty numerical processing.
- `scipy.stats`: Used for VaR/CVaR and normalized risk distributions.
- `cryptography`: Powers the secure reporting encryption layer.
- `services.portfolio.portfolio_aggregator`: Source of truth for holdings and weights.

## Usage Examples

### Running Risk Decomposition
```python
from services.analytics.risk_decomposition_service import get_risk_decomposition_service

risk_svc = get_risk_decomposition_service()
analysis = await risk_svc.calculate_concentration_risk(portfolio_id="user_77")

print(f"Holding Concentration (HHI): {analysis.by_holding.herfindahl_hirschman_index:.4f}")
print(f"Top 5 Concentration: {analysis.by_holding.top_5_concentration:.2%}")
```

### Generating a Secure Alpha Report
```python
from services.analytics.alpha_reporting import get_alpha_reporting_service

reporter = get_alpha_reporting_service()
report = reporter.generate_eod_report(encrypt=True)

print(f"Secure Report Generated. Checksum: {report['checksum']}")
# Payload is encrypted string: report['payload']
```
