# Backend Service: Simulation (The What-If Engine)

## Overview
The **Simulation Service** runs "what-if" scenarios to stress-test trading strategies and portfolios. It contains **17 specialized simulators** covering Monte Carlo projections, geopolitical shocks, liquidity crises, and reflexivity dynamics.

## Core Components (Selected)

### 1. Monte Carlo Simulator (`monte_carlo_sim.py`)
- **Trade Sequence Simulation**: Projects a strategy's win rate and R-multiples forward over 1,000+ trades.
- **Ruin Detection**: Stops simulation if equity drops 50%, flagging the strategy as high-risk.
- **Max Drawdown Tracking**: Records the deepest equity dip.

### 2. Class Risk Simulator (`class_risk_sim.py`)
- Simulates correlated drawdowns across asset classes.

### 3. Geopolitical Simulator (`geopolitical_sim_engine.py`)
- Models the impact of war, sanctions, or regime change on portfolio exposure.

### Other Key Modules
- `reflexivity_sim.py`: Models passive fund flow dynamics.
- `power_law_sim.py`: Simulates fat-tail events (Black Swans).
- `liquidity_crisis.py`: Models forced selling spirals.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategy Lab** | Monte Carlo Chart | `monte_carlo_sim.run_simulation()` | **Implemented** (`MonteCarlo.jsx`) |
| **Risk Dashboard** | Scenario Analyzer | `geopolitical_sim_engine` | **Partially Implemented** |

## Usage Example

```python
from services.simulation.monte_carlo_sim import MonteCarloSimulator

result = MonteCarloSimulator.run_simulation(
    win_rate=0.55,       # 55% win rate
    avg_win_r=2.0,       # Win 2R on average
    avg_loss_r=1.0,      # Lose 1R on average
    initial_balance=100000,
    risk_per_trade_pct=0.01, # Risk 1% per trade
    num_trades=1000
)

print(f"Final Equity: ${result['final_equity']:,.2f}")
print(f"Max Drawdown: {result['max_drawdown_pct']}%")
print(f"Ruin Occurred: {result['ruin_occurred']}")
```
