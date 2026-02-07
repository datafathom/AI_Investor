# Strategist Department Agents (`strategist/strategist_agents.py`)

The Strategist department is the "Quant Lab," where trading strategies are defined, optimized, and stress-tested.

## Backtest Autopilot Agent (Agent 3.1)
### Description
High-performance vectorized backtesting engine using Polars.
- **Benchmark**: Executes a 10-year SMA cross strategy in <2 seconds.

---

## Optimizer Agent (Agent 3.2)
### Description
Runs grid searches and genetic algorithms to find optimal strategy parameters.
- **Performance**: Identifies top 5 parameter sets in <10 seconds.

---

## Correlation Detective Agent (Agent 3.3)
### Description
Builds and maintains the "Correlation Web" (Neo4j), identifying hidden dependencies between assets.

---

## Risk Manager Agent (Agent 3.4)
### Description
Calculates Value at Risk (VaR) and overall portfolio risk metrics.

---

## Alpha Researcher Agent (Agent 3.5)
### Description
Conducts factor analysis and discovers new alpha signals in historical data.

---

## Blueprint Architect Agent (Agent 3.6)
### Description
The visual strategy builder that manages `StrategyBlueprints` and validates them for logical consistency.
