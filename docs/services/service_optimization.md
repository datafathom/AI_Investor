# Backend Service: Optimization (Quant Engine)

## Overview
The **Optimization Service** is the mathematical core of the investment process. It translates high-level strategic goals (e.g., "Maximize Sharpe Ratio") into precise asset allocation weights using advanced quantitative models like Mean-Variance Optimization (MVO), Black-Litterman, and Risk Parity. It also actively monitors portfolios for drift and generates tax-efficient rebalancing orders.

## Core Components

### 1. Portfolio Optimizer (`portfolio_optimizer_service.py`)
The Math Kernel.
- **Supported Models**:
    - **Mean-Variance (Markowitz)**: The classic approach to finding the Efficient Frontier.
    - **Risk Parity**: Allocates capital such that each asset contributes equally to overall portfolio risk (great for all-weather portfolios).
    - **Minimum Variance**: Seeks the absolute lowest volatility portfolio.
- **Constraint Handling**: Supports real-world constraints like `long_only` (no shorting), `position_limits` (e.g., max 5% per stock), and `sector_exposure`.

### 2. Rebalancing Engine (`rebalancing_service.py`)
The Drift Corrector.
- **Drift Monitoring**: Continuously compares Current Weights vs. Target Weights. If the deviation exceeds a threshold (default 5%), it flags the portfolio for rebalancing.
- **Trade Generation**: Auto-calculates the precise BUY/SELL orders needed to restore alignment.
- **Approval Workflow**: Enforces a safety check—if total trade value > $10,000, it requires explicit user approval before execution.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Strategist Workstation** | Rebalance Tool | `rebalancing_service.generate_rebalancing_recommendation()` | **Implemented** (`StrategistRebalance.jsx`) |
| **Brokerage** | Tax Lot Optimizer | `rebalancing_service._estimate_tax_impact()` | **Implemented** (`TaxLotOptimizer.jsx`) |
| **Institutional** | Allocation Wheel | `portfolio_optimizer_service.optimize()` | **Implemented** (`AssetAllocationWheel.jsx`) |

## Dependencies
- `numpy`: Matrix operations and linear algebra.
- `scipy.optimize`: The solver engine (SLSQP method) for minimization problems.
- `cvxpy`: (Future) For more complex convex optimization problems.

## Usage Examples

### Optimizing a Portfolio for Max Sharpe
```python
from services.optimization.portfolio_optimizer_service import get_optimizer_service

optimizer = get_optimizer_service()

result = await optimizer.optimize(
    portfolio_id="pf_growth_aggr",
    objective="maximize_sharpe",
    method="mean_variance",
    risk_model="historical"
)

for symbol, weight in result.optimal_weights.items():
    print(f"{symbol}: {weight*100:.1f}%")

print(f"Exp Return: {result.expected_return:.2%}")
print(f"Exp Volatility: {result.expected_risk:.2%}")
```

### Checking for Drift
```python
from services.optimization.rebalancing_service import get_rebalancing_service

rebalancer = get_rebalancing_service()

# Check if portfolio has drifted > 3%
needs_rebalance = await rebalancer.check_rebalancing_needed(
    portfolio_id="pf_retirement",
    threshold=0.03
)

if needs_rebalance:
    rec = await rebalancer.generate_rebalancing_recommendation("pf_retirement")
    print(f"Drift Detected: {rec.drift_percentage:.2f}%")
    print(f"Recommended Trades: {len(rec.recommended_trades)}")
```
