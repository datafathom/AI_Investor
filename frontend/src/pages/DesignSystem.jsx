/**
 * Design System Playground Page
 * 
 * Interactive component playground for developers.
 * Placeholder for now - will be implemented in .1.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import '../App.css';

function DesignSystem() {
  const { palette } = useColorPalette();

  return (
    <div className="design-system-container">
      <section className="glass card">
        <header>
          <h2>Design System Playground</h2>
          <p>Interactive component library with live code editing</p>
        </header>
        <div style={{ padding: '2rem', textAlign: 'center', color: palette?.text?.secondary || '#5a4a3a' }}>
          <p> Design system playground coming soon...</p>
          <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
            This will include live component previews with editable code using react-live.
          </p>
        </div>
      </section>
    </div>
  );
}

export default DesignSystem;

