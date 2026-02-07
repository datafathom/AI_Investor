# Orchestrator Department Agents (`orchestrator/orchestrator_agents.py`)

The Orchestrator department is the "Sovereign Kernel," the central nervous system that manages communication, security, and the overall system state.

## Synthesizer Agent (Agent 1.1)
### Description
Aggregates activity logs from all 84 agents into a unified "State of the Union" daily briefing.
- **Accuracy**: Briefing totals must match ledger totals to 0.01%.

---

## Command Interpreter Agent (Agent 1.2)
### Description
Translates voice or text commands into structured JSON system calls.
- **Accuracy**: 99% accuracy on entity extraction (tickers, quantities, dates).

---

## Traffic Controller Agent (Agent 1.3)
### Description
The "Kafka Master" that manages message routing and backpressure.
- **Performance**: Maintains Kafka lag < 200ms even during 5k msg/sec spikes.

---

## Layout Morphologist Agent (Agent 1.4)
### Description
Predicatively manages the UI layout based on market events.
- **Trigger**: Automatically switches the HUD to "Trader Mode" within 500ms of high-volatility detection.

---

## Red-Team Sentry Agent (Agent 1.5)
### Description
The internal security officer monitoring for unsafe bytecode or syscalls.
- **Enforcement**: Issues an immediate `SIGKILL` on any agent attempting un-whitelisted `os.system` or `eval` calls.

---

## Context Weaver Agent (Agent 1.6)
### Description
Maintains Redis-based session memory to ensure 100% context injection during agent role-switches.
