# Phase 2: Core Department Dashboards

> **Duration**: 4 Weeks  
> **Status**: [ ] Not Started  
> **Dependencies**: Phase 1 Complete  
> **Owner**: TBD  

---

## Phase Overview

Implement 18 department-specific dashboard pages using a shared template component. Each dashboard displays a central D3.js visualization, agent panel, metrics sidebar, and action workflows per mockup specifications.

---

## Deliverables Checklist

### 2.1 Department Dashboard Template
- [ ] Implementation Complete
- [ ] Responsive Layout Verified
- [ ] Theme Support (Dark/Light)
- [ ] Storybook Story Created

### 2.2 Individual Department Pages (18 Total)
- [ ] DeptOrchestrator.jsx
- [ ] DeptArchitect.jsx
- [ ] DeptDataScientist.jsx
- [ ] DeptStrategist.jsx
- [ ] DeptTrader.jsx
- [ ] DeptPhysicist.jsx
- [ ] DeptHunter.jsx
- [ ] DeptSentry.jsx
- [ ] DeptSteward.jsx
- [ ] DeptGuardian.jsx
- [ ] DeptLawyer.jsx
- [ ] DeptAuditor.jsx
- [ ] DeptEnvoy.jsx
- [ ] DeptFrontOffice.jsx
- [ ] DeptHistorian.jsx
- [ ] DeptStressTester.jsx
- [ ] DeptRefiner.jsx
- [ ] DeptBanker.jsx

### 2.3 Route Registration
- [ ] All 18 routes registered in App.jsx
- [ ] Lazy loading implemented
- [ ] Suspense fallbacks configured

### 2.4 Menu Integration
- [ ] Departments submenu added to MenuBar.jsx
- [ ] Keyboard navigation works
- [ ] Scrum of Scrums at top of menu

---

## Deliverable 2.1: Department Dashboard Template

### File Location
`frontend/src/components/Departments/DepartmentDashboard.jsx`

### Layout Specification

```
┌──────────────────────────────────────────────────────────────────────────┐
│  HEADER                                                                   │
│  [Icon] Department Name                    [Return to Scrum] [Settings]  │
├─────────────────────┬────────────────────────────────────────────────────┤
│                     │                                                     │
│  AGENT PANEL        │           CENTRAL D3.JS CANVAS                      │
│  (280px fixed)      │           (flex-grow)                               │
│                     │                                                     │
│  ┌───────────────┐  │     ┌──────────────────────────────────────────┐   │
│  │ Agent 1    ● │  │     │                                          │   │
│  │ [Invoke]     │  │     │        D3 Visualization Area             │   │
│  ├───────────────┤  │     │        (Mounted via useD3 hook)          │   │
│  │ Agent 2    ○ │  │     │                                          │   │
│  │ [Invoke]     │  │     │                                          │   │
│  ├───────────────┤  │     │                                          │   │
│  │ Agent 3    ● │  │     │                                          │   │
│  │ [Invoke]     │  │     └──────────────────────────────────────────┘   │
│  ├───────────────┤  │                                                     │
│  │ Agent 4    ○ │  │  ───────────────────────────────────────────────   │
│  │ [Invoke]     │  │                                                     │
│  ├───────────────┤  │           METRICS PANEL (Right Sidebar)            │
│  │ Agent 5    ○ │  │     ┌──────────────────────────────────────────┐   │
│  │ [Invoke]     │  │     │ Primary Metric: 42ms                     │   │
│  ├───────────────┤  │     │ Secondary: $1,234                        │   │
│  │ Agent 6    ● │  │     │ Status: ● LIVE                           │   │
│  │ [Invoke]     │  │     └──────────────────────────────────────────┘   │
│  └───────────────┘  │                                                     │
├─────────────────────┴────────────────────────────────────────────────────┤
│  ACTION WORKFLOWS                                                         │
│  [Primary Action]    [Secondary Action]    [Tertiary Action]             │
└──────────────────────────────────────────────────────────────────────────┘
```

### Component Props Interface

```typescript
interface DepartmentDashboardProps {
  departmentId: number;
  d3Config: {
    type: 'force-directed' | 'sunburst' | 'sankey' | 'radial-tree' | 
          '3d-surface' | 'globe-mesh' | 'timeline' | 'flowchart' | 
          'fractal' | 'bubble-chart';
    data?: any;
    options?: Record<string, any>;
  };
  actions: {
    primary: { label: string; onClick: () => void; icon?: string };
    secondary?: { label: string; onClick: () => void; icon?: string };
    tertiary?: { label: string; onClick: () => void; icon?: string };
  };
  customMetrics?: React.ReactNode;
}
```

