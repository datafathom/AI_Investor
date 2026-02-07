# Backend Service: Private Markets (The Illiquidity Engine)

## Overview
The **Private Markets Service** manages the valuation and risk assessment of assets that cannot be sold instantly (Private Equity, Venture Capital, Real Estate). Its primary job is to ensure the **Illiquidity Premium** is captured—meaning the user is adequately compensated (typically +300-500 bps) for locking up their capital for years.

## Core Components

### 1. Premium Optimizer (`premium_optimizer.py`)
The Reality Check.
- **Illiquidity Premium Calculator**: Compares the expected Internal Rate of Return (IRR) of a private deal against a public market equivalent (Public Market Equivalent - PME). If the spread is < 300bps, the deal is rejected.
- **Return Unsmoothing**: Private assets often report artificially stable returns (e.g., "Up 2% every quarter") because they are appraised infrequently. This component uses the **Geltner Formula** to reverse-engineer the *true* volatility, ensuring the Risk Parity models don't overweight these assets due to false low-volatility signals.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Asset Entry** | Valuation Form | `premium_optimizer.calculate_illiquidity_premium()` | **Implemented** (`PrivateEntry.jsx`) |
| **Risk Dashboard** | True Volatility | `premium_optimizer.unsmooth_returns()` | **Implicit** (Data flows to Risk Engine) |

## Dependencies
- `decimal`: Required for precise IRR spread calculations.

## Usage Examples

### Evaluating a PE Fund
```python
from services.private_markets.premium_optimizer import PremiumOptimizer
from decimal import Decimal

optimizer = PremiumOptimizer()

# PE Fund offers 15% IRR, while S&P 500 expects 10%
evaluation = optimizer.calculate_illiquidity_premium(
    private_irr=Decimal('0.15'),
    public_equiv_irr=Decimal('0.10')
)

print(f"Premium: {evaluation['premium_bps']} bps")
print(f"Is Sufficient? {evaluation['is_sufficient']}") # True (500 > 300)
```

### Unsmoothing Real Estate Returns
```python
# Quarterly appraisals show very low volatility
smoothed_returns = [0.02, 0.021, 0.019, 0.022]

# Reveal the true volatility (assuming 0.5 autocorrelation)
true_returns = optimizer.unsmooth_returns(smoothed_returns, rho=0.5)

print(f"Smoothed: {smoothed_returns}")
print(f"True Vol: {true_returns}") 
# Result will be much more volatile
```
