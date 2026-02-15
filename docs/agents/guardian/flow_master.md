# Flow Master (Agent 10.2)

## ID: `flow_master`

## Role & Objective
The 'Cash Sweep' engine. Monitors account balances and sweeps excess funds from low-yield checking accounts into high-yield savings (HYS) or brokerage silos.

## Logic & Algorithm
- **Balance Monitoring**: Checks bank balances daily for "Excess Liquidity" above the user-defined safety floor.
- **Target Allocation**: Identifies the highest-yield "Silo" currently available for idle cash.
- **Transfer Execution**: Stages ACH or Wire transfers to optimize interest arbitrage.

## Inputs & Outputs
- **Inputs**:
  - `bank_balances` (Dict): Real-time cash positions.
  - `yield_rates` (Dict): Current interest rates across all accounts.
- **Outputs**:
  - `transfer_orders` (List): Recommended fund movements.

## Acceptance Criteria
- Sweep funds into high-yield accounts within 24 hours of a balance exceeding the safety floor.
- Maintain a "Solvency Buffer" in the primary checking account at 100% of the defined threshold.
