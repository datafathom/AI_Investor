# Cap-Table Modeler (Agent 7.2)

## ID: `cap_table_modeler`

## Role & Objective
The 'Dilution Specialist'. Analyzes complex equity structures and liquidation preferences to determine the effective price per share.

## Logic & Algorithm
- Models 'Waterfall' scenarios for various exit valuations.
- Accounts for participant dilution in future funding rounds.
- Flags high-risk liquidation preferences (e.g., >1x Participating Preferred).

## Inputs & Outputs
- **Inputs**:
  - `raw_cap_table` (Dict): Stakeholders, share classes, and preferences.
  - `exit_valuation` (float): Hypothetical company sale price.
- **Outputs**:
  - `net_payout_per_share` (float): Expected return for the user's specific class.
  - `dilution_sensitivity` (float): Impact of next round on current stake.

## Acceptance Criteria
- Calculate payout waterfalls for cap tables with up to 50 stakeholders in < 1 second.
- Precision of net payout must match official company spreadsheets to 4 decimal places.
