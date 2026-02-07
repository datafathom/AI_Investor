# PHASE 4 IMPLEMENTATION PLAN: THE EXECUTION FLOOR (TRADING)
## FOCUS: TRADING AGENTS, BROKER APIS, AND ORDERS

---

## 1. PROJECT OVERVIEW: PHASE 4
Phase 4 transitions the system from theoretical logic into actual market action. This phase focuses on the **Trader Department (Dept 4)** and its 6 agents. This is where we connect the "Brain" to the "Fists" (Brokerage APIs).

---

## 2. GOALS & ACCEPTANCE CRITERIA
- **G1**: Full API integration with Brokerage (IBKR/Schwab) for automated order execution.
- **G2**: Implementation of the "Sniper" (Agent 4.1) with Iceberg execution logic.
- **G3**: Deployment of the "Position Sizer" (Agent 4.5) with strict Kelly Criterion bet-sizing.
- **G4**: Functional "Trader Workstation" with real-time L2 order book visualization.

---

## 3. FULL STACK SPECIFICATIONS

### 3.1 FRONTEND (The Trade Station)
- **Description**: Implementation of the high-fidelity Trading HUD and Order Entry system.
- **Acceptance Criteria**:
    - **C1: Order Book Visualization**: Real-time rendering of L2 Bid/Ask depth with < 50ms latency from the WebSocket stream.
    - **C2: Biometric Interlock**: The "Execute" button is globally disabled until a valid WebAuthn challenge is successfully completed by the user.
    - **C3: Visual Feedback**: Orders reflect "Staged," "Pending," and "Filled" states with distinct industrial colors and subtle micro-animations.

### 3.2 BACKEND (The Order Controller)
- **Description**: Managing the broker connection (IBKR `ib_insync`) and the trade execution logic.
- **Acceptance Criteria**:
    - **C1: Connection Resilience**: Automated reconnection to the Broker gateway with 0% data loss during 10-second internet outages.
    - **C2: Execution Latency**: Order signal to Broker API call (including Kelly check and Sentry validation) completes in < 15ms.
    - **C3: Non-Repudiation**: 100% of broker orders are logged with their cryptographically verified `signature_hash` in the Postgres ledger.

### 3.3 INFRASTRUCTURE (The Execution Pipeline)
- **Description**: Dedicated high-priority Kafka topics and Broker Gateway hosting.
- **Acceptance Criteria**:
    - **C1: Kafka Priority**: The `agent.commands` topic is configured with `0ms` linger to ensure immediate transmission.
    - **C2: Static IP Binding**: All broker API connections are white-listed to the static IP of the execution node.
    - **C3: Redundancy**: A secondary "Hot-Standby" Broker Gateway container is ready to take over in < 2 seconds if the primary fails.

### 3.4 TESTING & VERIFICATION
- **Description**: Safety-first trading validation.
- **Acceptance Criteria**:
    - **T1: Paper-Trade Loop**: 1,000 trades executed on the IBKR Paper account verify that Agent 4.5 NEVER exceeds the max dollar risk limit.
    - **T2: Circuit Breaker Test**: Simulate a -10% flash-crash; verify that Agent 4.6 cancels 100% of open orders within 50ms.
    - **T3: Auth Bypass**: Attempt a trade via the CLI without a signature; Backend MUST return a `403` and log a "Critical Security Breach" event.

---

## 4. AGENT CONTRACTS

##### 👤 AGENT 4.1: The Sniper
- **Acceptance Criteria**: Executes "Iceberg" orders with randomized intervals (3-7s), achieving an average fill price within 0.05% of the Mid-price.

##### 👤 AGENT 4.2: The Exit Manager
- **Acceptance Criteria**: Stop-loss orders are updated in < 1s after a ticker move that triggers the trailing threshold.

##### 👤 AGENT 4.5: The Position Sizer
- **Acceptance Criteria**: Bet-sizing logic follows Kelly Criterion exactly, never exceeding the "Max Trade Size" parameter in the user's risk profile.

---

## 5. MILESTONES & TIMELINE
- **Week 1**: Broker API (IBKR/Schwab) Handshake + Read-Only Stream.
- **Week 2**: Sniper Agent + Iceberg Fragmenter Logic.
- **Week 3**: Position Sizer (Kelly) + Risk Circuit Breaker deployment.
- **Week 4**: Trader Workstation UI Finalization + Paper-Trade E2E.

---
**END OF PHASE 4 IMPLEMENTATION PLAN**