### Implementation

```jsx
import React, { useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDepartmentStore } from '@/stores/departmentStore';
import { DEPT_REGISTRY } from '@/config/departmentRegistry';
import { AgentPanel } from './AgentPanel';
import { MetricsPanel } from './MetricsPanel';
import { D3Canvas } from '../D3Visualizations/D3Canvas';
import { Icon } from '@/components/UI/Icon';
import styles from './DepartmentDashboard.module.css';

export const DepartmentDashboard = ({ 
  departmentId, 
  d3Config, 
  actions,
  customMetrics 
}) => {
  const navigate = useNavigate();
  const department = useDepartmentStore(s => s.departments[departmentId]);
  const config = DEPT_REGISTRY[departmentId];
  
  const handleReturnToScrum = useCallback(() => {
    navigate('/dept/scrum-master');
  }, [navigate]);
  
  const headerStyle = useMemo(() => ({
    '--dept-color': config.color,
    '--dept-color-light': `${config.color}33`
  }), [config.color]);
  
  if (!department || !config) {
    return <div className={styles.error}>Department not found</div>;
  }
  
  return (
    <div className={styles.dashboard} style={headerStyle}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerLeft}>
          <Icon name={config.icon} className={styles.deptIcon} />
          <h1 className={styles.title}>{config.name}</h1>
          <span className={`${styles.status} ${styles[department.status]}`}>
            {department.status}
          </span>
        </div>
        <div className={styles.headerRight}>
          <button 
            className={styles.returnBtn}
            onClick={handleReturnToScrum}
          >
            ← Return to Scrum
          </button>
          <button className={styles.settingsBtn}>
            <Icon name="settings" />
          </button>
        </div>
      </header>
      
      {/* Main Content */}
      <div className={styles.content}>
        {/* Agent Panel - Left Sidebar */}
        <aside className={styles.agentPanel}>
          <AgentPanel 
            departmentId={departmentId}
            agents={department.agents}
          />
        </aside>
        
        {/* Center - D3 Visualization + Metrics */}
        <main className={styles.mainArea}>
          <div className={styles.d3Container}>
            <D3Canvas 
              type={d3Config.type}
              data={d3Config.data}
              options={d3Config.options}
              departmentColor={config.color}
            />
          </div>
          
          <aside className={styles.metricsPanel}>
            {customMetrics || (
              <MetricsPanel 
                metrics={department.metrics}
                primaryMetric={config.primaryMetric}
                primaryLabel={config.primaryMetricLabel}
                primaryUnit={config.primaryMetricUnit}
              />
            )}
          </aside>
        </main>
      </div>
      
      {/* Action Workflows - Bottom Bar */}
      <footer className={styles.actionBar}>
        <button 
          className={styles.primaryAction}
          onClick={actions.primary.onClick}
        >
          {actions.primary.icon && <Icon name={actions.primary.icon} />}
          {actions.primary.label}
        </button>
        
        {actions.secondary && (
          <button 
            className={styles.secondaryAction}
            onClick={actions.secondary.onClick}
          >
            {actions.secondary.icon && <Icon name={actions.secondary.icon} />}
            {actions.secondary.label}
          </button>
        )}
        
        {actions.tertiary && (
          <button 
            className={styles.tertiaryAction}
            onClick={actions.tertiary.onClick}
          >
            {actions.tertiary.icon && <Icon name={actions.tertiary.icon} />}
            {actions.tertiary.label}
          </button>
        )}
      </footer>
    </div>
  );
};

export default DepartmentDashboard;
```

### CSS Module

