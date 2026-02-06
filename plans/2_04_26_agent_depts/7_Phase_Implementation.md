# Phase 7: Venn Intersection Mode

> **Duration**: 2 Weeks  
> **Status**: [ ] Not Started  
> **Dependencies**: Phase 2 Complete  
> **Owner**: TBD  

---

## Phase Overview

Implement the multi-department "Venn Mode" that creates combined views when users drag two departments together. This enables hybrid workflows like "Physicist ∩ Architect = Structural Hedge Suite".

---

## Deliverables Checklist

### 7.1 Venn Trigger Mechanism
- [ ] Drag-and-drop between dept bubbles
- [ ] URL state encoding
- [ ] Store state management

### 7.2 Intersection Pages
- [ ] VennPhysicistArchitect.jsx (Structural Hedge Suite)
- [ ] VennGuardianTrader.jsx (Liquidity Command)
- [ ] VennHunterLawyer.jsx (Due Diligence Station)
- [ ] VennFrontOfficeAuditor.jsx (Auto-Dispute Center)
- [ ] Generic VennIntersection.jsx fallback

### 7.3 Color Blending UI
- [ ] Department color mixing algorithm
- [ ] Gradient backgrounds
- [ ] Dual agent panels

### 7.4 Combined Widget Sets
- [ ] Merged metrics from both departments
- [ ] Cross-department action workflows

---

## Deliverable 7.1: Venn Trigger Mechanism

### Store Integration

Already in `departmentStore.js`:

```javascript
triggerVennMode: (dept1Id, dept2Id) => {
  const depts = get().departments;
  if (!depts[dept1Id] || !depts[dept2Id]) return;
  if (dept1Id === dept2Id) return;
  
  set({ 
    vennIntersection: { 
      dept1: dept1Id, 
      dept2: dept2Id,
      blendColor: blendColors(depts[dept1Id].color, depts[dept2Id].color)
    },
    activeDepartment: null
  });
},

exitVennMode: () => set({ vennIntersection: null }),
```

### Drag-and-Drop Component

```jsx
// components/Departments/DeptBubble.jsx
import React from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { useDepartmentStore } from '@/stores/departmentStore';
import styles from './DeptBubble.module.css';

export const DeptBubble = ({ deptId, config }) => {
  const triggerVenn = useDepartmentStore(s => s.triggerVennMode);
  
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'DEPARTMENT',
    item: { deptId },
    collect: (monitor) => ({
      isDragging: monitor.isDragging()
    })
  }), [deptId]);
  
  const [{ isOver }, drop] = useDrop(() => ({
    accept: 'DEPARTMENT',
    drop: (item) => {
      if (item.deptId !== deptId) {
        triggerVenn(item.deptId, deptId);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver()
    })
  }), [deptId, triggerVenn]);
  
  return (
    <div 
      ref={(node) => drag(drop(node))}
      className={`${styles.bubble} ${isDragging ? styles.dragging : ''} ${isOver ? styles.dropTarget : ''}`}
      style={{ '--dept-color': config.color }}
    >
      <span className={styles.icon}>{config.icon}</span>
      <span className={styles.name}>{config.shortName}</span>
    </div>
  );
};
```

### URL State Encoding

```jsx
// hooks/useVennRouter.js
import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useDepartmentStore } from '@/stores/departmentStore';

export const useVennRouter = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const venn = useDepartmentStore(s => s.vennIntersection);
  const triggerVenn = useDepartmentStore(s => s.triggerVennMode);
  
  // Sync URL → Store on mount
  useEffect(() => {
    const d1 = searchParams.get('venn1');
    const d2 = searchParams.get('venn2');
    
    if (d1 && d2) {
      triggerVenn(parseInt(d1), parseInt(d2));
    }
  }, [searchParams, triggerVenn]);
  
  // Sync Store → URL on change
  useEffect(() => {
    if (venn) {
      navigate(`/dept/venn?venn1=${venn.dept1}&venn2=${venn.dept2}`, { replace: true });
    }
  }, [venn, navigate]);
};
```

