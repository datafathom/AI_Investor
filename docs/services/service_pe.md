# Backend Service: Private Equity (Deal Engine)

## Overview
The **Private Equity (PE) Service** provides the financial modeling infrastructure for illiquid investments. It mimics the analytical capabilities of a PE associate, enabling the autonomous system to evaluate "buyout" opportunities, project returns (IRR/MOIC), and manage complex distribution waterfalls between General Partners (GPs) and Limited Partners (LPs).

## Core Components

### 1. LBO Engine (`lbo_engine.py`)
The Buyout Calculator.
- **Return Projection**: Calculates Internal Rate of Return (IRR) and Multiple on Invested Capital (MOIC) based on entry/exit multiples, leverage ratios, and operational improvements.
- **Deleveraging Model**: Simulates the pay-down of debt using free cash flow over the hold period.

### 2. Waterfall Engine (`waterfall_engine.py`)
The Distribution Manager.
- **Tiered Splits**: Implements standard PE waterfall logic:
    1.  **Return of Capital**: LPs get 100% of cash flow until they recover their initial investment.
    2.  **Preferred Return**: LPs get a "hurdle rate" (e.g., 8%).
    3.  **GP Catch-up**: The Deal Sponsor gets their share.
    4.  **Carried Interest**: Splits remaining profits (e.g., 80/20).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Brokerage** | P&L Waterfall | `waterfall_engine.calculate_distributions()` | **Implemented** (`PLWaterfall.jsx`) |
| **Deal Room** | LBO Model | `lbo_engine.project_deal_returns()` | **Missing** (Logic exists, UI pending) |

## Dependencies
- `decimal`: **Critical** for financial precision. Floating point errors in waterfall calculations are legally unacceptable.

## Usage Examples

### Projecting an LBO Return
```python
from services.pe.lbo_engine import LBOEngine
from decimal import Decimal

lbo = LBOEngine()

# Project returns for a $10M EBITDA company bought at 10x
result = lbo.project_deal_returns(
    entry_ebitda=Decimal('10000000'),
    entry_multiple=Decimal('10.0'),
    equity_contribution_pct=Decimal('0.40'), # 40% Equity / 60% Debt
    exit_multiple=Decimal('12.0'),           # Ops Improvement
    years=5,
    revenue_growth_pct=Decimal('0.05')       # 5% YoY Growth
)

print(f"Projected MOIC: {result['moic']}x")
print(f"Projected IRR: {result['irr_pct']}%")
```

### Calculating GP/LP Distributions
```python
from services.pe.waterfall_engine import WaterfallEngine

distributor = WaterfallEngine()

# Distribute $500k of cash flow from a portfolio company
payout = distributor.calculate_distributions(
    distributable_cash=Decimal('500000'),
    invested_capital=Decimal('2000000')
)

print(f"LP Share: ${payout['total_lp_dist']:,.2f}")
print(f"GP Promote: ${payout['total_gp_dist']:,.2f}")
```
