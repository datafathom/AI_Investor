# Backend Service: Ingestion

## Overview
The **Ingestion Service** is the platform's "Digital Collector." It manages the high-bandwidth pipelines required to source alternative and traditional market data. From the granular "Dark Pool" tape to satellite-derived port congestion counts and SEC filing scrapers, this service ensures that the platform has a information edge by aggregating signals that are often invisible to retail and standard institutional players.

## Core Components

### 1. Dark Pool Tape Engine (`dark_tape.py`)
Tracks the "Invisible Hand" of institutional liquidity.
- **Off-Exchange Filtering**: Specifically targets "Dark Prints" (Exchange Code 'D') which represent 40%+ of global equity volume.
- **Block Cluster Detection**: Analyzes identical-size trade prints to identify "Split Block" orders, revealing the entry and exit points of institutional whales.
- **Dark Level Identification**: Pinpoints price levels with anomalous dark volume, which serve as institutional support and resistance zones.

### 2. SEC & Financial Scraper (`sec_scraper.py`)
The foundational layer for valuation modeling.
- **Live Financial Extraction**: Pulls real-time Free Cash Flow (FCF), ROIC, and Operating Margins via market data APIs (`yfinance`) to feed the platform's DCF (Discounted Cash Flow) engines.
- **Filing Discovery**: Provides a framework for automated EDGAR retrieval, allowing the system to monitor 10-K and 10-Q filings for fundamental sentiment shifts.

### 3. Alternative Telemetry Ingestors
- **Satellite Port Telemetry (`port_congestion.py`)**: Sinks visual ship counts from major global ports (e.g., Long Beach, Rotterdam) to provide leading indicators for supply chain bottlenecks and inflationary pressure.
- **Federal Reserve Balance Tracker (`fed_balance.py`)**: Monitors the "Size of the Fed" as a primary signal for macro liquidity conditions (QE/QT).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Whale Watch Terminal** | Dark Print Ticker | `dark_pool_tape.filter_dark_prints()` |
| **Whale Watch Terminal** | Institutional Level Heatmap | `dark_pool_tape.get_significant_levels()` |
| **Supply Chain Hub** | Port Congestion Gauge | `port_congestion.get_ship_count()` |
| **Fundamental Station** | Income/Cash Flow Ledger | `sec_scraper.get_financials()` |
| **Strategist Station** | Fed Balance Pulse | `fed_balance.py` (Telemetry feed) |

## Dependencies
- `yfinance`: Powers the immediate retrieval of live institutional-grade financials.
- `logging`: Records the discovery of "Split Block" clusters and satellite ingestion events.

## Usage Examples

### Detecting Institutional "Block Clusters" in Dark Pools
```python
from services.ingestion.dark_tape import DarkPoolTapeService

tape = DarkPoolTapeService()

# Mock tape data containing some identical 10,000 share chunks
mock_tape = [
    {"symbol": "NVDA", "price": 450.50, "size": 10000, "exchange": "D"},
    {"symbol": "NVDA", "price": 450.55, "size": 10000, "exchange": "D"},
    {"symbol": "NVDA", "price": 450.45, "size": 10000, "exchange": "D"}
]

clusters = tape.detect_block_clusters(dark_prints=mock_tape)

for c in clusters:
    print(f"Detected {c['count']}x {c['size']} share prints | Total Volume: {c['total_volume']}")
```

### Retrieving Live Valuation Metrics
```python
from services.ingestion.sec_scraper import SECScraper

scraper = SECScraper()

# Fetch valuation metrics for Microsoft
metrics = scraper.get_financials(ticker="MSFT")

print(f"Market Cap: ${metrics['market_cap'] / 1e12:.2f}T")
print(f"Free Cash Flow: ${metrics['free_cash_flow'] / 1e9:.2f}B")
print(f"ROIC: {metrics['roic']:.2%}")
```
