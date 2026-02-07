# Phase 4: Scrum of Scrums Command Center

> **Duration**: 2 Weeks  
> **Status**: [ ] Not Started  
> **Dependencies**: Phase 1, Phase 2, Phase 3  
> **Owner**: TBD  

---

## Phase Overview

Implement the 4-quadrant master command center that provides unified oversight of all 18 departments. This is the primary "Situation Room" view referenced in the mockups.

---

## Deliverables Checklist

### 4.1 Scrum Master Page
- [ ] 4-quadrant grid layout
- [ ] Real-time data loading
- [ ] Global header ribbon
- [ ] Quadrant click-to-expand

### 4.2 Quadrant Components
- [ ] AttackEngine.jsx (Q1)
- [ ] DefenseFortress.jsx (Q2)
- [ ] TreasuryFlow.jsx (Q3)
- [ ] MetaConscience.jsx (Q4)

### 4.3 Global Actions Bar
- [ ] Panic Mode button
- [ ] Cold Haven button
- [ ] Morning Sweep button
- [ ] Resource Conserve button

### 4.4 Center Hub
- [ ] Goal-Probability Delta display
- [ ] Unified health score

---

## Deliverable 4.1: Scrum Master Page

### File Location
`frontend/src/pages/Departments/ScrumMaster.jsx`

### Layout Reference

Per `scrum_of_scrums.jpg` mockup:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  GLOBAL RIBBON: Net Worth $1.2M | Threat: LOW | Alpha: +$847 | Run: 180d │
├─────────────────────────────────┬────────────────────────────────────────┤
│                                 │                                        │
│  Q1: ATTACK ENGINE              │  Q2: DEFENSE FORTRESS                  │
│  ┌─────────────────────────┐    │  ┌────────────────────────────────┐   │
│  │ Alpha Heatmap           │    │  │ Greeks Monitor                 │   │
│  │ [Hunter signals]        │    │  │ [Delta/Gamma/Theta]            │   │
│  │ [Correlation strength]  │    │  │ [Perimeter status]             │   │
│  │ [Trade execution queue] │    │  │ [Solvency gauge]               │   │
│  └─────────────────────────┘    │  └────────────────────────────────┘   │
│                                 │                                        │
├─────────────────────────────────┼────────────────────────────────────────┤
│                                 │                                        │
│  Q3: TREASURY & PLUMBING        │  Q4: META-COGNITION                    │
│  ┌─────────────────────────┐    │  ┌────────────────────────────────┐   │
│  │ Liquidity River (Sankey)│    │  │ Agent Pulse                    │   │
│  │ [Income → Outflow]      │    │  │ [Efficiency scores]            │   │
│  │ [Bill Queue]            │    │  │ [Logic score]                  │   │
│  │ [Burn velocity]         │    │  │ [Compute cost]                 │   │
│  └─────────────────────────┘    │  └────────────────────────────────┘   │
│                                 │                                        │
├─────────────────────────────────┴────────────────────────────────────────┤
│                     CENTER HUB: Goal-Probability Delta 82%               │
├──────────────────────────────────────────────────────────────────────────┤
│  [🔴 Panic Mode]  [🟡 Cold Haven]  [🟢 Morning Sweep]  [🔵 Conserve]     │
└──────────────────────────────────────────────────────────────────────────┘
```

### Implementation

```jsx
import React, { useState, useCallback, Suspense, lazy } from 'react';
import { useDepartmentStore } from '@/stores/departmentStore';
import { GlobalRibbon } from '@/components/Departments/GlobalRibbon';
import { GlobalActionsBar } from '@/components/Departments/GlobalActionsBar';
import { CenterHub } from '@/components/Departments/CenterHub';
import { QuadrantSkeleton } from '@/components/Departments/QuadrantSkeleton';
import styles from './ScrumMaster.module.css';

// Lazy load quadrant components
const AttackEngine = lazy(() => import('@/components/ScrumQuadrants/AttackEngine'));
const DefenseFortress = lazy(() => import('@/components/ScrumQuadrants/DefenseFortress'));
const TreasuryFlow = lazy(() => import('@/components/ScrumQuadrants/TreasuryFlow'));
const MetaConscience = lazy(() => import('@/components/ScrumQuadrants/MetaConscience'));

