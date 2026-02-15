# Liquidity Provider (Agent 18.6)

## ID: `liquidity_provider`

## Role & Objective
The 'Market Greaser'. Manages the cash-on-hand needed for daily operations (bills, tiny trades, fees) without forcing the sale of long-term assets.

## Logic & Algorithm
- **Buffer Management**: Maintains a "Liquidity Buffer" in stablecoins (USDC/USDT) equal to 5x the average daily burn rate.
- **Withdrawal Ladder**: Orchestrates the movement of capital from high-yield lockups back to liquid accounts on a staggered timeline.
- **Just-in-Time Funding**: Detects when the Trader is about to execute a high-conviction signal and ensures funds are in the right sub-account.

## Inputs & Outputs
- **Inputs**:
  - `burn_rate_stats` (float): Average daily operational cost.
  - `pending_trader_intent` (List): Incoming trade requests.
- **Outputs**:
  - `liquidity_status` (str): 'LIQUID' or 'CRITICAL_LOW'.
  - `ready_capital_audit` (float): Total immediate USD availability.

## Acceptance Criteria
- Ensure 0% "Insufficient Funds" errors for trades with a "High" confidence score.
- Maintain the "Liquidity Buffer" within 10% of the target range 99% of the time.
