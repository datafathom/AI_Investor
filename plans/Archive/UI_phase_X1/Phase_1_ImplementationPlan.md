# Phase 1: Foundation & Window Management

> **Phases 43, 43.1, 44** | Status: `[ ]` Not Started  
> Last Updated: 2026-01-18

---

## Overview

Transforms the dashboard from a static grid into a functional **Desktop OS environment**. Critical for managing an active agent swarm during extreme volatility events.

---

## 43: Institutional OS-Style Window Management

### 43.1 Window Wrapper Pattern

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/WindowManager/WindowWrapper.jsx`
- `[NEW]` `frontend2/src/components/WindowManager/WindowWrapper.css`
- `[NEW]` `frontend2/src/stores/windowStore.js`

**Acceptance Criteria:**
- [ ] React 19 hooks implementation with `useCallback` and `useMemo` optimization
- [ ] Zustand store slice `useWindowStore` managing multi-window state
- [ ] Window state: `{ id, title, x, y, width, height, zIndex, isMinimized, isMaximized }`
- [ ] Support for 50+ concurrent windows without performance degradation

**Jest Tests Required:**
- [ ] `WindowWrapper.test.jsx`: Render test, props validation, state changes
- [ ] `windowStore.test.js`: Store actions (add, remove, focus, minimize, maximize)

---

### 43.2 Eight-Direction Resize Handles

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/WindowManager/ResizeHandles.jsx`
- `[MODIFY]` `frontend2/src/components/WindowManager/WindowWrapper.jsx`

**Acceptance Criteria:**
- [ ] 8 distinct handles: N, S, E, W, NE, NW, SE, SW
- [ ] Minimum window size enforced: 200x150 pixels
- [ ] Handle hit area: 8px edge detection
- [ ] Cursor changes on hover: `ns-resize`, `ew-resize`, `nesw-resize`, `nwse-resize`

**Jest Tests Required:**
- [ ] `ResizeHandles.test.jsx`: All 8 handles render, resize callbacks fire correctly

---

### 43.3 Z-Index Stacking Engine

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/stores/windowStore.js`

**Acceptance Criteria:**
- [ ] Click on any window brings it to foreground
- [ ] Z-index range: 100-1000 for windows, 1001+ reserved for modals
- [ ] `bringToFront(windowId)` action updates all z-indices atomically
- [ ] No z-index collisions during rapid clicking

**Jest Tests Required:**
- [ ] `windowStore.test.js`: Z-index ordering logic, collision prevention

---

### 43.4 Postgres-Backed Layout Persistence

**Files to Create/Modify:**
- `[MODIFY]` `backend/services/user_preferences_service.py`
- `[NEW]` `frontend2/src/hooks/useWorkspacePersistence.js`

**Acceptance Criteria:**
- [ ] Save workspace layout on: window close, 30s debounce, manual save
- [ ] Restore workspace in <200ms on login
- [ ] API endpoint: `POST /api/v1/user/workspace`
- [ ] Schema: `{ userId, workspaceName, windows: [...], savedAt }`

**Jest Tests Required:**
- [ ] `useWorkspacePersistence.test.js`: Save/restore logic, debounce behavior

---

### 43.5 Framer Motion Dragging Physics

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/components/WindowManager/WindowWrapper.jsx`

**Acceptance Criteria:**
- [ ] `motion.div` with `drag` prop and `dragMomentum={false}`
- [ ] Constrain dragging to viewport bounds
- [ ] Zero-latency visual feedback during high-frequency data updates
- [ ] `onDragEnd` persists new position to Zustand

**Jest Tests Required:**
- [ ] `WindowWrapper.test.jsx`: Drag events update position state

---

## 43.1: Glassmorphism UI Chrome

