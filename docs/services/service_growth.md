# Backend Service: Growth

## Overview
The **Growth Service** is the platform's primary engine for modeling and tracking private equity and venture capital investments. It handles the complex mathematics of cap-table management, funding round dilution, and exit waterfalls, enabling institutional and UHNW clients to forecast the longitudinal growth of their private "Venture" holdings.

## Core Components

### 1. Venture Modeling Engine (`venture_service.py`)
The platform's dedicated calculator for private market liquidity events.
- **Exit Waterfall Logic**: Automatically resolves the distribution of proceeds during a liquidity event (M&A/IPO). It accounts for **Liquidation Preferences** (1x, 2x, etc.), **Participating Preferred** rights, and the remaining common pool.
- **Dilution Simulator**: Models the impact of new funding rounds on existing shareholders. It calculates pre/post-money valuations, price-per-share increments, and the resulting dilution percentages for early-stage investors.
- **Share Class Management**: Defines the specific rights and preferences of different investment series (e.g., Series A, Seed, Common).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Growth/Venture Station** | Exit Waterfall Simulator | `venture_service.calculate_waterfall()` |
| **Growth/Venture Station** | Cap-Table Dilution Tool | `venture_service.simulate_dilution()` |
| **Portfolio Detail** | Private Round Timeline | `venture_service` (Round history) |
| **Strategist Station** | Potential Exit Valuation | `venture_service.calculate_waterfall()` |

## Dependencies
- `pydantic`: Uses `ShareClass` models to enforce structure on investment terms.

## Usage Examples

### Running an Exit Waterfall Calculation
```python
from services.growth.venture_service import get_venture_service, ShareClass

growth_svc = get_venture_service()

# 50M Exit Scenario
cap_table = [
    ShareClass(name="Series A", shares=1_000_000, price_per_share=5.0, liquidation_preference=1.0, is_participating=True),
    ShareClass(name="Seed", shares=500_000, price_per_share=2.0, is_preferred=True)
]

waterfall = growth_svc.calculate_waterfall(
    exit_value=50_000_000,
    cap_table=cap_table,
    common_shares=5_000_000
)

print(f"Distributable Proceeds: ${waterfall['exit_value']:,.2f}")
for name, payout in waterfall['payouts'].items():
    print(f"{name}: Total Payout ${payout['total_payout']:,.2f}")
```

### Simulating a Series B Dilution
```python
from services.growth.venture_service import VentureService

vs = VentureService()

# 10M new investment on 40M pre-money
round_sim = vs.simulate_dilution(
    current_shares=10_000_000,
    new_investment=10_000_000,
    pre_money_valuation=40_000_000
)

print(f"Post-Money Valuation: ${round_sim['post_money']:,.2f}")
print(f"Dilution to Existing: {round_sim['dilution_percentage']:.2f}%")
print(f"New Share Price: ${round_sim['price_per_share']:.2f}")
```