export const ScrumMaster = () => {
  const [expandedQuadrant, setExpandedQuadrant] = useState(null);
  const pulse = useDepartmentStore(s => s.pulse);
  
  const handleQuadrantClick = useCallback((quadrant) => {
    setExpandedQuadrant(prev => prev === quadrant ? null : quadrant);
  }, []);
  
  const handleCloseExpanded = useCallback(() => {
    setExpandedQuadrant(null);
  }, []);
  
  return (
    <div className={styles.container}>
      {/* Global Ribbon */}
      <GlobalRibbon 
        netWorth={pulse.netWorth}
        threatLevel={pulse.threatLevel}
        dailyAlpha={pulse.dailyAlpha}
        liquidityDays={pulse.liquidityDays}
      />
      
      {/* Main Grid */}
      <div className={`${styles.grid} ${expandedQuadrant ? styles.hasExpanded : ''}`}>
        {/* Q1: Attack Engine */}
        <div 
          className={`${styles.quadrant} ${styles.q1} ${expandedQuadrant === 'q1' ? styles.expanded : ''}`}
          onClick={() => handleQuadrantClick('q1')}
        >
          <Suspense fallback={<QuadrantSkeleton />}>
            <AttackEngine isExpanded={expandedQuadrant === 'q1'} />
          </Suspense>
        </div>
        
        {/* Q2: Defense Fortress */}
        <div 
          className={`${styles.quadrant} ${styles.q2} ${expandedQuadrant === 'q2' ? styles.expanded : ''}`}
          onClick={() => handleQuadrantClick('q2')}
        >
          <Suspense fallback={<QuadrantSkeleton />}>
            <DefenseFortress isExpanded={expandedQuadrant === 'q2'} />
          </Suspense>
        </div>
        
        {/* Q3: Treasury Flow */}
        <div 
          className={`${styles.quadrant} ${styles.q3} ${expandedQuadrant === 'q3' ? styles.expanded : ''}`}
          onClick={() => handleQuadrantClick('q3')}
        >
          <Suspense fallback={<QuadrantSkeleton />}>
            <TreasuryFlow isExpanded={expandedQuadrant === 'q3'} />
          </Suspense>
        </div>
        
        {/* Q4: Meta Conscience */}
        <div 
          className={`${styles.quadrant} ${styles.q4} ${expandedQuadrant === 'q4' ? styles.expanded : ''}`}
          onClick={() => handleQuadrantClick('q4')}
        >
          <Suspense fallback={<QuadrantSkeleton />}>
            <MetaConscience isExpanded={expandedQuadrant === 'q4'} />
          </Suspense>
        </div>
        
        {/* Center Hub */}
        <CenterHub goalProbability={82} />
      </div>
      
      {/* Global Actions */}
      <GlobalActionsBar />
      
      {/* Expanded Overlay */}
      {expandedQuadrant && (
        <button 
          className={styles.closeExpanded}
          onClick={handleCloseExpanded}
        >
          ✕ Close
        </button>
      )}
    </div>
  );
};

export default ScrumMaster;
```

### CSS Module

```css
/* ScrumMaster.module.css */
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
  overflow: hidden;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 8px;
  flex: 1;
  padding: 8px;
  position: relative;
}

.quadrant {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quadrant:hover {
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 242, 255, 0.1);
}