### 43.1.1 Backdrop Filter Implementation

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/styles/glassmorphism.css`

**Acceptance Criteria:**
- [ ] `backdrop-filter: blur(20px)` on all widget containers
- [ ] Background fill: `rgba(13, 17, 23, 0.7)`
- [ ] Fallback for browsers without backdrop-filter support

---

### 43.1.2 Professional Shadows

**Acceptance Criteria:**
- [ ] Box shadow: `0 10px 15px -3px rgba(0, 0, 0, 0.5)`
- [ ] Distinct overlapping layer visibility

---

### 43.1.3 Active Window Neon Border

**Acceptance Criteria:**
- [ ] 1px neon border color based on agent risk state
- [ ] Green (`#00ff88`): Low risk
- [ ] Yellow (`#ffc107`): Medium risk  
- [ ] Red (`#ff4757`): High risk
- [ ] CSS variable: `--window-risk-color`

---

### 43.1.4 Window Chrome Buttons

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/WindowManager/WindowControls.jsx`

**Acceptance Criteria:**
- [ ] Close (Red), Minimize (Yellow), Maximize (Green) buttons
- [ ] 150ms hover transition with scale effect
- [ ] Accessible: keyboard navigation, aria-labels

**Jest Tests Required:**
- [ ] `WindowControls.test.jsx`: Click handlers, accessibility attributes

---

## 44: Taskbar Logic & Agent Heartbeat

### 44.1 Dynamic Bottom Dock

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/Taskbar/Taskbar.jsx`
- `[NEW]` `frontend2/src/components/Taskbar/Taskbar.css`
- `[NEW]` `frontend2/src/components/Taskbar/TaskbarIcon.jsx`

**Acceptance Criteria:**
- [ ] Fixed bottom dock (height: 48px)
- [ ] Icon-based representation of all active agents/widgets
- [ ] Click to restore minimized window
- [ ] Auto-hide option with hover reveal

**Jest Tests Required:**
- [ ] `Taskbar.test.jsx`: Renders all minimized windows, click restores
- [ ] `TaskbarIcon.test.jsx`: Status indicator colors

---

### 44.2 Kafka-Driven Heartbeat Indicators

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/hooks/useAgentHeartbeat.js`
- `[MODIFY]` `frontend2/src/components/Taskbar/TaskbarIcon.jsx`

**Acceptance Criteria:**
- [ ] Subscribe to Kafka topic: `agent-heartbeat`
- [ ] Green pulse: Agent responsive (<5s since last heartbeat)
- [ ] Red pulse: Agent unresponsive (>5s since last heartbeat)
- [ ] Pulse animation: CSS `@keyframes pulse`

**Jest Tests Required:**
- [ ] `useAgentHeartbeat.test.js`: Mock WebSocket, status transitions

---

### 44.3 Window Restoration Logic

**Acceptance Criteria:**
- [ ] Restore to exact (X, Y, W, H) coordinates in <100ms
- [ ] If previous position off-screen, center window
- [ ] Smooth Framer Motion `animate` transition

---

### 44.4 Hover Tooltip Sparklines

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/Taskbar/SparklineTooltip.jsx`

**Acceptance Criteria:**
- [ ] D3.js mini-sparkline (last 20 data points)
- [ ] Display primary metric: P&L, Hype Score, or Health %
- [ ] Tooltip appears in 200ms, disappears on mouse leave

**Jest Tests Required:**
- [ ] `SparklineTooltip.test.jsx`: Renders SVG, handles empty data

---

## Backend Implementation

### Python Services Required

#### `services/workspace/user_preferences_service.py` [NEW]

```python
"""User workspace and preferences management."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class WorkspaceLayout(BaseModel):
    workspace_id: str
    workspace_name: str
    windows: List[WindowState]
    saved_at: datetime

class WindowState(BaseModel):
    id: str
    title: str
    x: int
    y: int
    width: int
    height: int
    z_index: int
    is_minimized: bool
    is_maximized: bool

class UserPreferencesService:
    """Manages user workspace layouts in Postgres."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def save_workspace(self, user_id: str, workspace: WorkspaceLayout) -> bool:
        """Save workspace layout with <200ms target."""
        pass
    
    async def get_workspace(self, user_id: str, workspace_id: str = None) -> Optional[WorkspaceLayout]:
        """Retrieve workspace, default if workspace_id is None."""
        pass
    
    async def list_workspaces(self, user_id: str) -> List[dict]:
        """List all saved workspaces for user."""
        pass
    
    async def delete_workspace(self, user_id: str, workspace_id: str) -> bool:
        """Delete a saved workspace."""
        pass
```

