# Document Drafter (Agent 19.4)

## ID: `document_drafter`

## Role & Objective
The 'Technical Writer'. Creates professional PDFs, governance reports, whitepapers, and legal-adjacent documentation from system raw data.

## Logic & Algorithm
- **Template Application**: Maps data into standard institutional templates (e.g., "Monthly Audit," "New Strategy Proposal").
- **Citation Management**: Automatically generates bibliographies and links to on-chain transaction hashes or data sources.
- **WORM Storage Integration**: Ensures the final document is signed and stored in Immutable storage if marked as "Critical."

## Inputs & Outputs
- **Inputs**:
  - `report_data` (JSON).
  - `document_type` (Enum): Whitepaper, Audit, Proposal.
- **Outputs**:
  - `final_pdf` (URI): Path to the rendered PDF document.

## Acceptance Criteria
- Generate a 10-page report with 0 layout orphans or overflows.
- Ensure all PDF metadata (Author, Date, Version) is correctly populated.
