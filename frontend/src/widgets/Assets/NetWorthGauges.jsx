import React, { useEffect, useState } from 'react';
import { useWealthStore } from '../../stores/wealthStore';
import { TrendingUp, PieChart } from 'lucide-react';
import './NetWorthGauges.css';

export default function NetWorthGauges() {
  const { getTotalWealth, getIlliquidTotal, assets } = useWealthStore();
  const [totalWealth, setTotalWealth] = useState(0);
  const [illiquidTotal, setIlliquidTotal] = useState(0);
  
  // Simulated liquid assets for demo (since we don't have a live portfolio connection simulate it)
  const liquidTotal = 1250000; // Mock value for "Stocks/Cash"
  
  useEffect(() => {
    setTotalWealth(getTotalWealth() + liquidTotal);
    setIlliquidTotal(getIlliquidTotal());
  }, [assets, getTotalWealth, getIlliquidTotal]);

  const liquidPercent = totalWealth > 0 ? ((liquidTotal / totalWealth) * 100) : 0;
  const illiquidPercent = totalWealth > 0 ? ((illiquidTotal / totalWealth) * 100) : 0;

  // Calculate SVG stroke dashes for rings
  const radius = 80;
  const circumference = 2 * Math.PI * radius;
  
  const liquidDash = (liquidPercent / 100) * circumference;
  const illiquidDash = (illiquidPercent / 100) * circumference;

  return (
    <div className="net-worth-gauges widget-container glass-panel">
      <div className="widget-header">
        <h3>Unified Net Worth</h3>
        <span className="badge-live">LIVE</span>
      </div>

      <div className="gauge-container">
        <svg width="240" height="240" className="circular-gauge">
           {/* Background Ring */}
           <circle cx="120" cy="120" r={radius} stroke="var(--bg-elevated)" strokeWidth="20" fill="none" />
           
           {/* Illiquid Ring (Outer) */}
           <circle 
              cx="120" cy="120" r={radius} 
              stroke="var(--neon-purple)" 
              strokeWidth="20" 
              fill="none"
              strokeDasharray={`${illiquidDash} ${circumference}`}
              strokeDashoffset={circumference * 0.25} // Rotate to start at top
              strokeLinecap="round"
              className="gauge-segment"
           />
           
           {/* Liquid Ring (Inner - Simulated) */}
           <circle 
              cx="120" cy="120" r={radius - 25} 
              stroke="var(--neon-cyan)" 
              strokeWidth="15" 
              fill="none"
              strokeDasharray={`${(liquidPercent / 100) * (2 * Math.PI * (radius - 25))} ${(2 * Math.PI * (radius - 25))}`}
              strokeDashoffset={(2 * Math.PI * (radius - 25)) * 0.25}
              strokeLinecap="round"
              className="gauge-segment delay-1"
           />
        </svg>

        <div className="center-value">
           <span className="label">Total Net Worth</span>
           <span className="value">${totalWealth.toLocaleString(undefined, { maximumFractionDigits: 0 })}</span>
           <span className="trend positive">
             <TrendingUp size={14} /> +{(2.4).toFixed(1)}%
           </span>
        </div>
      </div>

      <div className="legend-grid">
         <div className="legend-item">
            <div className="dot" style={{ background: 'var(--neon-cyan)' }} />
            <div className="info">
               <span className="type">Liquid Assets</span>
               <span className="amt">${liquidTotal.toLocaleString()}</span>
            </div>
         </div>
         <div className="legend-item">
            <div className="dot" style={{ background: 'var(--neon-purple)' }} />
            <div className="info">
               <span className="type">Illiquid / Real Estate</span>
               <span className="amt">${illiquidTotal.toLocaleString()}</span>
            </div>
         </div>
      </div>
    </div>
  );
}