#### `services/agents/heartbeat_service.py` [NEW]

```python
"""Agent heartbeat monitoring via Kafka."""
from typing import List, Dict
from datetime import datetime, timedelta
from enum import Enum

class AgentStatus(Enum):
    ALIVE = "alive"
    DEAD = "dead"
    STARTING = "starting"
    STOPPING = "stopping"

class HeartbeatService:
    """Tracks agent heartbeats via Kafka topic 'agent-heartbeat'."""
    
    HEARTBEAT_TIMEOUT_SECONDS = 5
    
    def __init__(self, kafka_consumer):
        self.kafka = kafka_consumer
        self.heartbeats: Dict[str, datetime] = {}
    
    async def record_heartbeat(self, agent_id: str, status: AgentStatus) -> None:
        """Record heartbeat from agent."""
        pass
    
    def is_agent_alive(self, agent_id: str) -> bool:
        """Check if agent heartbeat is within threshold."""
        last = self.heartbeats.get(agent_id)
        if not last:
            return False
        return datetime.utcnow() - last < timedelta(seconds=self.HEARTBEAT_TIMEOUT_SECONDS)
    
    async def get_all_agents(self) -> List[dict]:
        """Get status of all registered agents."""
        pass
```

---

### Web Routes Required

#### `web/routes/workspace_routes.py` [NEW]

| Endpoint | Method | Handler | Auth | Response Time |
|----------|--------|---------|------|---------------|
| `/api/v1/user/workspace` | GET | `get_user_workspace` | JWT | <200ms |
| `/api/v1/user/workspace` | POST | `save_user_workspace` | JWT | <200ms |
| `/api/v1/user/workspaces` | GET | `list_user_workspaces` | JWT | <100ms |
| `/api/v1/user/workspace/:id` | DELETE | `delete_workspace` | JWT | <100ms |

#### `web/routes/heartbeat_routes.py` [NEW]

| Endpoint | Method | Handler | Auth | Type |
|----------|--------|---------|------|------|
| `/ws/agents/heartbeat` | WS | `heartbeat_stream` | JWT | WebSocket |
| `/api/v1/agents/status` | GET | `get_all_agent_status` | JWT | REST |

---

### Database Migrations

#### `migrations/phase1_001_user_workspaces.sql` [NEW]

```sql
-- Create user_workspaces table for layout persistence
CREATE TABLE IF NOT EXISTS user_workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workspace_name VARCHAR(255) NOT NULL,
    layout_json JSONB NOT NULL,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, workspace_name)
);

CREATE INDEX idx_user_workspaces_user_id ON user_workspaces(user_id);
CREATE INDEX idx_user_workspaces_default ON user_workspaces(user_id, is_default) WHERE is_default = true;

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_workspace_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER workspace_updated
    BEFORE UPDATE ON user_workspaces
    FOR EACH ROW EXECUTE FUNCTION update_workspace_timestamp();
```

---

### Pytest Tests Required

#### `tests/workspace/test_user_preferences_service.py` [NEW]

| Test Case | Description | Priority |
|-----------|-------------|----------|
| `test_save_workspace_new` | Save new workspace layout | P0 |
| `test_save_workspace_update` | Update existing workspace | P0 |
| `test_get_workspace_exists` | Retrieve existing workspace | P0 |
| `test_get_workspace_not_found` | Handle missing workspace (return default) | P0 |
| `test_list_workspaces_empty` | User has no saved workspaces | P1 |
| `test_list_workspaces_multiple` | User has multiple workspaces | P1 |
| `test_delete_workspace_success` | Delete existing workspace | P1 |
| `test_delete_workspace_not_found` | Delete non-existent workspace | P1 |
| `test_restore_time_under_200ms` | Performance requirement | P0 |
| `test_workspace_schema_validation` | Pydantic validation | P1 |

