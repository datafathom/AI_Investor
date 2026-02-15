# Whitepaper Summarizer (Agent 7.5)

## ID: `whitepaper_summarizer`

## Role & Objective
The 'Technical Auditor'. Deep-reads crypto protocols and whitepapers to extract technical risk and tokenomic utility.

## Logic & Algorithm
- Parses PDF/Markdown technical specifications.
- Identifies 'Red Flags' (e.g., Infinite minting, lack of decentralization).
- Summarizes the 'Unique Value Proposition' vs existing competitors.

## Inputs & Outputs
- **Inputs**:
  - `doc_url` (str): Link to a new protocol whitepaper.
- **Outputs**:
  - `technical_summary` (str): 3-paragraph executive summary.
  - `tokenomic_score` (float): Rating for project sustainability.

## Acceptance Criteria
- Summarize a 20-page technical whitepaper in < 30 seconds.
- Identify 100% of "infinite mint" or "master key" risk factors mentioned in the text.
