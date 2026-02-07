# Documentation: `tests/unit/test_orchestrator_agents.py`

## Overview
This test suite provides granular validation for the "Orchestrator" workforce (Phase 1), which manages system-wide coordination, security, and UI state.

## Agents Under Test
- **1.1 Synthesizer**: Log aggregation and ledger validation.
- **1.2 Command Interpreter**: Natural language to structured command parsing.
- **1.3 Traffic Controller**: Backpressure and lag monitoring.
- **1.4 Layout Morphologist**: UI response to market volatility.
- **1.5 Red-Team Sentry**: Forbidden syscall blocking (e.g., `os.system`).
- **1.6 Context Weaver**: State transfer during role switching.

## Key Test Scenarios

### 1. Safety & Security (Sentry)
- **Goal**: Prevent malicious code execution from third-party agents.
- **Assertions**: Calls to `eval()` or `os.system()` trigger an immediate `SIGKILL` status.

### 2. Decision Logic (Traffic & Layout)
- **Goal**: Ensure the system responds to environmental changes.
- **Assertions**:
    - Lag > 200ms triggers `backpressure: True`.
    - Market volatility > 5% switches UI to `trader_hud`.

### 3. State Integrity (Synthesizer & Weaver)
- **Goal**: Maintain a clean state across agent transitions.
- **Assertions**:
    - Ledger variance > 0.01% triggers a `mismatch` validation.
    - Context buffer correctly limits to the last 5 relevant actions.

## Holistic Context
This suite is the primary verification for the "Operating System" layer of the project. It ensures that the system is not just performing financial tasks, but is structurally sound and self-defending.
