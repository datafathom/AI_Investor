import React from 'react';
import { Power } from 'lucide-react';
import './ZenMode.css';

export default function AutopilotToggle({ autopilotActive, onToggle }) {
  return (
    <div className="zen-widget">
      <div className="widget-wrapper">
         <h3>System Autopilot</h3>
         
         <button 
            onClick={onToggle}
            style={{
                width: '80px',
                height: '80px',
                borderRadius: '50%',
                border: 'none',
                background: autopilotActive ? 'var(--neon-cyan)' : 'rgba(255,255,255,0.1)',
                color: autopilotActive ? '#000' : '#fff',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: autopilotActive ? '0 0 30px rgba(0,242,254,0.4)' : 'none',
                transition: 'all 0.3s ease'
            }}
         >
            <Power size={32} />
         </button>

         <div style={{textAlign: 'center', opacity: 0.8, maxWidth: '200px'}}>
             {autopilotActive 
               ? "Master Override Active. High-frequency trading disabled. Passive income optimization only."
               : "Manual Control Enabled. Market exposure is active."
             }
         </div>
      </div>
    </div>
  );
}
