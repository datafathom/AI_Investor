# Backend Service: Funds

## Overview
The **Funds Service** manages the platform's institutional pooled investment products. It handles the lifecycle of index funds, tracks massive capital flows (In/Out) across the platform, and provides a sophisticated **Tradability Classification** layer that ensures large institutional trades are only executed in sufficiently liquid markets with manageable geopolitical risk.

## Core Components

### 1. Index Fund Master (`index_fund_service.py`)
The central registry for the platform's fund offerings.
- **Product Management**: Handles the registration of new index products (ETFs/Mutual Funds) and manages their metadata (Ticker, Name, Fund Type).
- **AUM Tracking**: Dynamically updates the current Assets Under Management (AUM) for each fund, which serves as the baseline for liquidity and fee calculations.

### 2. Capital Flow Processor (`flow_processor.py`)
Monitors the "circulatory system" of institutional capital.
- **Net Flow Analysis**: Tracks daily net inflows and outflows at the ticker level.
- **Outflow Alerts**: Automatically flags "Significant Outflows" (threshold: -$1B) to warn the investment committee of potential institutional flight.
- **Market Impact Multipliers**: Calculates the expected multiplier effect of capital flows on a fund's underlying market cap.

### 3. Tradability Classifier (`tradability_classifier.py`)
An institutional risk guardrail for trade execution.
- **Liquidity Tiering**: Categorizes assets into `HIGHLY_LIQUID`, `LIQUID`, `MODERATE`, or `ILLIQUID` tiers based on the ratio of Average Daily Volume (ADV) to total fund AUM.
- **Geopolitical Risk Filter**: Factors in "Country Repatriation Risk" to identify restricted markets where capital may be trapped or liquidity may evaporate.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Fund Supermarket** | Index Catalog Grid | `index_fund_service.list_funds()` |
| **Mission Control** | Whale Flow Radar | `flow_processor.process_flow()` (Outflow alerts) |
| **Trading Terminal** | Liquidity Shield | `tradability_classifier.calculate_tradability_score()` |
| **Admin Station** | AUM Management Console | `index_fund_service.update_aum()` |
| **Institutional Station** | Restricted Market Map | `tradability_classifier` (Country risk flags) |

## Dependencies
- `schemas.index_fund`: Defines the Pydantic models for `IndexFund` and `IndexFundCreate`.
- `logging`: Records structural fund events, specifically "Significant Outflow" alerts.

## Usage Examples

### Classifying an Emerging Market Index Fund
```python
from services.funds.tradability_classifier import TradabilityClassifier

classifier = TradabilityClassifier()

# Example: EEM (Emerging Markets) with moderate country risk
classification = classifier.calculate_tradability_score(
    ticker="EEM",
    avg_volume=50_000_000,
    aum=25_000_000_000,
    country_risk=6 # Scale 0-10
)

print(f"Ticker: {classification['ticker']} | Tier: {classification['tier']}")
print(f"Tradability Score: {classification['score']}/100")
if classification['is_restricted']:
    print("WARNING: Capital controls detected. Trading limited.")
```

### Processing a Whale Inflow
```python
from services.funds.flow_processor import FlowProcessor

fp = FlowProcessor()

# $500M inflow into SPY
flow_report = fp.process_flow({
    "ticker": "SPY",
    "net_flow_usd": 500_000_000
})

print(f"Net Flow: ${flow_report['net_flow']:,.2f}")
print(f"Estimated Market Impact: ${flow_report['impact_on_market_cap']:,.2f}")
```
