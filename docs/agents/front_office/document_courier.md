# Document Courier (Agent 14.5)

## ID: `document_courier`

## Role & Objective
The 'Paperwork Manager'. Collects, organizes, and files physical and digital documents (scans, receipts, notices) for consumption by the Lawyer and Auditor departments.

## Logic & Algorithm
- **Categorization Engine**: Sorts raw uploads into folders: "Tax," "Legal," "Health," or "Commerce."
- **Metadata Extraction**: Identifies EINs, Reference Numbers, and Account IDs to link documents to specific financial entities.
- **Duplicate Removal**: Flags and deletes redundant copies of the same statement.

## Inputs & Outputs
- **Inputs**:
  - `raw_upload_pool` (Files): The "Inbox" for all new paperwork.
- **Outputs**:
  - `structured_document_index` (JSON): The mapping of files to their respective system nodes.

## Acceptance Criteria
- Categorize 100% of uploaded documents with a classification accuracy of > 98%.
- Sync 100% of "Tax-Relevant" documents to the Lawyer's vault within 5 minutes of upload.
