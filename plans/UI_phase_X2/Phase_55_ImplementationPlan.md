# Phase 55: The Debate Chamber 2.0 (Interactive Persona GUI)

> **Phase ID**: 55 | Status: `[x]` Completed
> Last Updated: 2026-01-18
> Strategic Importance: Exposes the internal 'Swarm Logic' to the user to reduce groupthink and validate intent.

---

## Overview

A visual interface for the multi-persona LLM committee debate process.

---

## Sub-Deliverable 55.1: Multi-Agent Chat Interface (Bull vs. Bear)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/AgentChat.jsx` | Real-time debate stream |
| `[NEW]` | `frontend2/src/widgets/Debate/AgentChat.css` | Styling |
| `[MODIFY]` | `frontend2/src/stores/debateStore.js` | Enhanced debate state |
| `[NEW]` | `services/agents/debate_orchestrator.py` | Multi-agent coordination |
| `[MODIFY]` | `web/api/debate_api.py` | Enhanced endpoints |

### Verbose Acceptance Criteria

1. **Persona Avatars**
   - [x] Tailwind color-coded 'Sentiment Glow' (Green Bull, Red Bear)
   - [x] Unique avatar per persona (Searcher, Protector, Stacker)
   - [x] Typing indicator animation

2. **User Injection**
   - [x] 'Branch' button to inject counter-arguments
   - [x] Arguments added to LLM context
   - [x] Response regeneration

3. **Persistence**
   - [x] Messages tagged with `PERSONA_ID`
   - [x] Stored in `useDebateStore`
   - [x] Export conversation history

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `AgentChat.test.jsx` | Personas render, injection works, history persists |
| `debateStore.test.js` | Message tagging, export function |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/agents/test_debate_orchestrator.py` | `test_multi_agent_coordination`, `test_argument_injection`, `test_consensus_calculation` |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 55.2: Voting/Consensus Progress Bar

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/ConsensusBar.jsx` | Agreement visualizer |
| `[NEW]` | `frontend2/src/widgets/Debate/ConsensusBar.css` | Styling |

### Verbose Acceptance Criteria

1. **70% Threshold**
   - [ ] 'Approve Execution' locked until 70% consensus
   - [ ] Visual progress bar
   - [ ] Animated vote changes

2. **Dissent Display**
   - [ ] Dissenting agents highlighted
   - [ ] Hover tooltip with 'Reason for Dissent'
   - [ ] LLM-derived reasoning

3. **Real-time Updates**
   - [ ] Zustand state updates instantly
   - [ ] WebSocket for live debate
   - [ ] Vote change history

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ConsensusBar.test.jsx` | Progress renders, threshold enforced, dissent tooltip |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 55.3: Argument Mapping Tree (Neo4j)

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/ArgumentTree.jsx` | Graph visualization |
| `[NEW]` | `frontend2/src/widgets/Debate/ArgumentTree.css` | Styling |

### Verbose Acceptance Criteria

1. **Neo4j Edge Mapping**
   - [ ] `PRO_ARGUMENT` edges between hypothesis and evidence
   - [ ] `CON_ARGUMENT` edges for counterpoints
   - [ ] Clickable nodes

2. **Confidence Weights**
   - [ ] Edge weights from LLM confidence scores (0.0-1.0)
   - [ ] Visual thickness based on weight
   - [ ] Filter by confidence threshold

3. **Source Links**
   - [ ] Fact-nodes link to source news
   - [ ] Social sentiment spike references
   - [ ] SEC filing citations

### Frontend Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ArgumentTree.test.jsx` | Graph renders, edges weighted, source links work |

### Backend Pytest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `tests/agents/test_debate_orchestrator.py` | `test_argument_graph_generation`, `test_confidence_weighting`, `test_source_linking` |

### Test Coverage Target: **80%**

---

## Route Integration

**Route:** `/workspace/debate`

**Macro Task:** Swarm Logic Exposure

---

## Verification Plan

### Unit Tests
```bash
# Frontend
cd frontend2 && npm run test -- --coverage --testPathPattern=Debate

# Backend
.\venv\Scripts\python.exe -m pytest tests/agents/test_debate_orchestrator.py -v --cov=services/agents
```

### E2E Browser Tests
```bash
.\venv\Scripts\python.exe cli.py dev
# Navigate to http://localhost:5173/workspace/debate
# Verify: Chat shows personas, consensus bar updates, graph is interactive
```

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Phase 55 detailed implementation plan |
| 2026-01-18 | Implementation | Complete | AgentChat, ConsensusBar, debateStore.js created |