```css
/* DepartmentDashboard.module.css */
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
  color: var(--text-primary);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: var(--dept-color-light);
  border-bottom: 1px solid var(--dept-color);
}

.headerLeft {
  display: flex;
  align-items: center;
  gap: 12px;
}

.deptIcon {
  width: 32px;
  height: 32px;
  color: var(--dept-color);
}

.title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.status.active { background: #22c55e33; color: #22c55e; }
.status.inactive { background: #6b728033; color: #6b7280; }
.status.error { background: #ef444433; color: #ef4444; }

.headerRight {
  display: flex;
  gap: 12px;
}

.returnBtn {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border-primary);
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-primary);
}

.returnBtn:hover {
  background: var(--bg-hover);
}

.content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.agentPanel {
  width: 280px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-primary);
  overflow-y: auto;
  padding: 16px;
}

.mainArea {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 16px;
}

.d3Container {
  flex: 1;
  min-height: 400px;
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
}

.metricsPanel {
  height: 120px;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 16px;
}

.actionBar {
  display: flex;
  gap: 16px;
  padding: 16px 24px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-primary);
}

.primaryAction {
  padding: 12px 24px;
  background: var(--dept-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.secondaryAction,
.tertiaryAction {
  padding: 12px 24px;
  background: transparent;
  border: 1px solid var(--border-primary);
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Responsive */
@media (max-width: 1200px) {
  .agentPanel {
    width: 220px;
  }
}

@media (max-width: 900px) {
  .content {
    flex-direction: column;
  }
  
  .agentPanel {
    width: 100%;
    height: auto;
    max-height: 200px;
    border-right: none;
    border-bottom: 1px solid var(--border-primary);
  }
}
```

### E2E Definition of Done

1. **Render Test**
   - [ ] Component renders without console errors
   - [ ] All child components mount correctly

2. **Layout Verification**
   - [ ] Header shows department name and icon
   - [ ] Agent panel on left (280px)
   - [ ] D3 canvas in center (flex)
   - [ ] Metrics panel visible
   - [ ] Action bar at bottom

3. **Responsive Check**
   - [ ] At 1200px: Agent panel shrinks to 220px
   - [ ] At 900px: Stacks vertically

4. **Theme Check**
   - [ ] Dark mode renders correctly
   - [ ] Light mode renders correctly
   - [ ] Department color applies to accents

---

## Deliverable 2.2: Individual Department Pages

### Directory Structure
```
frontend/src/pages/Departments/
├── DeptOrchestrator.jsx
├── DeptArchitect.jsx
├── DeptDataScientist.jsx
├── DeptStrategist.jsx
├── DeptTrader.jsx
├── DeptPhysicist.jsx
├── DeptHunter.jsx
├── DeptSentry.jsx
├── DeptSteward.jsx
├── DeptGuardian.jsx
├── DeptLawyer.jsx
├── DeptAuditor.jsx
├── DeptEnvoy.jsx
├── DeptFrontOffice.jsx
├── DeptHistorian.jsx
├── DeptStressTester.jsx
├── DeptRefiner.jsx
├── DeptBanker.jsx
└── index.js
```

### Template for Each Page

Each page follows this pattern with department-specific customizations:

```jsx
// Example: DeptTrader.jsx
import React, { useCallback, useEffect, useState } from 'react';
import { DepartmentDashboard } from '@/components/Departments/DepartmentDashboard';
import { useDepartmentStore } from '@/stores/departmentStore';
import { useDepartmentSocket } from '@/hooks/useDepartmentSocket';
import { traderService } from '@/services/traderService';

const DEPT_ID = 5;

export const DeptTrader = () => {
  const [d3Data, setD3Data] = useState(null);
  const updateMetrics = useDepartmentStore(s => s.updateDepartmentMetrics);
  
  // WebSocket subscription
  useDepartmentSocket(DEPT_ID, (message) => {
    if (message.type === 'metrics') {
      updateMetrics(DEPT_ID, message.data);
    }
    if (message.type === 'd3_update') {
      setD3Data(message.data);
    }
  });
  
  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      const orderBook = await traderService.getOrderBookData();
      setD3Data(orderBook);
    };
    loadData();
  }, []);
  
  // Action handlers
  const handleFlattenAll = useCallback(async () => {
    if (confirm('Flatten all positions? This cannot be undone.')) {
      await traderService.flattenAllPositions();
    }
  }, []);
  
  const handlePauseExecution = useCallback(async () => {
    await traderService.pauseExecution();
  }, []);
  
  const handleManualOrder = useCallback(() => {
    // Open order entry modal
  }, []);
  
  return (
    <DepartmentDashboard
      departmentId={DEPT_ID}
      d3Config={{
        type: 'bubble-chart',
        data: d3Data,
        options: {
          xAxis: 'price',
          yAxis: 'volume',
          sizeBy: 'impact',
          colorBy: 'side' // bid=green, ask=red
        }
      }}
      actions={{
        primary: {
          label: 'Flatten All',
          onClick: handleFlattenAll,
          icon: 'x-circle'
        },
        secondary: {
          label: 'Pause Execution',
          onClick: handlePauseExecution,
          icon: 'pause'
        },
        tertiary: {
          label: 'Manual Order',
          onClick: handleManualOrder,
          icon: 'edit'
        }
      }}
    />
  );
};

export default DeptTrader;
```

