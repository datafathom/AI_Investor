# Physicist Department Agents (`physicist/physicist_agents.py`)

The Physicist department is the "Volatility Engine," managing complex mathematical layers of risk, Options Greeks, and tail-risk probability.

## Theta Collector Agent (Agent 5.1)
### Description
Monitors portfolio time-decay (Theta) and harvests yield.
- **SLA**: Daily P&L report must track Theta with <$1.00 variance.

---

## Volatility Surface Mapper Agent (Agent 5.2)
### Description
Generates 3D data meshes for vizualizing Implied Volatility across different strikes and expiries.
- **Performance**: Mesh generation must have <50ms latency.

---

## Delta Hedger Agent (Agent 5.4)
### Description
Calculates net portfolio Delta and stages rebalancing trades.
- **Enforcement**: Stages hedge trades when Delta drift exceeds 10% thresholds.

---

## Black-Scholes Solver Agent (Agent 5.5)
### Description
A dedicated compute agent for high-frequency Black-Scholes calculations (Option pricing and Greeks).

---

## Black-Swan Watcher Agent (Agent 5.6)
### Description
Monitors for "Tail-Risk" and extreme market events using IV heuristics.
- **Risk Levels**: Categorizes risk as NORMAL, ELEVATED, or EXTREME.
