# Trader Department Agents (`trader/trader_agents.py`)

The Trader department is the "Execution Layer," responsible for order routing, fill tracking, and algorithmic execution.

## Order General Agent (Agent 4.1)
### Description
The supreme commander of order flow, responsible for routing orders to optimal venues (NYSE, NASDAQ, etc.) using Smart Order Routing (SOR).
- **Latency**: SOR routing under 50ms.

---

## Fill Tracker Agent (Agent 4.2)
### Description
Monitors and reconciles all order fills in real-time.
- **Accuracy**: 100% reconciliation against broker records.
- **Positioning**: Updates the system’s net position immediately upon fill.

---

## Algo-Executor Agent (Agent 4.3)
### Description
Executes large orders using algorithmic profiles (TWAP, VWAP, Iceberg) to minimize market impact.

---

## Hedger Agent (Agent 4.4)
### Description
Monitors net portfolio exposure and executes automatic hedging trades (e.g., buying SQQQ if exposure is too long).

---

## Arbitrageur Agent (Agent 4.5)
### Description
Identifies and executes latency or cross-venue arbitrage opportunities.

---

## Market Maker Agent (Agent 4.6)
### Description
Provides two-sided liquidity and manages bid/ask spreads to minimize slippage on internal crossings.
