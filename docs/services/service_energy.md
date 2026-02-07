# Backend Service: Energy

## Overview
The **Energy Service** manages the platform's transition into the physical energy and deep-tech sectors. It provides dual-layer capabilities: (1) real-time operational management of renewable energy assets (Solar, Battery Storage) and grid arbitrage, and (2) high-frontier investment research focusing on breakthroughs in fusion energy and proprietary patent analysis.

## Core Components

### 1. Grid Arbitrage & Battery Hub (`battery_mgr.py`)
Optimizes energy storage assets for profitability.
- **Dynamic Grid Arbitrage**: Monitors real-time grid prices and automatically triggers "CHARGE" cycles during off-peak periods (<$0.10) and "DISCHARGE" cycles during peak periods (>$0.40).
- **Asset Health**: Monitors charge levels and remaining runtime for residential/commercial battery banks (e.g., Tesla Powerwalls).

### 2. High-Frontier Energy Tech
- **Fusion Reactor Simulation (`fusion_sim.py`)**: Provides high-fidelity telemetry for fusion energy investments. Tracks critical metrics like **Plasma Temperature**, **Magnetic Confinement Stability**, and the **Q-factor** (Energy Gain vs. Input).
- **Patent Discovery Bot (`patent_bot.py`)**: A "Deep Tech" aggregator that scans USPTO, WIPO, and EPO databases for keywords like "Low Energy Nuclear Reactions (LENR)," "Zero Point," and "Solid State." Includes a "Scientific Validity" scoring layer to filter high-potential disruptions from noise.

### 3. Physical Asset Monitoring
- **Solar Monitor (`solar_monitor.py`)**: Tracks real-time photovoltaic output and efficiency.
- **Generator Service (`generator_svc.py`)**: Manages backup and peaking generator assets.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Energy Station** | Grid Price Arbitrage Table | `battery_manager.optimize_cycle()` |
| **Energy Station** | Facility Battery Health | `battery_manager.get_status()` |
| **Deep Tech Research** | Fusion Reactor Telemetry | `fusion_reactor_sim.get_telemetry()` |
| **Deep Tech Research** | New Patent Alerts | `patent_aggregator.scan_patents()` |
| **Strategist Station** | Asset Replacement Value | `solar_monitor.py` (Efficiency metrics) |

## Dependencies
- `random`: Used in simulations to model plasma fluctuations and technical volatility.
- `logging`: Records structural energy events, including "SCRAM" emergency shutdowns and patent flags.

## Usage Examples

### Executing Grid Arbitrage Optimization
```python
from services.energy.battery_mgr import BatteryManagerService

battery = BatteryManagerService()

# Simulate a peak price event ($0.45/kWh)
decision = battery.optimize_cycle(grid_price=0.45)

if decision == "DISCHARGE":
    print("Action: Selling energy back to the grid at peak rates.")
    print(f"Current Charge: {battery.get_status()['charge_level']}")
```

### Scanning for Fusion Energy Breakthroughs
```python
from services.energy.patent_bot import PatentAggregatorService

bot = PatentAggregatorService()

# Scan global databases for new filings
findings = bot.scan_patents()

for patent in findings:
    analysis = bot.analyze_patent(patent['id'])
    if analysis['market_potential'] == "DISRUPTIVE":
        print(f"ALERT: Disruptive energy technology detected: {patent['title']}")
```
