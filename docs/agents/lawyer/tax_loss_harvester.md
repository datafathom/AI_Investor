# Tax Loss Harvester (Agent 11.4)

## ID: `tax_loss_harvester`

## Role & Objective
The 'Deduction Finder'. Identifies unrealized losses in the portfolio that can be strategically harvested to offset capital gains and reduce total tax liability.

## Logic & Algorithm
- **Loss Scanning**: Monitors every open position for unrealized losses exceeding a user-defined threshold (e.g., $1,000).
- **Gain Offsetting**: Matches identified losses against realized capital gains from the current tax year.
- **Efficiency Scoring**: Prioritizes harvests that provide the most significant immediate tax benefit (Short-term vs. Long-term).

## Inputs & Outputs
- **Inputs**:
  - `open_positions_pnl` (Dict): Real-time unrealized profit/loss.
  - `realized_gains_ytd` (float): Current tax liability baseline.
- **Outputs**:
  - `harvest_recommendations` (List): Specific tickers and lot numbers to sell for a tax offset.

## Acceptance Criteria
- Identify 100% of harvestable losses that meet the defined "Efficiency Threshold".
- Coordinate with the Wash-Sale Watchdog to ensure no harvested losses are accidentally negated.
