# Backend Service: Valuation (The Appraisal Desk)

## Overview
The **Valuation Service** calculates intrinsic value using valuation models. Its centerpiece is a 2-stage Discounted Cash Flow (DCF) engine powered by live financial data.

## Core Components

### 1. DCF Engine (`dcf_engine.py`)
- **Data Integration**: Fetches financials via SEC Scraper.
- **2-Stage DCF Model**: Projects cash flows for 5 years, then calculates terminal value.
- **Margin of Safety**: Compares fair value to current price.

### 2. Supporting Modules
- `safe_calc.py`: SAFE note conversion calculations.
- `secondary_market.py`: Pre-IPO secondary share valuation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Research Dashboard** | Fair Value Badge | `dcf_engine.calculate_intrinsic_value()` | **Implemented** |

## Usage Example

```python
from services.valuation.dcf_engine import DCFEngine

engine = DCFEngine()

result = engine.calculate_intrinsic_value("AAPL")

print(f"Current Price: ${result['current_price']:.2f}")
print(f"Fair Value: ${result['fair_value']:.2f}")
print(f"Margin of Safety: {result['margin_of_safety_pct']:.1f}%")
```
