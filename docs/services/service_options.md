# Backend Service: Options (Derivatives Engine)

## Overview
The **Options Service** provides the "Hedge Fund" capabilities of the Sovereign OS. It goes beyond simple price tracking to analyze second-order derivatives (Greeks) and market structure (Gamma Exposure). It enables the system to detect "Dealer Hedging Pressure" (GEX), price complex strategies (Straddles, Iron Condors), and visualize implied volatility surfaces.

## Core Components

### 1. GEX Calculator (`gex_calculator.py`)
The Market Structure Engine.
- **Gamma Exposure (GEX)**: Calculates the total dollar value of Gamma dealers must hedge for every 1% move in the underlying.
- **Gamma Flip Detection**: Identifies the precise price level where dealers switch from being "Long Gamma" (stabilizing flows, buy-the-dip) to "Short Gamma" (accelerating flows, sell-the-rip).
- **Regime Identification**: Classifies the market state as `LONG_GAMMA` (Low volatility expected) or `SHORT_GAMMA` (High volatility danger zone).

### 2. Options Analytics (`options_analytics_service.py`)
The Pricing Kernel.
- **Real-Time Greeks**: Calculates Delta, Gamma, Theta, Vega, and Rho for individual options and complex multi-leg strategies using the Black-Scholes model.
- **Probability of Profit (PoP)**: Estimates the statistical likelihood of a trade ending In-The-Money (ITM) based on current Implied Volatility (IV).
- **P&L Simulation**: Projects profit/loss across different price and time horizons (e.g., "What if SPY drops 2% tomorrow vs. next week?").

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Market Dashboard** | GEX Profile | `gex_calculator.calculate_gex()` | **Implemented** (`GEXProfile.jsx`) |
| **Trading Terminal** | Options Analysis | `options_analytics_service.analyze_strategy()` | **Implemented** (`OptionsChainWidget.jsx`) |
| **Flow Monitor** | Unusual Whales | `options_analytics_service` (Flow data aggregator) | **Implemented** (`OptionsFlowTable.jsx`) |

## Dependencies
- `scipy.stats.norm`: Used for Cumulative Distribution Functions (CDF) in Black-Scholes pricing.
- `numpy`: Vectorized calculations for efficient pricing of entire option chains.

## Usage Examples

### Calculating Gamma Exposure for SPY
```python
from services.options.gex_calculator import GEXCalculator

# Mock Option Chain Data
chain = [
    {'strike': 450, 'gamma': 0.05, 'open_interest': 15000, 'type': 'CALL'},
    {'strike': 450, 'gamma': 0.04, 'open_interest': 12000, 'type': 'PUT'},
    # ... more contracts
]

gex_result = GEXCalculator.calculate_gex(spot_price=452.50, options_chain=chain)

print(f"Total Dealer GEX: ${gex_result['total_gex']:,.0f}")
print(f"Gamma Flip Level: ${gex_result['gamma_flip_price']:.2f}")
print(f"Market Regime: {gex_result['market_regime']}")
```

### Analyzing an Iron Condor Strategy
```python
from services.options.options_analytics_service import get_options_analytics_service
from schemas.options import OptionsStrategy, OptionLeg

analytics = get_options_analytics_service()

# Define Strategy
condor = OptionsStrategy(legs=[
    OptionLeg(symbol="SPY", strike=440, option_type="put", action="sell", quantity=1),
    OptionLeg(symbol="SPY", strike=435, option_type="put", action="buy", quantity=1),
    OptionLeg(symbol="SPY", strike=460, option_type="call", action="sell", quantity=1),
    OptionLeg(symbol="SPY", strike=465, option_type="call", action="buy", quantity=1)
])

# Get Greeks & P&L
analysis = await analytics.analyze_strategy(
    strategy=condor,
    underlying_price=450.00,
    days_to_expiration=30,
    volatility=0.18
)

print(f"Total Theta: {analysis.greeks.total_theta:.4f}")
print(f"Max Profit probability: {analysis.probability_profit:.1%}")
```
