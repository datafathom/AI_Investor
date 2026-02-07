# Backend Service: Physicist (Quant Lab)

## Overview
The **Physicist Service** is the specialized research arm of the system, dedicated to advanced derivatives pricing and market thermodynamics. While the `options` service handles general flow and strategy P&L, the **Physicist** focuses on the raw mathematics of volatility, offering a high-performance Black-Scholes-Merton engine optimized for real-time Greeks and Implied Volatility (IV) surface calibration.

## Core Components

### 1. Options Pricing Engine (`options_pricing_service.py`)
The Speed Demon.
- **Black-Scholes-Merton**: Implementation of the standard pricing model for European options.
- **Real-Time Greeks**: Calculates secondary risk metrics (Rho, Vega per 1% vol change) efficiently.
- **Newton-Raphson Solver**: Solves for Implied Volatility (IV) given a market price, essential for constructing surface maps.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Physicist Workstation** | Expected Move | `options_pricing_service.black_scholes()` | **Implemented** (`PhysicistExpectedmove.jsx`) |
| **Physicist Workstation** | Volatility Surface | `options_pricing_service.calculate_implied_volatility()` | **Implemented** (`PhysicistMorphing.jsx`) |

## Dependencies
- `scipy.stats.norm`: For Gaussian cumulative distribution functions.
- `math`: Standard library used for maximum speed (avoiding numpy overhead for single-contract pricing).

## Usage Examples

### Pricing a Call Option
```python
from services.physicist.options_pricing_service import get_options_pricing_service

pricer = get_options_pricing_service()

# Price a Call: Spot=100, Strike=100, Time=1 year, RiskFree=5%, Vol=20%
result = pricer.black_scholes(
    S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.20, option_type="call"
)

print(f"Theoretical Price: ${result['price']:.2f}")
print(f"Delta: {result['delta']:.4f}")
print(f"Gamma: {result['gamma']:.4f}")
```

### Solving for Implied Volatility
```python
# If the market price is $10.50, what is the Implied Vol?
iv = pricer.calculate_implied_volatility(
    market_price=10.50,
    S=100.0, K=100.0, T=1.0, r=0.05, option_type="call"
)

print(f"Implied Volatility: {iv:.2%}")
```
