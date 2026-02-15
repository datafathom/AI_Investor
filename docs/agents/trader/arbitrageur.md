# Arbitrageur (Agent 5.3)

## ID: `arbitrageur`

## Role & Objective
The "Inefficiency Exploiter". Captures risk-free profit from price discrepancies across different venues (CEX vs DEX) or related asset pairs.

## Logic & Algorithm
1. **Multi-Venue Scan**: Simultaneously monitors prices for the same asset across Coinbase, Binance, Uniswap, etc.
2. **Triangular Logic**: Scans for loops in currency pairs that result in a net gain (e.g., BTC-ETH-USDT-BTC).
3. **Fee-Aware Execution**: Only triggers trades if the profit exceeds the combined gas and transaction fees by at least 20%.

## Inputs & Outputs
- **Inputs**:
  - `multisource_prices` (Dict): Fragmented venue data.
- **Outputs**:
  - `arb_execution` (Dict): Simultaneous buy/sell orders.
  - `net_profit_estimate` (float): Net gain after all fees.

## Acceptance Criteria
- Arbitrage execution must be atomic (simultaneous) across multiple venues to prevent "legged" risk.
- Net profit calculations must include real-time gas/network fee estimates.