### Department-Specific Configurations

| Dept | D3 Type | Primary Action | Secondary | Tertiary |
|------|---------|----------------|-----------|----------|
| 1 Orchestrator | force-directed | Kill Switch | Context Save | System Restart |
| 2 Architect | sunburst | Update Plan | Export PDF | New Simulation |
| 3 Data Scientist | force-directed | Deploy Model | Refresh Scrape | Toggle Anomaly |
| 4 Strategist | flowchart | Push to Trader | Stress Test | Halt Logic |
| 5 Trader | bubble-chart | Flatten All | Pause Execution | Manual Order |
| 6 Physicist | 3d-surface | Neutralize Delta | Scan Premium | Morph Position |
| 7 Hunter | bubble-chart | Send to Backtest | Toggle Sentiment | Commit Bounty |
| 8 Sentry | globe-mesh | Visual Blackout | Rotate Credentials | Deep Scan |
| 9 Steward | sunburst | Run Procurement | Schedule Maintenance | Sync Wellness |
| 10 Guardian | sankey | Execute Sweep | Pause Bills | Emergency Fund |
| 11 Lawyer | radial-tree | Harvest Losses | Audit Documents | Check Wash Sale |
| 12 Auditor | sunburst | Run Reconciliation | Export Report | Flag Slippage |
| 13 Envoy | radial-tree | Schedule Meeting | Run CRM Sync | Draft Pitch |
| 14 Front Office | force-directed | Generate Brief | Clear Inbox | Start Voice Call |
| 15 Historian | timeline | New Journal Entry | Compare Scenario | Export Timeline |
| 16 Stress-Tester | fractal | Run War Game | Inject Black Swan | Calculate Liquidation |
| 17 Refiner | force-directed | Optimize Prompts | Purge Memory | Tune Agent |
| 18 Banker | sankey | Execute Transfer | Categorize Batch | Reserve Taxes |

### E2E Definition of Done (Per Page)

1. **Route Access**
   - [ ] Navigate via URL: `/dept/{slug}`
   - [ ] Navigate via menu click

2. **Visual Match**
   - [ ] 80%+ match to mockup screenshot

3. **D3 Visualization**
   - [ ] Renders within 500ms
   - [ ] Shows placeholder during load

4. **Agent Panel**
   - [ ] Shows 6 agents
   - [ ] Status indicators update

5. **Actions**
   - [ ] Primary action calls API
   - [ ] Confirmation dialogs work

---

## Deliverable 2.3: Route Registration

### File Modification
`frontend/src/App.jsx`

