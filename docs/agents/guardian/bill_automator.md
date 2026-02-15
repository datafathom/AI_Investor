# Bill Automator (Agent 10.1)

## ID: `bill_automator`

## Role & Objective
The 'Liability Processor'. Manages the identification, categorization, and staging of all recurring institutional liabilities (utilities, mortgages, subscriptions).

## Logic & Algorithm
- **Bill Parsing**: Uses OCR and NLP to extract payment amounts and due dates from PDF statements.
- **Verification**: Cross-references invoices against historical averages to detect overcharging.
- **Staging**: Queues payments for authorization by the user or the Flow Master.

## Inputs & Outputs
- **Inputs**:
  - `digital_invoices` (List): PDF or raw email data from utilities/banks.
- **Outputs**:
  - `payment_schedule` (Dict): Breakdown of what is due and when.

## Acceptance Criteria
- Extract payment data from 95% of standard utility invoices with 100% currency accuracy.
- Stage bills at least 7 days prior to their due date.
