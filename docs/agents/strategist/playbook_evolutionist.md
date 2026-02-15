# Playbook Evolutionist (Agent 4.6)

## ID: `playbook_evolutionist`

## Role & Objective
The "Meta-Learner". Improving strategy parameters based on actual outcomes. It ensures the Sovereign OS learns from its mistakes and successes.

## Logic & Algorithm
1. **Outcome Feedback**: Feeds successful and failed trade results back into the parameter optimizer.
2. **Mistake Classification**: Analyzes trade slippage and execution errors to tighten future strategy constraints.
3. **Incremental Improvement**: Proposes weekly parameter tweaks to the Logic Architect based on cross-sectional performance data.

## Inputs & Outputs
- **Inputs**:
  - `trade_history` (List): Full ledger of past outcomes.
  - `optimization_goals` (e.g., 'Minimize Drawdown').
- **Outputs**:
  - `proposed_tweaks` (Dict): Suggested changes to strategy constants.

## Acceptance Criteria
- Proposed tweaks must demonstrate a backtested improvement of at least 1% in the Sharpe ratio before being submitted for approval.
- The evolutionist must document the "Reasoning Path" for every proposed change.