.q1 { border-color: #22c55e33; }
.q2 { border-color: #ef444433; }
.q3 { border-color: #14b8a633; }
.q4 { border-color: #8b5cf633; }

.expanded {
  position: fixed;
  top: 60px;
  left: 16px;
  right: 16px;
  bottom: 80px;
  z-index: 100;
  cursor: default;
}

.hasExpanded .quadrant:not(.expanded) {
  opacity: 0.3;
  pointer-events: none;
}

.closeExpanded {
  position: fixed;
  top: 70px;
  right: 24px;
  z-index: 101;
  padding: 8px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-primary);
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
}
```

---

## Deliverable 4.2: Quadrant Components

### AttackEngine.jsx (Q1)

Combines data from Depts 3, 5, 7

```jsx
// components/ScrumQuadrants/AttackEngine.jsx
import React from 'react';
import { useDepartmentStore } from '@/stores/departmentStore';
import { AlphaHeatmap } from '@/components/D3Visualizations/AlphaHeatmap';
import { SignalPipeline } from './SignalPipeline';
import styles from './Quadrant.module.css';

export const AttackEngine = ({ isExpanded }) => {
  const hunter = useDepartmentStore(s => s.departments[7]);
  const dataScientist = useDepartmentStore(s => s.departments[3]);
  const trader = useDepartmentStore(s => s.departments[5]);
  
  return (
    <div className={`${styles.quadrant} ${styles.attack}`}>
      <header className={styles.header}>
        <h3>Q1 // Alpha & Market Intelligence</h3>
        <span className={styles.status}>
          {hunter.metrics.activeOpportunities} signals
        </span>
      </header>
      
      <div className={styles.content}>
        {isExpanded ? (
          <>
            <AlphaHeatmap 
              signals={hunter.metrics.signals}
              correlations={dataScientist.metrics.correlations}
            />
            <SignalPipeline trader={trader} />
          </>
        ) : (
          <div className={styles.summary}>
            <div className={styles.metric}>
              <span className={styles.label}>Hit Rate</span>
              <span className={styles.value}>{hunter.metrics.signalHitRate}%</span>
            </div>
            <div className={styles.metric}>
              <span className={styles.label}>Correlation</span>
              <span className={styles.value}>{dataScientist.metrics.correlationStrength}</span>
            </div>
            <div className={styles.metric}>
              <span className={styles.label}>Daily P&L</span>
              <span className={`${styles.value} ${trader.metrics.dailyPnL >= 0 ? styles.positive : styles.negative}`}>
                ${trader.metrics.dailyPnL.toLocaleString()}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
```

### DefenseFortress.jsx (Q2)

Combines Depts 6, 8, 10

### TreasuryFlow.jsx (Q3)

Combines Depts 9, 10, 18 with Sankey visualization

### MetaConscience.jsx (Q4)

Combines Depts 15, 16, 17

---

## Deliverable 4.3: Global Actions Bar

### Implementation

```jsx
// components/Departments/GlobalActionsBar.jsx
import React, { useState, useCallback } from 'react';
import { systemService } from '@/services/systemService';
import { useAuthStore } from '@/stores/authStore';
import { ConfirmModal } from '@/components/UI/ConfirmModal';
import { Icon } from '@/components/UI/Icon';
import { toast } from 'react-hot-toast';
import styles from './GlobalActionsBar.module.css';

const ACTIONS = [
  {
    id: 'panic',
    label: 'Panic Mode',
    icon: 'alert-octagon',
    color: '#ef4444',
    description: 'Kill all execution, freeze transfers, flatten positions',
    adminOnly: true,
    dangerous: true
  },
  {
    id: 'cold_haven',
    label: 'Cold Haven',
    icon: 'snowflake',
    color: '#fbbf24',
    description: 'Sweep funds to cold storage accounts',
    adminOnly: true,
    dangerous: true
  },
  {
    id: 'morning_sweep',
    label: 'Morning Sweep',
    icon: 'sun',
    color: '#22c55e',
    description: 'Auto-prune underperforming positions',
    adminOnly: false,
    dangerous: false
  },
  {
    id: 'conserve',
    label: 'Resource Conserve',
    icon: 'battery-low',
    color: '#3b82f6',
    description: 'Switch to local LLM, reduce API calls',
    adminOnly: false,
    dangerous: false
  }
];

export const GlobalActionsBar = () => {
  const [confirmAction, setConfirmAction] = useState(null);
  const [executing, setExecuting] = useState(null);
  const isAdmin = useAuthStore(s => s.user?.role === 'admin');
  
  const handleAction = useCallback(async (actionId) => {
    setExecuting(actionId);
    try {
      await systemService.executeGlobalAction(actionId);
      toast.success(`${actionId} executed successfully`);
    } catch (error) {
      toast.error(`Failed: ${error.message}`);
    } finally {
      setExecuting(null);
      setConfirmAction(null);
    }
  }, []);
  
  const visibleActions = ACTIONS.filter(a => !a.adminOnly || isAdmin);
  
  return (
    <footer className={styles.bar}>
      {visibleActions.map(action => (
        <button
          key={action.id}
          className={styles.actionBtn}
          style={{ '--action-color': action.color }}
          onClick={() => action.dangerous ? setConfirmAction(action) : handleAction(action.id)}
          disabled={executing === action.id}
        >
          <Icon name={action.icon} />
          {action.label}
        </button>
      ))}
      
      {confirmAction && (
        <ConfirmModal
          title={`Confirm ${confirmAction.label}`}
          message={confirmAction.description}
          danger={confirmAction.dangerous}
          onConfirm={() => handleAction(confirmAction.id)}
          onCancel={() => setConfirmAction(null)}
        />
      )}
    </footer>
  );
};
```

---

## E2E Definition of Done

1. **Page Load**: Scrum Master loads in < 1s with skeleton placeholders
2. **Data Flow**: All 4 quadrants show live department metrics within 3s
3. **Expand**: Clicking quadrant expands to full-screen modal
4. **Actions**: Panic Mode requires confirmation, logs to audit table
5. **WebSocket**: Metrics update every 1 second
6. **Mobile**: Stacks 2x2 → 1x4 below 900px width

---

## Phase Sign-Off

- [ ] Scrum Master page complete
- [ ] All 4 quadrants functional
- [ ] Global actions working with auth gates
- [ ] Center hub displays Goal-Probability Delta
- [ ] Real-time updates verified