```jsx
import React, { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { LoadingSpinner } from '@/components/UI/LoadingSpinner';

// Lazy load department pages
const ScrumMaster = lazy(() => import('./pages/Departments/ScrumMaster'));
const DeptOrchestrator = lazy(() => import('./pages/Departments/DeptOrchestrator'));
const DeptArchitect = lazy(() => import('./pages/Departments/DeptArchitect'));
const DeptDataScientist = lazy(() => import('./pages/Departments/DeptDataScientist'));
const DeptStrategist = lazy(() => import('./pages/Departments/DeptStrategist'));
const DeptTrader = lazy(() => import('./pages/Departments/DeptTrader'));
const DeptPhysicist = lazy(() => import('./pages/Departments/DeptPhysicist'));
const DeptHunter = lazy(() => import('./pages/Departments/DeptHunter'));
const DeptSentry = lazy(() => import('./pages/Departments/DeptSentry'));
const DeptSteward = lazy(() => import('./pages/Departments/DeptSteward'));
const DeptGuardian = lazy(() => import('./pages/Departments/DeptGuardian'));
const DeptLawyer = lazy(() => import('./pages/Departments/DeptLawyer'));
const DeptAuditor = lazy(() => import('./pages/Departments/DeptAuditor'));
const DeptEnvoy = lazy(() => import('./pages/Departments/DeptEnvoy'));
const DeptFrontOffice = lazy(() => import('./pages/Departments/DeptFrontOffice'));
const DeptHistorian = lazy(() => import('./pages/Departments/DeptHistorian'));
const DeptStressTester = lazy(() => import('./pages/Departments/DeptStressTester'));
const DeptRefiner = lazy(() => import('./pages/Departments/DeptRefiner'));
const DeptBanker = lazy(() => import('./pages/Departments/DeptBanker'));

// Inside Routes component:
<Suspense fallback={<LoadingSpinner />}>
  <Routes>
    {/* Department Routes */}
    <Route path="/dept/scrum-master" element={<ScrumMaster />} />
    <Route path="/dept/orchestrator" element={<DeptOrchestrator />} />
    <Route path="/dept/architect" element={<DeptArchitect />} />
    <Route path="/dept/data-scientist" element={<DeptDataScientist />} />
    <Route path="/dept/strategist" element={<DeptStrategist />} />
    <Route path="/dept/trader" element={<DeptTrader />} />
    <Route path="/dept/physicist" element={<DeptPhysicist />} />
    <Route path="/dept/hunter" element={<DeptHunter />} />
    <Route path="/dept/sentry" element={<DeptSentry />} />
    <Route path="/dept/steward" element={<DeptSteward />} />
    <Route path="/dept/guardian" element={<DeptGuardian />} />
    <Route path="/dept/lawyer" element={<DeptLawyer />} />
    <Route path="/dept/auditor" element={<DeptAuditor />} />
    <Route path="/dept/envoy" element={<DeptEnvoy />} />
    <Route path="/dept/front-office" element={<DeptFrontOffice />} />
    <Route path="/dept/historian" element={<DeptHistorian />} />
    <Route path="/dept/stress-tester" element={<DeptStressTester />} />
    <Route path="/dept/refiner" element={<DeptRefiner />} />
    <Route path="/dept/banker" element={<DeptBanker />} />
    
    {/* ... existing routes */}
  </Routes>
</Suspense>
```

---

## Deliverable 2.4: Menu Integration

### File Modification
`frontend/src/components/Navigation/MenuBar.jsx`

Add to Routes dropdown:

```javascript
const departmentsMenu = {
  label: "Departments",
  action: "nav-departments",
  submenu: [
    { label: "⚡ Scrum of Scrums", action: "nav-scrum-master", highlight: true },
    { type: "divider" },
    
    { label: "📊 Attack Engine", disabled: true },
    { label: "  Data Scientist", action: "nav-dept-data-scientist" },
    { label: "  Strategist", action: "nav-dept-strategist" },
    { label: "  Trader", action: "nav-dept-trader" },
    { label: "  Physicist", action: "nav-dept-physicist" },
    { label: "  Hunter", action: "nav-dept-hunter" },
    { type: "divider" },
    
    { label: "🛡️ Defense Fortress", disabled: true },
    { label: "  Sentry", action: "nav-dept-sentry" },
    { label: "  Guardian", action: "nav-dept-guardian" },
    { label: "  Lawyer", action: "nav-dept-lawyer" },
    { label: "  Auditor", action: "nav-dept-auditor" },
    { type: "divider" },
    
    { label: "🏠 Household", disabled: true },
    { label: "  Steward", action: "nav-dept-steward" },
    { label: "  Envoy", action: "nav-dept-envoy" },
    { label: "  Front Office", action: "nav-dept-front-office" },
    { label: "  Banker", action: "nav-dept-banker" },
    { type: "divider" },
    
    { label: "🧠 Meta-Cognition", disabled: true },
    { label: "  Orchestrator", action: "nav-dept-orchestrator" },
    { label: "  Architect", action: "nav-dept-architect" },
    { label: "  Historian", action: "nav-dept-historian" },
    { label: "  Stress-Tester", action: "nav-dept-stress-tester" },
    { label: "  Refiner", action: "nav-dept-refiner" }
  ]
};
```

---

## Phase Sign-Off Checklist

### Builder Verification

- [ ] Dashboard template component complete
- [ ] All 18 department pages implemented
- [ ] Routes registered with lazy loading
- [ ] Menu integration complete
- [ ] All pages render without errors
- [ ] Visual match to mockups (80%+)

### Reviewer Verification

- [ ] Code follows React best practices
- [ ] CSS follows design system variables
- [ ] Accessibility checked (keyboard nav, ARIA)
- [ ] Performance acceptable (< 500ms render)

### Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Builder | | | |
| Reviewer | | | |
| Product | | | |
