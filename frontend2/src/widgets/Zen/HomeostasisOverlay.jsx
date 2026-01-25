import React from 'react';
import { Wind } from 'lucide-react';
import './ZenMode.css';

export default function HomeostasisOverlay({ active, onUnlock }) {
  if (!active) return null;

  return (
    <div className="homeostasis-overlay">
      <div className="breathe-circle"></div>
      
      <h2 style={{marginTop: '2rem', fontSize: '2rem', fontWeight: 200, letterSpacing: '2px'}}>HOMEOSTASIS</h2>
      <p style={{opacity: 0.7, maxWidth: '400px', textAlign: 'center', lineHeight: '1.6'}}>
        The system is preserving capital. High-frequency noise is filtered. Only long-term signals are processed.
      </p>

      <div style={{marginTop: '3rem', display: 'flex', gap: '1rem', alignItems: 'center'}}>
         <Wind className="animate-pulse" size={24} color="#4facfe" />
         <span style={{fontFamily: 'monospace', color: '#4facfe'}}>SYSTEM_STATUS: ZEN</span>
      </div>

      <button 
        onClick={onUnlock}
        style={{
            marginTop: '4rem',
            background: 'transparent',
            border: '1px solid rgba(255,255,255,0.3)',
            color: '#fff',
            padding: '0.8rem 2rem',
            borderRadius: '30px',
            cursor: 'pointer',
            fontSize: '0.9rem',
            transition: 'background 0.2s'
        }}
        onMouseOver={(e) => e.target.style.background = 'rgba(255,255,255,0.1)'}
        onMouseOut={(e) => e.target.style.background = 'transparent'}
      >
        Disengage Autopilot
      </button>
    </div>
  );
}