---

## Deliverable 7.2: Intersection Pages

### Key Intersection Mappings

| Dept 1 | Dept 2 | Name | Key Features |
|--------|--------|------|--------------|
| 6 (Physicist) | 2 (Architect) | Structural Hedge Suite | Goal-probability delta, insurance slider, Greeks overlay on life plan |
| 10 (Guardian) | 5 (Trader) | Liquidity Command | Margin stress gauge, "pay the bills first" toggle, execution priority |
| 7 (Hunter) | 11 (Lawyer) | Due Diligence Station | Clawback simulator, vested token graph, wash-sale check |
| 14 (Front Office) | 12 (Auditor) | Auto-Dispute Center | Refund pipeline, voice call status, fee recovery tracker |

### Generic Intersection Component

```jsx
// components/Departments/VennIntersection.jsx
import React, { useMemo } from 'react';
import { useDepartmentStore } from '@/stores/departmentStore';
import { DEPT_REGISTRY } from '@/config/departmentRegistry';
import { AgentPanel } from './AgentPanel';
import { DualMetricsPanel } from './DualMetricsPanel';
import { Icon } from '@/components/UI/Icon';
import styles from './VennIntersection.module.css';

export const VennIntersection = () => {
  const venn = useDepartmentStore(s => s.vennIntersection);
  const exitVenn = useDepartmentStore(s => s.exitVennMode);
  const dept1 = useDepartmentStore(s => s.departments[venn?.dept1]);
  const dept2 = useDepartmentStore(s => s.departments[venn?.dept2]);
  
  const config1 = DEPT_REGISTRY[venn?.dept1];
  const config2 = DEPT_REGISTRY[venn?.dept2];
  
  const intersectionName = useMemo(() => {
    // Named intersections
    const named = {
      '6-2': 'Structural Hedge Suite',
      '2-6': 'Structural Hedge Suite',
      '10-5': 'Liquidity Command',
      '5-10': 'Liquidity Command',
      '7-11': 'Due Diligence Station',
      '11-7': 'Due Diligence Station',
      '14-12': 'Auto-Dispute Center',
      '12-14': 'Auto-Dispute Center'
    };
    
    const key = `${venn?.dept1}-${venn?.dept2}`;
    return named[key] || `${config1?.shortName} ∩ ${config2?.shortName}`;
  }, [venn, config1, config2]);
  
  if (!venn || !dept1 || !dept2) {
    return null;
  }
  
  return (
    <div 
      className={styles.container}
      style={{
        '--blend-color': venn.blendColor,
        '--color1': config1.color,
        '--color2': config2.color
      }}
    >
      {/* Header with gradient */}
      <header className={styles.header}>
        <div className={styles.deptIndicators}>
          <span style={{ color: config1.color }}>
            <Icon name={config1.icon} /> {config1.name}
          </span>
          <span className={styles.intersect}>∩</span>
          <span style={{ color: config2.color }}>
            <Icon name={config2.icon} /> {config2.name}
          </span>
        </div>
        <h1 className={styles.title}>{intersectionName}</h1>
        <button className={styles.exitBtn} onClick={exitVenn}>
          Exit Venn Mode
        </button>
      </header>
      
      {/* Main content - dual panels */}
      <div className={styles.content}>
        {/* Left: Dept 1 agents */}
        <aside className={styles.agentPanel} style={{ borderColor: config1.color }}>
          <h3>Team from {config1.shortName}</h3>
          <AgentPanel 
            departmentId={venn.dept1} 
            agents={dept1.agents}
            compact
          />
        </aside>
        
        {/* Center: Combined visualization or custom component */}
        <main className={styles.centerArea}>
          <VennVisualization 
            dept1={dept1}
            dept2={dept2}
            config1={config1}
            config2={config2}
          />
        </main>
        
        {/* Right: Dept 2 agents */}
        <aside className={styles.agentPanel} style={{ borderColor: config2.color }}>
          <h3>Team from {config2.shortName}</h3>
          <AgentPanel 
            departmentId={venn.dept2} 
            agents={dept2.agents}
            compact
          />
        </aside>
      </div>
      
      {/* Combined metrics */}
      <DualMetricsPanel 
        metrics1={dept1.metrics}
        metrics2={dept2.metrics}
        label1={config1.primaryMetricLabel}
        label2={config2.primaryMetricLabel}
      />
      
      {/* Cross-department actions */}
      <footer className={styles.actionBar}>
        <VennActions dept1Id={venn.dept1} dept2Id={venn.dept2} />
      </footer>
    </div>
  );
};
```

