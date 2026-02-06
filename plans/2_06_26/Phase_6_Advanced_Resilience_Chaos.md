# Phase 6: Advanced Resilience & Chaos

## Overview
This phase hardens the OS against internal failure and external deception. We are building the "Immune System" of the Sovereign OS. This includes a dedicated Chaos Agent for stress testing, Shadow Modeling for logic verification, and Active Defense traps to catch intruders sniffing our data bus.

## Deliverables

### 1. The Chaos Agent (Stress Injector)
**Description**: A specialized agent that injects artificial failures into the dev environment to test system recovery.
- **Acceptance Criteria**:
  - Successfully simulates "Kafka Lag" by throttling consumer throughput.
  - Automatically kills "Non-Essential" containers to verify that Orchestrator (Dept 1) re-spawns them.
  - Injects "Noisy Data" (malformed JSON) into topics to test agent error-handling.

### 2. "Shadow Prompting" Verification Engine
**Description**: Using a secondary, local LLM to critique and score the primary model's critical outputs.
- **Acceptance Criteria**:
  - "Disagreement Score" > 0.4 triggers an automatic HITL pause.
  - Secondary model (e.g., Llama 3) runs on a separate isolated container from the primary.
  - Logic comparisons are logged in the Trace Log as `SHADOW_VERIFICATION`.

### 3. "Honey-Token" Active Defense Traps
**Description**: Placing tripwire credentials and ghost assets throughout the state to detect breaches.
- **Acceptance Criteria**:
  - If any process attempts to use the `HONEY_TEST_KEY`, a "Total Lockdown" is triggered by Dept 8.
  - Honey-tokens are automatically rotated to avoid detection by repeat attackers.
  - Detection event includes a "Spatial Map" (IP/ProcessID) of where the token was touched.

### 4. Smart Model Router (Hybrid Cloud/Local)
**Description**: A "Sovereign Brain" that routes tasks based on privacy, cost, and complexity.
- **Acceptance Criteria**:
  - Tasks containing "Private Keys" or "Neo4j Identifiers" are 100% routed to local LLMs (Ollama).
  - Low-complexity tasks (Summarization) use small 7B models to save resources.
  - Router latency overhead is < 15ms.

### 5. Automated Agent "Backtesting" (Simulation)
**Description**: A "Sandbox Mode" where agents process real data but tool calls are sent to a Mock API.
- **Acceptance Criteria**:
  - Simulation results are compared against a human "Ground Truth" to calculate a "Financial IQ" score.
  - Agents require a > 95% IQ score over a 48-hour run before "Promotion" to live status.
  - Mock API captures 100% of outbound headers for security auditing.

### 6. Cascading Failure Prevention (Circuit Breakers)
**Description**: Implementing patterns to stop a single agent's failure from freezing the Kafka bus.
- **Acceptance Criteria**:
  - 100% of inter-dept tool calls are wrapped in `Circuit Breaker` decorators.
  - "Amber Alert" state is triggered when a circuit trips, alerting the HUD.
  - "Auto-Recovery" logic attempts a reset only after a 60-second cool-down.

## Proposed Changes

### [Backend] [Resilience]
- [NEW] [chaos_agent.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/agents/chaos_agent.py): The injector.
- [NEW] [shadow_verifier.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/shadow_verifier.py): Dual-model check.
- [NEW] [circuit_breaker.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/utils/circuit_breaker.py): Stability decorators.

### [Backend] [Intelligence]
- [NEW] [sovereign_router.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/sovereign_router.py): Ollama/Cloud routing logic.

## Verification Plan

### Automated Tests
- `pytest tests/resilience/test_honeytoken_trigger.py`
- `pytest tests/resilience/test_shadow_scoring.py`

### Manual Verification
- Toggle "Chaos Stress Test" in HUD and verify department recovery.
- Submit a "Sensitive" query and verify `ollama` container picks it up (view logs).
