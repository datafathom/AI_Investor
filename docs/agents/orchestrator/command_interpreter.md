# Command Interpreter (Agent 1.2)

## ID: `command_interpreter`

## Role & Objective
The linguistic gateway of the system. It translates natural language (voice or text) into structured, executable system calls that other agents can understand.

## Logic & Algorithm
1. **Verb Extraction**: Identifies primary actions (BUY, REBALANCE, AUDIT) using a high-precision whitelist.
2. **Entity Recognition**: Extracted Tickers, Amounts, and Dates using optimized Regex and NLP models.
3. **Context Sensitivity**: Resolves ambiguous terms (e.g., "Apple" to AAPL) based on portfolio context.
4. **Validation**: Scores output confidence to determine if a follow-up clarification is needed.

## Inputs & Outputs
- **Inputs**:
  - Raw User Text/Voice Transcripts
- **Outputs**:
  - Structured System Call (JSON)
  - Confidence Score

## Acceptance Criteria
- 99% accuracy on entity extraction for Tickers, Accounts, and Dates.
- Interpretation latency must be < 100ms for standard commands.