### Specific Intersection: Structural Hedge Suite

```jsx
// pages/Departments/VennPhysicistArchitect.jsx
import React, { useState } from 'react';
import { VennIntersection } from '@/components/Departments/VennIntersection';
import { GoalProbabilityDelta } from '@/components/Widgets/GoalProbabilityDelta';
import { InsuranceSlider } from '@/components/Widgets/InsuranceSlider';
import { GreeksOverlay } from '@/components/Widgets/GreeksOverlay';
import styles from './VennPages.module.css';

export const VennPhysicistArchitect = () => {
  const [insuranceLevel, setInsuranceLevel] = useState(50);
  const [selectedGoal, setSelectedGoal] = useState(null);
  
  return (
    <VennIntersection customContent={
      <div className={styles.structuralHedge}>
        {/* Main widget: Goal-Probability Delta */}
        <GoalProbabilityDelta 
          onGoalSelect={setSelectedGoal}
        />
        
        {/* Greeks overlay on selected goal */}
        {selectedGoal && (
          <GreeksOverlay 
            goal={selectedGoal}
            showDelta
            showTheta
            showVega
          />
        )}
        
        {/* Insurance slider */}
        <div className={styles.insuranceControl}>
          <label>Insurance Level: {insuranceLevel}%</label>
          <InsuranceSlider 
            value={insuranceLevel}
            onChange={setInsuranceLevel}
            min={0}
            max={100}
          />
          <div className={styles.insuranceInfo}>
            <span>Cost: ${(insuranceLevel * 12).toLocaleString()}/yr</span>
            <span>Protection: ${(insuranceLevel * 10000).toLocaleString()}</span>
          </div>
        </div>
      </div>
    } />
  );
};
```

### Specific Intersection: Liquidity Command

```jsx
// pages/Departments/VennGuardianTrader.jsx
import React, { useState } from 'react';
import { VennIntersection } from '@/components/Departments/VennIntersection';
import { MarginStressGauge } from '@/components/Widgets/MarginStressGauge';
import { BillsPriorityToggle } from '@/components/Widgets/BillsPriorityToggle';
import { ExecutionQueue } from '@/components/Widgets/ExecutionQueue';

export const VennGuardianTrader = () => {
  const [billsFirst, setBillsFirst] = useState(true);
  
  return (
    <VennIntersection customContent={
      <div className={styles.liquidityCommand}>
        {/* Margin stress gauge */}
        <MarginStressGauge />
        
        {/* Priority toggle */}
        <BillsPriorityToggle 
          enabled={billsFirst}
          onChange={setBillsFirst}
          label="Pay Bills Before Trading"
        />
        
        {/* Execution queue filtered by liquidity */}
        <ExecutionQueue 
          filterByLiquidity={billsFirst}
        />
      </div>
    } />
  );
};
```

---

## Deliverable 7.3: Color Blending UI

### Blend Algorithm

Already in store, enhanced version:

