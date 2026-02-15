# Tax Reserve Calculator (Agent 18.5)

## ID: `tax_reserve_calculator`

## Role & Objective
The 'Provisional Accountant'. Calculates realize capital gains and other income in real-time, setting aside appropriate USD reserves to ensure the system is always liquid for tax day.

## Logic & Algorithm
- **Gains Tracking**: Calculates the cost-basis and profit for every closed position (FIFO/LIFO as per Lawyer's rules).
- **Reserve Partitioning**: Applies a "Blended Tax Rate" to all net-profits and requests an envelope transfer.
- **Quarterly Forecasting**: Projects total tax liability for the fiscal year based on current run-rates.

## Inputs & Outputs
- **Inputs**:
  - `realized_pnl` (Data).
- **Outputs**:
  - `required_reserve_delta` (float): The amount to move to the Tax Envelope.

## Acceptance Criteria
- Maintain a reserve within 5% of the actual tax liability at all times.
- Update the "Tax Forecast" every 24 hours based on system trading performance.
