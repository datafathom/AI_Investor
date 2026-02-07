# Backend Service: Pricing (The Ticker)

## Overview
The **Pricing Service** manages the granular details of market data. It has two main responsibilities: ensuring mathematical precision (rounding, pip calculations) to prevent floating-point errors in financial transactions, and high-frequency storage of incoming price ticks into a specialized Time-Series Database (TimescaleDB).

## Core Components

### 1. Precision Engine (`pricing/precision_engine.py`)
The Normalizer.
- **Decimal Enforcement**: Ensures all prices and quantities are stored as `Decimal` objects, not floats.
- **Pip/Tick Calculation**: Converts raw price differences into standardized "Pips" for FX or "Ticks" for Futures based on symbol-specific configs.
- **Display Formatting**: Guarantees that JPY pairs show 3 decimal places while EURUSD shows 5, matching standard trading terminals.

### 2. Price Telemetry Service (`price_telemetry_service.py`)
The Tape.
- **High-Frequency Ingestion**: Writes thousands of price updates per second (Ticks) into a hypertable.
- **TimescaleDB Integration**: Uses efficient SQL for time-series queries (e.g., "Get the last known price").

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **System Health** | Telemetry Stream | `price_telemetry_service.get_latest_price()` | **Implemented** (`Telemetry.jsx`) |
| **Trade Ticket** | Price Formatter | `precision_engine.format_for_display()` | **Implicit** (Used in various inputs) |

## Dependencies
- `decimal`: **Mandatory** for all internal math.
- `sqlalchemy`: Connectivity to the TimescaleDB instance.

## Usage Examples

### Normalizing a Price for Display
```python
from services.pricing.precision_engine import PrecisionEngine

# Raw float input from API
raw_price = 1.09214567 

# Normalize for EUR/USD (5 decimals)
norm_price = PrecisionEngine.normalize_price("EURUSD", raw_price)
display_str = PrecisionEngine.format_for_display("EURUSD", raw_price)

print(f"Stored: {norm_price} (Type: {type(norm_price)})")
print(f"Displayed: {display_str}")
```

### Storing a Market Tick
```python
from services.price_telemetry_service import PriceTelemetryService

telemetry = PriceTelemetryService()

# Store a new tick from WebSocket
telemetry.store_tick(
    symbol="BTC-USD",
    price=42069.50,
    volume=0.5,
    source="COINBASE"
)

# Retrieve latest
latest = telemetry.get_latest_price("BTC-USD")
print(f"Latest BTC Price: ${latest:,.2f}")
```
