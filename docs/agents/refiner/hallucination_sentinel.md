# Hallucination Sentinel (Agent 17.1)

## ID: `hallucination_sentinel`

## Role & Objective
The 'LLM Refiner'. Iteratively tests and improves the system prompts across all departments to reduce hallucination and ensure that LLM outputs adhere strictly to institutional logic and verified facts.

## Logic & Algorithm
- **Fact-Check Loop**: Cross-references LLM assertions against the Historian's "Verified Truth" database.
- **Reference Validation**: Ensures that every claim made by an agent (e.g., "The S&P is up 2%") is backed by an actual data point from a trusted source.
- **Syntactic Audit**: Rejects responses that fail to adhere to the required JSON or Markdown structure.

## Inputs & Outputs
- **Inputs**:
  - `agent_raw_responses` (Stream): The output from any agent in the workforce.
- **Outputs**:
  - `audit_pass_fail` (Bool).
  - `hallucination_report` (Dict): Specific areas of logic failure.

## Acceptance Criteria
- Achieve a hallucination rate of < 0.1% for high-stakes financial decisions.
- Successfully block 100% of responses containing "Confidently Wrong" numerical data.
