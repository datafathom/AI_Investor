/**
 * Window Manager Widget
 * 
 * Main widget component that demonstrates the window management system.
 * Can be added to the dashboard to manage windows.
 */

import React, { useState } from 'react';
import { useWindowManager } from '../../hooks/useWindowManager';
import WindowRegistry from './WindowRegistry';
import './WindowManagerWidget.css';

export default function WindowManagerWidget() {
  const {
    windows,
    registerWindow,
    saveLayout,
    loadLayout,
    getSavedLayouts,
    deleteLayout,
  } = useWindowManager();

  const [showRegistry, setShowRegistry] = useState(false);
  const [layoutName, setLayoutName] = useState('');
  const [savedLayouts, setSavedLayouts] = useState(() => getSavedLayouts());

  const handleCreateTestWindow = () => {
    const windowId = `test-window-${Date.now()}`;
    registerWindow({
      id: windowId,
      title: `Test Window ${windows.length + 1}`,
      component: 'TestComponent',
      position: { x: 100 + windows.length * 30, y: 100 + windows.length * 30 },
      size: { width: 400, height: 300 },
      state: 'normal',
      metadata: { type: 'test' },
    });
  };

  const handleSaveLayout = () => {
    if (!layoutName.trim()) {
      alert('Please enter a layout name');
      return;
    }
    saveLayout(layoutName);
    setSavedLayouts(getSavedLayouts());
    setLayoutName('');
    alert(`Layout "${layoutName}" saved!`);
  };

  const handleLoadLayout = (name) => {
    loadLayout(name);
    alert(`Layout "${name}" loaded!`);
  };

  const handleDeleteLayout = (name) => {
    if (confirm(`Delete layout "${name}"?`)) {
      deleteLayout(name);
      setSavedLayouts(getSavedLayouts());
    }
  };

  return (
    <div className="window-manager-widget">
      <div className="window-manager-widget-header">
        <h3>Window Manager</h3>
        <div className="window-manager-stats">
          <span>{windows.length} window{windows.length !== 1 ? 's' : ''}</span>
        </div>
      </div>

      <div className="window-manager-widget-content">
        <div className="window-manager-actions">
          <button
            onClick={handleCreateTestWindow}
            className="window-manager-btn window-manager-btn-primary"
          >
            + Create Test Window
          </button>
          <button
            onClick={() => setShowRegistry(!showRegistry)}
            className="window-manager-btn"
          >
            {showRegistry ? 'Hide' : 'Show'} Registry
          </button>
        </div>

        {showRegistry && (
          <div className="window-manager-registry-container">
            <WindowRegistry />
          </div>
        )}

        <div className="window-manager-layouts">
          <h4>Layout Management</h4>
          <div className="window-manager-save-layout">
            <input
              type="text"
              placeholder="Layout name..."
              value={layoutName}
              onChange={(e) => setLayoutName(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSaveLayout();
                }
              }}
              className="window-manager-input"
            />
            <button
              onClick={handleSaveLayout}
              className="window-manager-btn window-manager-btn-primary"
            >
              Save Layout
            </button>
          </div>

          <div className="window-manager-saved-layouts">
            <h5>Saved Layouts</h5>
            {Object.keys(savedLayouts).length === 0 ? (
              <p className="window-manager-empty">No saved layouts</p>
            ) : (
              <div className="window-manager-layout-list">
                {Object.entries(savedLayouts).map(([name, layout]) => (
                  <div key={name} className="window-manager-layout-item">
                    <span className="window-manager-layout-name">{name}</span>
                    <span className="window-manager-layout-meta">
                      {layout.windows?.length || 0} windows
                    </span>
                    <div className="window-manager-layout-actions">
                      <button
                        onClick={() => handleLoadLayout(name)}
                        className="window-manager-btn-small"
                        title="Load layout"
                      >
                        
                      </button>
                      <button
                        onClick={() => handleDeleteLayout(name)}
                        className="window-manager-btn-small window-manager-btn-danger"
                        title="Delete layout"
                      >
                        
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