#### `tests/agents/test_heartbeat_service.py` [NEW]

| Test Case | Description | Priority |
|-----------|-------------|----------|
| `test_record_heartbeat` | Record agent heartbeat | P0 |
| `test_heartbeat_timeout_5s` | Agent dead after 5s | P0 |
| `test_heartbeat_alive` | Agent alive within 5s | P0 |
| `test_get_all_agents` | List all agent statuses | P1 |
| `test_kafka_topic_subscription` | Kafka integration | P1 |

#### `tests/web/test_workspace_routes.py` [NEW]

| Test Case | Description | Priority |
|-----------|-------------|----------|
| `test_save_workspace_authenticated` | Auth required, success | P0 |
| `test_save_workspace_unauthenticated` | 401 response | P0 |
| `test_get_workspace_performance` | Response <200ms | P0 |
| `test_save_workspace_invalid_payload` | 422 validation error | P1 |

---

## Frontend Test Coverage Requirements

### Vitest Tests (frontend2/tests/)

| Component | Test File | Test Cases | Priority |
|-----------|-----------|------------|----------|
| WindowWrapper | `components/WindowWrapper.test.jsx` | Render, drag, resize, z-index | P0 |
| ResizeHandles | `components/ResizeHandles.test.jsx` | All 8 directions, min size | P0 |
| WindowControls | `components/WindowControls.test.jsx` | Close, minimize, maximize | P1 |
| windowStore | `stores/windowStore.test.js` | CRUD, z-index management | P0 |
| Taskbar | `components/Taskbar.test.jsx` | Render, restore windows | P0 |
| TaskbarIcon | `components/TaskbarIcon.test.jsx` | Heartbeat colors, tooltips | P1 |
| useAgentHeartbeat | `hooks/useAgentHeartbeat.test.js` | WS connection, status | P0 |
| useWorkspacePersistence | `hooks/useWorkspacePersistence.test.js` | Save, restore, debounce | P0 |
| SparklineTooltip | `components/SparklineTooltip.test.jsx` | D3 render, empty data | P1 |

**Minimum Coverage Target:** 80%

---

## Nice-to-Have Enhancements

### Performance Optimizations
- [ ] Debounced workspace save (30s after last change)
- [ ] Window position caching in localStorage as fallback
- [ ] WebSocket reconnection logic with exponential backoff

### UX Improvements
- [ ] Window snap-to-edge when dragging near viewport bounds
- [ ] Double-click title bar to maximize/restore
- [ ] Right-click context menu on taskbar icons
- [ ] Keyboard shortcuts: Ctrl+Shift+N (new window), Ctrl+W (close)

### Accessibility
- [ ] Screen reader announcements for window state changes
- [ ] High contrast mode support
- [ ] Reduced motion preference support

### Developer Experience
- [ ] Window state debug overlay (dev mode only)
- [ ] Performance timing in console (dev mode)
- [ ] Storybook stories for all window components

---

## Integration Test Scenarios

### E2E Test: Workspace Persistence Flow
1. Login as test user
2. Open 3 widgets (Fear/Greed, Options Chain, DOM)
3. Arrange widgets in specific layout
4. Click "Save Workspace"
5. Refresh browser
6. Verify layout restored within 200ms
7. Verify all 3 widgets at correct positions

### E2E Test: Agent Heartbeat Monitoring
1. Start test agent via CLI
2. Observe taskbar icon turns green within 2s
3. Stop test agent
4. Observe taskbar icon turns red after 5s

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Initial specification |
| 2026-01-18 | Backend Added | Draft | Full Python services and pytest specs |

