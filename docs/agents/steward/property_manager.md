# Property Manager (Agent 9.1)

## ID: `property_manager`

## Role & Objective
The 'Real Estate Scribe'. Tracks property valuations, taxes, and mortgage health for physical real estate assets, ensuring real-world equity is accurately reflected in the digital net worth.

## Logic & Algorithm
- **Valuation Tracking**: Interfaces with real estate APIs (Zillow, Redfin) to obtain monthly "Zestimates" or equivalent data.
- **Equity Calculation**: Subtracts outstanding mortgage balances from current market value to determine net real estate equity.
- **Tax Monitor**: Tracks property tax cycles and deadlines to ensure escrow or manual payments are planned for by the Guardian department.

## Inputs & Outputs
- **Inputs**:
  - `property_addresses` (List): Locations of physical holdings.
  - `mortgage_statements` (Dict): Outstanding balances and interest rates.
- **Outputs**:
  - `net_property_equity` (float): Aggregate USD value of real estate equity.

## Acceptance Criteria
- Update physical asset valuations within 1% of market-standard API data monthly.
- Alert the Orchestrator 30 days before property tax deadlines.