```javascript
// utils/colorUtils.js

/**
 * Blend two hex colors for Venn intersection UI
 */
export function blendColors(color1, color2, ratio = 0.5) {
  const hex = (c) => parseInt(c.slice(1), 16);
  
  const r1 = (hex(color1) >> 16) & 255;
  const g1 = (hex(color1) >> 8) & 255;
  const b1 = hex(color1) & 255;
  
  const r2 = (hex(color2) >> 16) & 255;
  const g2 = (hex(color2) >> 8) & 255;
  const b2 = hex(color2) & 255;
  
  const r = Math.round(r1 * (1 - ratio) + r2 * ratio);
  const g = Math.round(g1 * (1 - ratio) + g2 * ratio);
  const b = Math.round(b1 * (1 - ratio) + b2 * ratio);
  
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

/**
 * Generate CSS gradient for Venn header
 */
export function vennGradient(color1, color2) {
  return `linear-gradient(135deg, ${color1}33 0%, ${blendColors(color1, color2)}66 50%, ${color2}33 100%)`;
}
```

### CSS Styling

```css
/* VennIntersection.module.css */
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
}

.header {
  padding: 16px 24px;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--color1) 30%, transparent) 0%,
    color-mix(in srgb, var(--blend-color) 50%, transparent) 50%,
    color-mix(in srgb, var(--color2) 30%, transparent) 100%
  );
  border-bottom: 2px solid var(--blend-color);
}

.deptIndicators {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 0.875rem;
}

.intersect {
  color: var(--blend-color);
  font-size: 1.25rem;
  font-weight: bold;
}

.title {
  font-size: 1.75rem;
  color: var(--text-primary);
  text-shadow: 0 0 20px var(--blend-color);
}

.content {
  display: flex;
  flex: 1;
  gap: 8px;
  padding: 8px;
}

.agentPanel {
  width: 200px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 8px;
  border-left: 3px solid;
}

.centerArea {
  flex: 1;
  background: var(--bg-secondary);
  border-radius: 8px;
  overflow: hidden;
}

.actionBar {
  display: flex;
  gap: 12px;
  padding: 12px 24px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--blend-color);
}

/* Responsive */
@media (max-width: 1200px) {
  .content {
    flex-direction: column;
  }
  
  .agentPanel {
    width: 100%;
    max-height: 150px;
    overflow-y: auto;
  }
}
```

---

## Deliverable 7.4: Combined Widget Sets

### DualMetricsPanel Component

```jsx
// components/Departments/DualMetricsPanel.jsx
import React from 'react';
import styles from './DualMetricsPanel.module.css';

export const DualMetricsPanel = ({ 
  metrics1, 
  metrics2, 
  label1, 
  label2,
  unit1 = '',
  unit2 = ''
}) => {
  const primaryValue1 = Object.values(metrics1)[0];
  const primaryValue2 = Object.values(metrics2)[0];
  
  return (
    <div className={styles.panel}>
      <div className={styles.metric}>
        <span className={styles.label}>{label1}</span>
        <span className={styles.value}>{primaryValue1}{unit1}</span>
      </div>
      
      <div className={styles.divider} />
      
      <div className={styles.metric}>
        <span className={styles.label}>{label2}</span>
        <span className={styles.value}>{primaryValue2}{unit2}</span>
      </div>
      
      {/* Combined/derived metrics */}
      <div className={styles.combined}>
        <span className={styles.label}>Combined Score</span>
        <span className={styles.value}>
          {((primaryValue1 + primaryValue2) / 2).toFixed(1)}
        </span>
      </div>
    </div>
  );
};
```

### VennActions Component

