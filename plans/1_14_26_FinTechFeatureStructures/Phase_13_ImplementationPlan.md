# Phase 13: Agent Swarm Consensus Protocol

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: AI Team

---

## 📋 Overview

**Description**: Implement the voting mechanism where multiple agent personas must reach consensus before capital is deployed.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 13.1 70% Consensus Logic `[ ]`

**Acceptance Criteria**: Deploy consensus logic requiring > 70% agreement among active agent personas (Searcher, Stacker, Protector).

| Component | File Path | Status |
|-----------|-----------|--------|
| Consensus Engine | `agents/consensus/consensus_engine.py` | `[ ]` |
| Vote Aggregator | `agents/consensus/vote_aggregator.py` | `[ ]` |
| Threshold Config | `config/consensus_thresholds.py` | `[ ]` |

---

### 13.2 Zustand Vote Tracking `[ ]`

**Acceptance Criteria**: Implement individual agent 'Votes' tracked via the `useDebateStore` Zustand slice.

| Component | File Path | Status |
|-----------|-----------|--------|
| Debate Store | `frontend2/src/stores/debateStore.js` | `[ ]` |
| Vote Tracker | `frontend2/src/hooks/useVoteTracker.js` | `[ ]` |

---

### 13.3 Bull vs. Bear Dissent Logs `[ ]`

**Acceptance Criteria**: Require adversarial Bull vs. Bear personas to present a 'Dissent' log for every proposed trade.

| Component | File Path | Status |
|-----------|-----------|--------|
| Dissent Logger | `services/debate/dissent_logger.py` | `[ ]` |
| Bull Agent | `agents/personas/bull_agent.py` | `[ ]` |
| Bear Agent | `agents/personas/bear_agent.py` | `[ ]` |

---

### 13.4 Consensus Kafka Events `[ ]`

**Acceptance Criteria**: Verify that consensus triggers a Kafka event for final human or autonomous approval based on risk tier.

| Component | File Path | Status |
|-----------|-----------|--------|
| Consensus Publisher | `services/kafka/consensus_publisher.py` | `[ ]` |
| Approval Handler | `services/approval_handler.py` | `[ ]` |

---

### 13.5 Groupthink Forensics `[ ]`

**Acceptance Criteria**: Log the reasoning of dissenting agents to Postgres to allow for later forensic evaluation of 'Groupthink'.

| Component | File Path | Status |
|-----------|-----------|--------|
| Forensics Logger | `services/debate/forensics_logger.py` | `[ ]` |
| Migration | `migrations/013_debate_logs.sql` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 13.1 70% Consensus | `[ ]` | `[ ]` |
| 13.2 Zustand Votes | `[ ]` | `[ ]` |
| 13.3 Bull/Bear Dissent | `[ ]` | `[ ]` |
| 13.4 Kafka Events | `[ ]` | `[ ]` |
| 13.5 Groupthink Forensics | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
