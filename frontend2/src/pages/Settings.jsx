/**
 * Settings Page
 * 
 * Application configuration and theme builder.
 * Placeholder for now - will include Theme Builder in Phase 4.2.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import '../App.css';

function Settings() {
  const { palette } = useColorPalette();

  return (
    <div className="settings-container">
      <section className="glass card">
        <header>
          <h2>Settings</h2>
          <p>Application configuration and preferences</p>
        </header>
        <div style={{ padding: '2rem', textAlign: 'center', color: palette?.text?.secondary || '#5a4a3a' }}>
          <p> Settings panel coming soon...</p>
          <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
            This will include an interactive Theme Builder for customizing the color palette.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Settings;

