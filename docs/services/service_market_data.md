# Backend Service: Market Data (Structural Flow Intelligence)

## Overview
The **Market Data Service** (internally known as **Structural Flow Intelligence**) is the platform's deep-intelligence layer. It focuses on identifying structural imbalances and institutional movements that aren't visible in raw price tick data. The service follows sophisticated quantitative theses, such as **Michael Green's "Forced Seller"** model (passive index fragility), tracks **Whale Selling Pressure** via 13F filing deltas, and monitors **Volume Promo Spikes** to identify social-media-driven pumps that create artificial exit liquidity for insiders.

## Core Components

### 1. Forced Seller & Passive Fragility Tracker (`forced_seller_svc.py`)
Analyzes the structural risks of passive indexing.
- **Passive Concentration Index**: Scores tickers based on their percentage of passive ownership. High passive concentration indicates structural "inelasticity"—where mandatory buying/selling by index funds can cause violent price swings independent of fundamentals.
- **Liquidity Trap Detector**: Monitors bid/ask spread expansion relative to historical averages. It triggers a "Halt" signal if the spread expands by >2.5x, indicating a liquidity vacuum where active trading becomes dangerous.

### 2. Whale Flow & Crowding Analyzer (`fund_flow_service.py`)
Tracks the footprints of institutional capital.
- **Whale Selling Tracker**: Analyzes 13F and institutional filing data to detect "Agitator Selling"—aggressive exit pressure (>1M shares) by major hedge funds or asset managers.
- **Sector Overcrowding Engine**: Identifies when specific sectors (e.g., Tech, Energy) become structurally overcrowded by institutional "Long" mandates, signaling a higher risk of a sharp multi-trader exit.

### 3. Volume & Promo Monitor (`volume_monitor.py`)
Detects artificial activity and sentiment spikes.
- **Promo Spike Detector**: Cross-references volume spikes (>2x average) with extreme social media sentiment to identify "Promotional Pumping." This is a critical indicator for detecting efforts to create sellable volume for Rule 144 affiliate sales or institutional exits.
- **Weekly Volume Baseline**: Establishes a 4-week moving average of trading volume to provide a stable baseline for anomaly detection.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Whale Watch Terminal** | Institutional Exit Feed | `fund_flow_service.track_whale_selling()` |
| **Whale Watch Terminal** | Passive Fragility Heatmap | `forced_seller_svc.monitor_passive_flow()` |
| **Market Intelligence** | Sector Overcrowding Dial | `fund_flow_service.detect_sector_overcrowding()` |
| **System Monitor** | Liquidity Trap Warning | `forced_seller_svc.detect_liquidity_trap()` |
| **Governance Hub** | Promo/Hype Alert Ticker | `volume_monitor.detect_promo_spike()` |

## Dependencies
- `decimal`: Used for all high-precision calculations involving ownership percentages and flow velocities.
- `json / logging`: Manages the ingestion of Kafka-based volume alerts and records structural risk events.

## Usage Examples

### Detecting Structural Fragility in an Index Heavyweight
```python
from services.market_data.forced_seller_svc import ForcedSellerService

fs_svc = ForcedSellerService()

# Ticker with 75% passive ownership (e.g., a core S&P 500 component)
report = fs_svc.monitor_passive_flow(ticker="AAPL", passive_ownership_pct=75.0)

print(f"Ticker: {report['ticker']} | Fragility Score: {report['fragility_score']}")
print(f"Risk Level: {report['risk_level']}")
if report['risk_level'] == "CRITICAL":
    print("WARNING: Price is structurally inelastic to active supply/demand.")
```

### Tracking Aggressive 'Whale' Exit Pressure
```python
from services.market_data.fund_flow_service import FundFlowService

whale_svc = FundFlowService()

# Latest filing deltas for a specific stock
deltas = [
    {"holder": "WHALE_FUND_A", "change": -2500000}, # Sold 2.5M shares
    {"holder": "WHALE_FUND_B", "change": -1200000}
]

report = whale_svc.track_whale_selling(ticker="TSLA", filing_data=deltas)

print(f"Signal: {report['signal']} | Major Sellers: {', '.join(report['major_sellers'])}")
print(f"Total Institutional Pressure: {report['total_whale_sold']:,} shares")
```

### Identifying a Social-Media-Driven Volume Spike
```python
from services.market_data.volume_monitor import VolumeMonitor

monitor = VolumeMonitor()

# Input: Current Vol 5M vs Avg Vol 1M, with extremely positive social hype (0.95)
spike = monitor.detect_promo_spike(
    ticker="PUMP_TICKER", 
    current_vol=5000000, 
    avg_vol=1000000, 
    social_sentiment_score=0.95
)

if spike['is_promo_spike']:
    print(f"FLAGGED: {spike['ticker']} is undergoing a PROMO SPIKE.")
    print(f"Action: {spike['action']}")
```
