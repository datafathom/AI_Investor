# Backend Service: Economics

## Overview
The **Economics Service** provides specialized macroeconomic and behavioral modeling tailored for the Ultra-High-Net-Worth (UHNW) segment. It moves beyond standard retail metrics (like CPI) to track the **CLEW Index** (Cost of Living Extremely Well) and provides structural insights into **Social Class Maintenance (SCM)**, ensuring that investment strategies account for the actual "lifestyles of the extremely wealthy" inflation.

## Core Components

### 1. CLEW Index Service (`clew_index_svc.py`)
Proprietary inflation tracking for the 0.1%.
- **UHNW Basket**: Tracks a specialized inflation basket including:
    - **Private Aviation**: Fuel, hangarage, and crew cost volatility.
    - **Tuition**: Historical 7% CAGR of Ivy League and elite primary education.
    - **Concierge Staff**: Wages for domestic staff and wealth management offices.
    - **Luxury Real Estate**: Maintenance and tax inflation for prime property holdings.
- **Inflation Delta**: Automatically calculates the spread between standard CPI and the CLEW Index to provide a "Real Yield" adjusted for high-end lifestyle maintenance.

### 2. Social Class Maintenance (SCM) Service (`scm_service.py`)
Predictive modeling for inter-generational wealth retention.
- **SCM Score**: A critical metric calculated as: `(Portfolio Yield - CLEW Inflation) / Lifestyle Burn`.
    - **Score > 1.0**: The family's wealth is expanding relative to their social class costs.
    - **Score < 1.0**: "Social Dilution" is occurring; the lifestyle is currently unsustainable by current portfolio performance.
- **Lifestyle Burn Projection**: Models how current spending will compound over 5, 10, and 20 years when adjusted for high-beta luxury inflation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **UHNW Life Dashboard** | Personal Inflation Pulse | `clew_index_service.get_uhnwi_inflation_rate()` |
| **Strategist Station** | Social Class Health Meter | `scm_service.calculate_scm_score()` |
| **Planning Station** | Burn Projection Plot | `scm_service.project_lifestyle_burn()` |
| **Estate Detail** | Basket Allocator | `clew_index_service.calculate_personal_inflation()` |

## Dependencies
- `decimal`: Essential for high-precision inflation compounding and financial score calculations.
- `logging`: Records structural economic shifts for the platform's macro-agent history.

## Usage Examples

### Calculating an SCM Score for a SFO
```python
from services.economics.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# Portfolio yields 12%, Lifestyle burn is 4% of AUM
# CLEW Inflation is calculated internally (typically 6-8%)
score = scm.calculate_scm_score(
    portfolio_yield_pct=Decimal("0.12"),
    lifestyle_burn_pct=Decimal("0.04")
)

if score > 1.0:
    print(f"Status: Growth. SCM Score: {score}")
else:
    print(f"Status: Dilution Risk. SCM Score: {score}")
```

### Projecting Future Lifestyle Costs
```python
from services.economics.clew_index_svc import get_clew_index_service
from decimal import Decimal

clew_svc = get_clew_index_service()
current_spend = Decimal("2500000") # $2.5M annual burn

# Project spend in 10 years adjusted for CLEW inflation
rate = Decimal(str(clew_svc.get_uhnwi_inflation_rate()))
projected = current_spend * ((1 + rate) ** 10)

print(f"Current Spend: ${current_spend:,.2f}")
print(f"Projected Spend (10yrs): ${projected:,.2f} at {rate:.2%} CLEW rate")
```
