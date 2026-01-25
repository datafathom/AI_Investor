import React, { useState, useEffect } from 'react';
import { useWealthStore } from '../../stores/wealthStore';
import './ZenMode.css';

export default function GoalProgress() {
  const { assets, getTotalWealth } = useWealthStore();
  const [currentWealth, setCurrentWealth] = useState(0);
  const [freedomNumber, setFreedomNumber] = useState(5000000); 

  useEffect(() => {
    setCurrentWealth(getTotalWealth());
  }, [assets, getTotalWealth]);

  const progress = Math.min((currentWealth / freedomNumber) * 100, 100);

  return (
    <div className="zen-widget">
      <div className="widget-wrapper">
        <h3>The Freedom Metric</h3>
        
        <div className="stat-display">
            <span className="current">${currentWealth.toLocaleString()}</span>
            <span className="separator"> / </span>
            <span className="target">${freedomNumber.toLocaleString()}</span>
        </div>

        <div className="progress-container">
            <div className="progress-fill" style={{ width: `${progress}%` }}>
                {progress >= 100 && <div className="progress-glow"></div>}
            </div>
        </div>

        <div className="caption">
            {progress >= 100 
                ? "You have reached 'Enough'. Everything else is extra."
                : `You are ${progress.toFixed(1)}% of the way to autonomy.`
            }
        </div>
      </div>
    </div>
  );
}
