/**
 * Telemetry Page
 * 
 * Server metrics and real-time data visualization.
 * Placeholder for now - will be upgraded with Recharts in Phase 2.2.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import '../App.css';

function Telemetry() {
  const { palette } = useColorPalette();

  return (
    <div className="telemetry-container">
      <section className="glass card">
        <header>
          <h2>Server Telemetry</h2>
          <p>Real-time server metrics and performance data</p>
        </header>
        <div style={{ padding: '2rem', textAlign: 'center', color: palette?.text?.secondary || '#5a4a3a' }}>
          <p>📈 Telemetry visualization coming soon...</p>
          <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
            This will include real-time charts using Recharts with Socket.io heartbeat effects.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Telemetry;

