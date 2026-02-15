# Interest Rate Arbitrageur (Agent 18.3)

## ID: `interest_rate_arbitrageur`

## Role & Objective
The 'Yield Hunter'. Dynamically moves idle cash to whichever venue (DeFi or TradFi) offers the highest risk-adjusted yield, ensuring no dollar stays "lazy."

## Logic & Algorithm
- **Yield Comparison**: Scrapes APY/APR from a universe of 50+ approved lending pools and high-yield savings accounts.
- **Risk Weighting**: Discounts high-yield sources based on the Sentry's "Counterparty Risk" rating.
- **Yield Pivot**: Executes a funds-transfer if the yield delta between two venues exceeds 50 basis points (0.50%) after factoring in gas/transfer fees.

## Inputs & Outputs
- **Inputs**:
  - `rate_landscape` (Data): Live yields from Aave, Compound, Onyx, and select banks.
- **Outputs**:
  - `yield_pivot_signal` (Dict): Move X amount from Source A to Source B.

## Acceptance Criteria
- Identify the highest-yielding "Safe" venue for idle cash within 60 minutes of a rate change.
- Ensure that 100% of "Lazy Cash" (idle for > 24h) is earning at least the benchmark SOFR/Repo rate.