```jsx
// components/Departments/VennActions.jsx
import React, { useCallback } from 'react';
import { Icon } from '@/components/UI/Icon';
import { vennService } from '@/services/vennService';
import styles from './VennActions.module.css';

const VENN_ACTIONS = {
  '6-2': [
    { id: 'hedge_goals', label: 'Hedge All Goals', icon: 'shield' },
    { id: 'simulate_crash', label: 'Crash Simulation', icon: 'activity' },
    { id: 'optimize_insurance', label: 'Optimize Insurance', icon: 'sliders' }
  ],
  '10-5': [
    { id: 'liquidity_check', label: 'Liquidity Check', icon: 'droplet' },
    { id: 'margin_stress', label: 'Margin Stress Test', icon: 'alert-triangle' },
    { id: 'pay_bills', label: 'Pay Pending Bills', icon: 'file-text' }
  ],
  '7-11': [
    { id: 'due_diligence', label: 'Run Due Diligence', icon: 'search' },
    { id: 'check_wash', label: 'Check Wash Sales', icon: 'repeat' },
    { id: 'vest_schedule', label: 'View Vest Schedule', icon: 'calendar' }
  ],
  '14-12': [
    { id: 'dispute_scan', label: 'Scan for Disputes', icon: 'flag' },
    { id: 'auto_refund', label: 'Auto-Refund Queue', icon: 'refresh-cw' },
    { id: 'fee_recovery', label: 'Fee Recovery', icon: 'dollar-sign' }
  ]
};

export const VennActions = ({ dept1Id, dept2Id }) => {
  const key = `${dept1Id}-${dept2Id}`;
  const altKey = `${dept2Id}-${dept1Id}`;
  const actions = VENN_ACTIONS[key] || VENN_ACTIONS[altKey] || [];
  
  const handleAction = useCallback(async (actionId) => {
    await vennService.executeAction(dept1Id, dept2Id, actionId);
  }, [dept1Id, dept2Id]);
  
  if (actions.length === 0) {
    return <span className={styles.noActions}>No specific actions for this intersection</span>;
  }
  
  return (
    <>
      {actions.map(action => (
        <button
          key={action.id}
          className={styles.actionBtn}
          onClick={() => handleAction(action.id)}
        >
          <Icon name={action.icon} />
          {action.label}
        </button>
      ))}
    </>
  );
};
```

---

## Route Registration

```jsx
// In App.jsx routes
<Route path="/dept/venn" element={<VennRouter />} />

// VennRouter.jsx - routes to specific or generic intersection
import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { VennIntersection } from '@/components/Departments/VennIntersection';
import { VennPhysicistArchitect } from './VennPhysicistArchitect';
import { VennGuardianTrader } from './VennGuardianTrader';
import { VennHunterLawyer } from './VennHunterLawyer';
import { VennFrontOfficeAuditor } from './VennFrontOfficeAuditor';

const SPECIFIC_VENNS = {
  '6-2': VennPhysicistArchitect,
  '2-6': VennPhysicistArchitect,
  '10-5': VennGuardianTrader,
  '5-10': VennGuardianTrader,
  '7-11': VennHunterLawyer,
  '11-7': VennHunterLawyer,
  '14-12': VennFrontOfficeAuditor,
  '12-14': VennFrontOfficeAuditor
};

export const VennRouter = () => {
  const [searchParams] = useSearchParams();
  const d1 = searchParams.get('venn1');
  const d2 = searchParams.get('venn2');
  
  const key = `${d1}-${d2}`;
  const SpecificComponent = SPECIFIC_VENNS[key];
  
  if (SpecificComponent) {
    return <SpecificComponent />;
  }
  
  return <VennIntersection />;
};
```

---

## E2E Definition of Done

1. **Trigger**: Dragging dept 6 onto dept 2 opens Structural Hedge Suite
2. **URL**: URL shows `/dept/venn?venn1=6&venn2=2`
3. **Visual**: Header gradient blends both department colors
4. **Agents**: Both department agent panels visible
5. **Actions**: Cross-department actions execute successfully
6. **Exit**: "Exit Venn Mode" returns to previous view
7. **Deep Link**: Direct URL `/dept/venn?venn1=10&venn2=5` works

---

## Phase Sign-Off

- [ ] Drag-and-drop trigger working
- [ ] 4 specific intersection pages complete
- [ ] Generic fallback for undefined intersections
- [ ] Color blending UI polished
- [ ] URL state persists and restores
- [ ] All E2E tests passing
