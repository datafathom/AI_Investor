# Documentation: `tests/integration/test_sovereign_kernel_e2e.py`

## Overview
This is a high-fidelity End-to-End (E2E) test suite for the "Phase 1: Sovereign Kernel". It validates the core Zero-Trust security primitives, the triple-entry ledger system (Postgres + Neo4j), and the orchestration agent workforce.

## Components Under Test
- `services.auth.sovereign_auth_service`: WebAuthn-based Zero-Trust Auth.
- `services.neo4j.graph_ledger_sync`: Real-time Postgres-to-Neo4j synchronization.
- `agents.orchestrator`: The primary agent workforce (Interpreter, Sentry, Weaver, etc.).

## Critical Performance & Acceptance Criteria

### 1. Challenge-Response Latency (C2)
- **Goal**: Auth cycle must complete in < 300ms.
- **Verification**: Measures the performance of generating and verifying signatures.

### 2. Double-Entry Integrity
- **Goal**: Prevent unbalanced ledger entries.
- **Verification**: Ensures that journal entries where `debit != credit` are rejected with a `ValueError`.

### 3. Real-Time Graph Sync (C4)
- **Goal**: Postgres commits must reflect in Neo4j in < 100ms.
- **Verification**: Measures the sync latency for new journal entries.

### 4. Zero Variance Audit (C3)
- **Goal**: The graph representation must match the relational database exactly.
- **Verification**: Performs a comprehensive account-by-account variance check.

### 5. Orchestrator Agent Health
- **Goal**: All 6 core orchestrator agents (Synthesizer, Interpreter, Guardian, Sentry, Weaver) must be operational.
- **Verification**: Starts the agents and validates their health status and specific process logic (e.g., Sentry blocking dangerous syscalls).

## Holistic Context
The Sovereign Kernel is the "brain stem" of the AI Investor. These tests provide extreme confidence that the foundational security, accounting, and decision-making systems are performing at institutional standards.
