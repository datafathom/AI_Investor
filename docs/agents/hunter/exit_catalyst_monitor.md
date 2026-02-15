# Exit Catalyst Monitor (Agent 7.3)

## ID: `exit_catalyst_monitor`

## Role & Objective
The 'IPO Watcher'. Monitors news and regulatory filings for signs that a private holding is preparing for a liquidity event (M&A or IPO).

## Logic & Algorithm
- Tracks S-1 filing activity and 'Confidential IPO' rumors.
- Monitors the 'Secondary Market' (EquityZen, Forge) for price discovery.
- Signals the optimal window to sell secondary shares.

## Inputs & Outputs
- **Inputs**:
  - `portfolio_private_assets` (List): List of companies currently held.
- **Outputs**:
  - `liquidity_probability` (float): Likelihood of an exit within 12 months.
  - `catalyst_events` (List): Specific news items indicating an upcoming exit.

## Acceptance Criteria
- Detect S-1 filings within 5 minutes of public release.
- Provide a secondary market price pulse for 80% of current private holdings.
