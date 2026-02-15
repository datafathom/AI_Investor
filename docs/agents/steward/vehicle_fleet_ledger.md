# Vehicle Fleet Ledger (Agent 9.2)

## ID: `vehicle_fleet_ledger`

## Role & Objective
The 'Mobility Auditor'. Tracks car valuations, fuel efficiency, and depreciation schedules for the user's vehicle fleet.

## Logic & Algorithm
- **Depreciation Modeling**: Uses standard mileage-based and age-based depreciation curves to estimate private vehicle value.
- **Operating Cost Analysis**: Aggregates gas, insurance, and charging costs to calculate "Cost Per Mile" (CPM).
- **Secondary Market Pulse**: Monitors private sale listings for similar models to refine the valuation mesh.

## Inputs & Outputs
- **Inputs**:
  - `vehicle_vin_list` (List): Vehicle identification numbers.
  - `fuel_receipt_stream` (Data): Log of operating expenses.
- **Outputs**:
  - `fleet_liquidation_value` (float): Estimated USD if all vehicles were sold today.
  - `cpm_metrics` (float): Cost-per-mile efficiency score.

## Acceptance Criteria
- Maintain vehicle valuations within 5% of Kelly Blue Book or equivalent trade-in values.
- Categorize 100% of vehicle-related expenses from the Banker's transaction stream.
