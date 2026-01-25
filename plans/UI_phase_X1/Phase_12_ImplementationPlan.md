# Phase 12: The Debate Chamber 2.0 (Interactive Persona GUI)

> **Phase 55** | Status: `[x]` Completed  
> Last Updated: 2026-01-18 | Verified: Yes (Screenshot stored)  
> Strategic Importance: Exposes the internal 'Swarm Logic' to the user to reduce groupthink and validate intent.

---

## Overview

A visual interface for the multi-persona LLM committee debate process, allowing humans to observe and intervene in AI decision-making.

---

## Sub-Deliverable 55.1: Multi-Agent Chat Interface (Bull vs. Bear)

### Description
Real-time debate stream between adversarial agent personas with user intervention capabilities.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[MODIFY]` | `frontend2/src/pages/DebateRoom.jsx` | Enhance existing page |
| `[MODIFY]` | `frontend2/src/pages/DebateRoom.css` | Updated styling |
| `[NEW]` | `frontend2/src/components/Debate/PersonaAvatar.jsx` | Agent avatar |
| `[NEW]` | `frontend2/src/components/Debate/MessageBubble.jsx` | Debate message |
| `[NEW]` | `frontend2/src/components/Debate/UserInterjection.jsx` | User input |
| `[NEW]` | `frontend2/src/stores/debateStore.js` | Zustand debate store |

### Verbose Acceptance Criteria

1. **Persona-Specific Avatars**
   - [ ] Distinct avatars for each persona: Bull, Bear, Neutral, Risk Officer
   - [ ] Tailwind color-coded "Sentiment Glow" around avatar
   - [ ] Bull = Green glow, Bear = Red glow, Neutral = Blue glow
   - [ ] Animated glow intensity based on conviction strength

2. **Branch Debate Capability**
   - [ ] User can inject counter-arguments mid-debate
   - [ ] "What if..." prompt for hypothetical scenarios
   - [ ] Agents respond to user input in real-time
   - [ ] Branch history tracked for replay

3. **Message Tagging**
   - [ ] All messages tagged with `PERSONA_ID`
   - [ ] Persisted in `useDebateStore` Zustand slice
   - [ ] Timestamp and conviction score metadata
   - [ ] Export debate transcript as markdown

4. **Real-time Streaming**
   - [ ] WebSocket connection for live debate updates
   - [ ] Typing indicator when agent is "thinking"
   - [ ] Auto-scroll to newest message
   - [ ] Pause/resume stream controls

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ws/debate` | WS | Real-time debate stream |
| `/api/v1/debate/interject` | POST | User interjection |
| `/api/v1/debate/history` | GET | Debate transcript |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `DebateRoom.test.jsx` | Messages render, user can interject, scroll behavior |
| `PersonaAvatar.test.jsx` | Avatar displays, glow color correct |
| `MessageBubble.test.jsx` | Message content, persona tag, timestamp |
| `debateStore.test.js` | Message add, branch tracking, export |

### Test Coverage Target: **80%**

---

## Sub-Deliverable 55.2: Voting/Consensus Progress Bar

### Description
Visual representation of agreement levels for proposed trades among AI agents.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/components/Debate/ConsensusBar.jsx` | Progress bar |
| `[NEW]` | `frontend2/src/components/Debate/ConsensusBar.css` | Bar styling |
| `[NEW]` | `frontend2/src/components/Debate/DissenterBadge.jsx` | Dissent indicator |

### Verbose Acceptance Criteria

1. **70% Threshold Enforcement**
   - [ ] "Approve Execution" button disabled until consensus ≥70%
   - [ ] Visual progress bar showing current consensus %
   - [ ] Animated fill as votes come in
   - [ ] Color gradient: Red (<50%) → Yellow (50-69%) → Green (≥70%)

2. **Dissenting Agent Highlights**
   - [ ] Dissenting agents highlighted with red badge
   - [ ] Hover-tooltip shows "Reason for Dissent"
   - [ ] Dissent reasons displayed as bullet points
   - [ ] Option to view full dissent argument

3. **Real-time Vote Updates**
   - [ ] Zustand state updates instantly as agents change votes
   - [ ] Vote change animations (flip from yes to no)
   - [ ] Historical vote tracking per proposal
   - [ ] "Force Approve" option for admin (with warning)

4. **Vote Breakdown Display**
   - [ ] Count: X For / Y Against / Z Abstain
   - [ ] Pie chart of vote distribution
   - [ ] List of voters with their positions

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ConsensusBar.test.jsx` | Progress accurate, threshold enforcement, button state |
| `DissenterBadge.test.jsx` | Badge appears, tooltip content, reason display |

### Test Coverage Target: **85%**

---

## Sub-Deliverable 55.3: Argument Mapping Tree (Neo4j)

### Description
Graph-based visualization of the AI's logical deductions for complete transparency.

### Files to Create/Modify

| Action | File Path | Purpose |
|--------|-----------|---------|
| `[NEW]` | `frontend2/src/widgets/Debate/ArgumentTree.jsx` | Tree visualization |
| `[NEW]` | `frontend2/src/widgets/Debate/ArgumentTree.css` | Tree styling |
| `[NEW]` | `frontend2/src/widgets/Debate/FactNode.jsx` | Clickable fact node |

### Verbose Acceptance Criteria

1. **Neo4j Edge Relationships**
   - [ ] Map `PRO_ARGUMENT` edges (supporting evidence)
   - [ ] Map `CON_ARGUMENT` edges (counter-evidence)
   - [ ] Central node = Trade Proposal
   - [ ] Branching nodes = Arguments

2. **Edge Weights from LLM Confidence**
   - [ ] Edge thickness = confidence score (0.0-1.0)
   - [ ] Thicker edges = stronger arguments
   - [ ] Hover shows exact confidence percentage
   - [ ] Filter by minimum confidence threshold

3. **Clickable Fact Nodes**
   - [ ] Click opens source document/news article
   - [ ] Support SEC filings, news URLs, internal analysis
   - [ ] Preview in modal before full navigation
   - [ ] "Verify Source" button for fact-checking

4. **Tree Layout**
   - [ ] D3.js force-directed graph or tree layout
   - [ ] Zoom/pan support
   - [ ] Collapse/expand branches
   - [ ] Export as PNG image

### Backend Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/graph/argument-tree` | GET | Neo4j argument structure |
| `/api/v1/sources/:id` | GET | Source document details |

### Jest Tests Required

| Test File | Test Cases |
|-----------|------------|
| `ArgumentTree.test.jsx` | Tree renders, edges display, nodes clickable |
| `FactNode.test.jsx` | Click handler, modal preview, source link |

### Test Coverage Target: **80%**

---

## Widget Registry Entries

```javascript
{
  id: 'debate-chamber',
  name: 'AI Debate Chamber',
  component: lazy(() => import('../../pages/DebateRoom')),
  category: 'AI',
  defaultSize: { width: 700, height: 600 }
},
{
  id: 'consensus-bar',
  name: 'Voting Consensus',
  component: lazy(() => import('../../components/Debate/ConsensusBar')),
  category: 'AI',
  defaultSize: { width: 400, height: 150 }
},
{
  id: 'argument-tree',
  name: 'Argument Mapping',
  component: lazy(() => import('../../widgets/Debate/ArgumentTree')),
  category: 'AI',
  defaultSize: { width: 600, height: 500 }
}
```

---

## Route Integration

**Route:** `/analyst/debate`

**Macro Task:** The Analyst

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Individual phase plan |

