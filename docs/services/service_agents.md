# Backend Service: Agents

## Overview
The **Agents Service** is the brain of the AI Investor platform. it orchestrates a swarm of specialized AI agents, each with unique financial personas. The service handles multi-agent consensus, competitive debates between "Bull" and "Bear" perspectives, agent health monitoring, and critical security protocols to prevent rogue behavior.

## Core Components

### CIO Agent (`cio_agent.py`)
Represents the Chief Investment Officer persona for a Family Office.
- **Role**: Provides high-level portfolio oversight and high-fidelity investment recommendations.
- **Logic**: Analyzes portfolio weights and suggests rebalancing (e.g., reducing equity if >70%).

### Consensus Engine (`consensus_engine.py`)
A democratic decision-making layer for the agent swarm.
- **Purpose**: Ensures major decisions (e.g., large trades) are backed by a quorum of agents.
- **Mechanism**: Agents cast votes, and the engine calculates the approval rate against a configurable threshold (Default: 70%).

---

### Debate Ecosystem
Multi-agent competitive analysis to simulate deep market research.

#### Debate Chamber (`debate_chamber.py`)
Provides the analytical logic for weighing arguments.
- **Personas**: Includes `AGGRESSIVE_GROWTH`, `CONSERVATIVE_YIELD`, `MACRO_BEAR`, and `QUANT_ARBITRAGE`.
- **Logic**: Aggregates confidence scores for bullish vs. bearish arguments to reach a consensus verdict.

#### Debate Orchestrator (`debate_orchestrator.py`)
A singleton service that manages live debate sessions.
- **Features**: 
    - Handles turn-taking between participants like "The Bull", "The Bear", and "The Risk Manager". 
    - Maintains a transcript of the debate.
    - Allows human intervention (user arguments) to influence the AI debate.
    - Continuously recalculates sentiment scores based on recent turns.

---

### Operations & Security

#### Heartbeat Service (`heartbeat_service.py`)
A real-time monitoring system for the agent workforce.
- **Tracking**: Monitors heartbeats via Kafka to ensure agents are `ALIVE`.
- **Auto-Detection**: Automatically marks agents as `DEAD` if no heartbeat is received within 5 seconds.

#### Persona Rotator (`persona_rotator.py`)
Optimizes the agent workforce based on market conditions.
- **Logic**: Dynamically switches active personas based on the market regime (e.g., uses `SEARCHER` for Trending markets, `PROTECTOR` for High Volatility).

#### Rogue Killer (`rogue_killer.py`)
A critical security circuit breaker.
- **Function**: Monitors the "Trades Per Minute" (TPM) of every agent.
- **Trigger**: If an agent exceeds 100 TPM, it is flagged as a "Rogue Agent" and a `KILL` action is triggered to terminate the process immediately.

## Dependencies
- `services.system.model_manager`: Used for LLM-based agent responses.
- `asyncio`: Used for non-blocking heartbeat tracking.
- `datetime`: Used for session timing and heartbeat thresholds.

## Usage Example

### Orchestrating a Debate
```python
from services.agents.debate_orchestrator import DebateOrchestrator

orch = DebateOrchestrator()
session = orch.start_debate(ticker="NVDA")
print(f"Session {session['id']} started for {session['ticker']}")
```

### Checking Agent Health
```python
from services.agents.heartbeat_service import heartbeat_service

agents = await heartbeat_service.get_all_agents()
for agent in agents:
    status = "✅" if agent['is_alive'] else "❌"
    print(f"{status} Agent {agent['agent_id']} ({agent['status']})")
```
