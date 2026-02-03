import React, { Suspense } from 'react';
// Imports removed to prevent R3F side-effects

const FitnessSurface3D = ({ data }) => {
  // TEMPORARILY STUBBED - 3D disabled to debug crash
  return (
    <div style={{ 
      width: '100%', 
      height: '400px', 
      background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%)', 
      borderRadius: '12px', 
      overflow: 'hidden', 
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      border: '1px solid #333'
    }}>
      <div style={{ 
        color: '#666', 
        fontFamily: 'monospace', 
        fontSize: '12px',
        textAlign: 'center' 
      }}>
        <div style={{ fontSize: '24px', marginBottom: '8px' }}>🧬</div>
        3D Fitness Surface<br/>
        <span style={{ color: '#444', fontSize: '10px' }}>(Renderer Disabled)</span>
      </div>
    </div>
  );
};

export default FitnessSurface3D;
