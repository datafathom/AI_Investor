# Phase 55: The Debate Chamber 2.0 (Interactive Persona GUI)

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: AI & UX Team

---

## 📋 Overview

**Description**: Expose internal "Swarm Logic" through a visual interface. The user sees the Bull (FOMO) fighting the Bear (Risk) fighting the Analyst (Logic). This builds trust in the AI's decision making process.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 55

---

## 🎯 Sub-Deliverables

### 55.1 Multi-Agent Chat Interface `[x]`

**Acceptance Criteria**: Implement a chat interface where different "Personas" appear as distinct users with avatars. "Bullbot says..." "Bearbot says..."

| Component | File Path | Status |
|-----------|-----------|--------|
| Chat Component | `frontend2/src/components/Debate/ChatRoom.jsx` | `[x]` |

---

### 55.2 Argument Branching Interactions `[x]`

**Acceptance Criteria**: Enable 'Argument Branching' allowing the user to inject counter-arguments directly into the LLM context. "But what about CPI?" -> Agents react.

| Component | File Path | Status |
|-----------|-----------|--------|
| Context Manager | `services/ai/debate_context.py` | `[x]` |

---

### 55.3 Consensus Approval Lock `[x]`

**Acceptance Criteria**: Lock the 'Approve Execution' button until the swarm reaches a 70% consensus threshold. Visual progress bar of agreement.

| Component | File Path | Status |
|-----------|-----------|--------|
| Consensus Lock | `frontend2/src/components/Debate/ConsensusBar.jsx` | `[x]` |

---

### 55.4 Neo4j Argument Tree `[x]`

**Acceptance Criteria**: Visualize logical deductions via an Argument Mapping Tree in Neo4j with `SUPPORTS` / `CONTRADICTS` relationship edges.

```cypher
(:ARGUMENT {text: "Inflation is persistent"})-[:SUPPORTS]->(:THESIS {text: "Buy Gold"})
(:ARGUMENT {text: "Rates are high"})-[:CONTRADICTS]->(:THESIS {text: "Buy Gold"})
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Tree Builder | `services/neo4j/argument_tree.py` | `[x]` |

---

### 55.5 Confidence Edge Weights `[x]`

**Acceptance Criteria**: Derive edge weights from LLM confidence scores (0.0-1.0) and visualize via stroke thickness in the Neo4j graph/UI.

| Component | File Path | Status |
|-----------|-----------|--------|
| Weight Logic | `services/ai/confidence_calc.py` | `[x]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py debate start <topic>` | Launch swarm | `[x]` |
| `python cli.py debate status` | Current consensus | `[x]` |

---

*Last verified: 2026-01-25*
