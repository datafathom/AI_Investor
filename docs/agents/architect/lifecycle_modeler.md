# LifeCycle Modeler Agent (`architect/architect_agents.py`)

## Description
The `LifeCycleModelerAgent` (Agent 7.1) is responsible for long-term financial planning and multi-decade wealth projection. It helps the user model the path to Financial Independence (FI) and retirement.

## Role in Department
Acts as the "Strategic Visionary" in the Architect department, focusing on macro-level wealth goals rather than short-term trades.

## Input & Output
- **Input**: Net worth, current age, retirement target age, monthly savings rate, and expected annual returns.
- **Output**: Detailed projection data including year-over-year wealth accumulation, "Dead Simple" FI status, and estimated retirement year.

## Integration & Logic
- **Simulation**: Uses compound interest models to simulate financial health over 30-50 year horizons.
- **Goal Tracking**: Emits status updates comparing current progress against the "Retirement Goal" threshold.
- **Departmental Flow**: Provides the long-term context that informs the `Strategist`'s risk tolerance.
