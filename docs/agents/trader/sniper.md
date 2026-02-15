# Sniper (Agent 5.1)

## ID: `sniper`

## Role & Objective
The "Precision Entry" engine. The Sniper's goal is to execute orders at the exact moment where liquidity and price alignment hit optimal levels to minimize market impact.

## Logic & Algorithm
1. **L2 Monitoring**: Constant surveillance of Level 2 order books for price improvement opportunities.
2. **Iceberg Execution**: Uses hidden/iceberg orders to prevent front-running by predatory HFT bots.
3. **Micro-second Sync**: Matches entry signals from the quantitative stack with sub-millisecond precision.

## Inputs & Outputs
- **Inputs**:
  - `target_order` (Dict): Symbol, Side, Size, and Limit.
  - `live_order_book` (Dict): Real-time bid/ask depth.
- **Outputs**:
  - `execution_status` (Dict): Fill details.
  - `slippage_report` (float): Actual fill vs mid-price.

## Acceptance Criteria
- Execute orders within 10ms of receiving a high-conviction signal from the Orchestrator.
- Maintain average slippage < 2 basis points on liquid assets.
