# Logic Architect (Agent 4.1)

## ID: `logic_architect`

## Role & Objective
The "Strategy Designer" of the Sovereign OS. The Logic Architect converts qualitative investment theses into structured, executable code blocks for the backtesting engine.

## Logic & Algorithm
1. **Thesis Parsing**: Analyzes natural language strategy descriptions (e.g., 'Buy when RSI < 30 and volume spikes').
2. **Blueprint Generation**: Outputs JSON objects defining entry/exit rules and risk parameters.
3. **Circular Dependency Check**: Validates that strategies do not rely on future data or circular logic.

## Inputs & Outputs
- **Inputs**:
  - `strategy_thesis` (str): Qualitative description of a trading signal.
- **Outputs**:
  - `code_blueprint` (Dict): Structured entry/exit rules and risk parameters.

## Acceptance Criteria
- Successfully parse and convert 95% of standard technical analysis patterns into executable JSON.
- Blueprint generation must complete in under 500ms.
