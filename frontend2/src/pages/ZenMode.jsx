import React, { useState, useEffect } from 'react';
import { useWealthStore } from '../stores/wealthStore';
import GoalProgress from '../widgets/Zen/GoalProgress';
import RetirementGauge from '../widgets/Zen/RetirementGauge';
import AutopilotToggle from '../widgets/Zen/AutopilotToggle';
import HomeostasisOverlay from '../widgets/Zen/HomeostasisOverlay';
import '../widgets/Zen/ZenMode.css';

export default function ZenMode() {
  const fetchAssets = useWealthStore((state) => state.fetchAssets);
  const [autopilot, setAutopilot] = useState(false);

  useEffect(() => {
    fetchAssets();
  }, [fetchAssets]);

  return (
    <div className="zen-mode-container page-shell-os animate-fade-in">
       <HomeostasisOverlay active={autopilot} onUnlock={() => setAutopilot(false)} />
       
       <header className="zen-header">
          <h1 className="zen-title">The Sanctuary</h1>
          <div className="zen-subtitle">Where enough is plenty.</div>
       </header>

       <div className="zen-grid">
          <div data-tour-id="freedom-number"><GoalProgress /></div>
          <RetirementGauge />
          <AutopilotToggle autopilotActive={autopilot} onToggle={() => setAutopilot(true)} />
       </div>
    </div>
  );
}
