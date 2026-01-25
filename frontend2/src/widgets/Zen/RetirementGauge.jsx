import React, { useState } from 'react';
import { ShieldCheck, AlertTriangle } from 'lucide-react';
import './ZenMode.css';

export default function RetirementGauge() {
  const [frugalMode, setFrugalMode] = useState(false);
  
  // Mock calculations
  const successProbability = frugalMode ? 99.9 : 94.2;
  const yearsCovered = frugalMode ? 'Forever' : '42 years';
  
  return (
    <div className="zen-widget">
      <div className="widget-wrapper">
        <div style={{display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center'}}>
            <h3>Survival Probability</h3>
            <label style={{display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem'}}>
                <span>Lux</span>
                <input 
                    type="checkbox" 
                    className="zen-toggle" 
                    checked={frugalMode}
                    onChange={() => setFrugalMode(!frugalMode)}
                />
                <span>Frugal</span>
            </label>
        </div>

        <div style={{position: 'relative', width: '160px', height: '160px'}}>
             <svg width="160" height="160" style={{transform: 'rotate(-90deg)'}}>
                 <circle cx="80" cy="80" r="70" stroke="rgba(255,255,255,0.1)" strokeWidth="8" fill="none" />
                 <circle 
                    cx="80" cy="80" r="70" 
                    stroke={successProbability > 95 ? "#4facfe" : "#ffbd59"} 
                    strokeWidth="8" 
                    fill="none" 
                    strokeDasharray={`${(successProbability / 100) * 440} 440`}
                    strokeLinecap="round"
                    style={{transition: 'all 1s ease'}}
                 />
             </svg>
             <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
                 <span style={{fontSize: '2rem', fontWeight: 'bold'}}>{successProbability}%</span>
                 <span style={{fontSize: '0.8rem', opacity: 0.7}}>Success</span>
             </div>
        </div>

        <div style={{textAlign: 'center', marginTop: '0.5rem'}}>
            <div style={{color: '#4facfe', fontWeight: 'bold', fontSize: '1.1rem'}}>{yearsCovered}</div>
            <div style={{fontSize: '0.8rem', opacity: 0.7}}>Expenses Covered</div>
        </div>
      </div>
    </div>
  );
}
