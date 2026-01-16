/**
 * Window Group Component
 * 
 * Tabbed interface for grouping related windows together.
 * Similar to browser tabs, but for application windows.
 */

import React, { useState } from 'react';
import { useWindowManager } from '../../hooks/useWindowManager';
import './WindowGroup.css';

export default function WindowGroup({ groupId, onClose }) {
  const { getGroupWindows, bringToFront, unregisterWindow } = useWindowManager();
  const [activeTab, setActiveTab] = useState(null);

  const windows = getGroupWindows(groupId);

  // Set first window as active if none selected
  React.useEffect(() => {
    if (windows.length > 0 && !activeTab) {
      setActiveTab(windows[0].id);
    }
  }, [windows, activeTab]);

  if (windows.length === 0) {
    return null;
  }

  const handleTabClick = (windowId) => {
    setActiveTab(windowId);
    bringToFront(windowId);
  };

  const handleTabClose = (e, windowId) => {
    e.stopPropagation();
    unregisterWindow(windowId);
    
    // If closing active tab, switch to another
    if (windowId === activeTab) {
      const remaining = windows.filter(w => w.id !== windowId);
      if (remaining.length > 0) {
        setActiveTab(remaining[0].id);
        bringToFront(remaining[0].id);
      } else if (onClose) {
        onClose();
      }
    }
  };

  const activeWindow = windows.find(w => w.id === activeTab);

  return (
    <div className="window-group">
      <div className="window-group-tabs">
        {windows.map((window) => (
          <div
            key={window.id}
            className={`window-group-tab ${activeTab === window.id ? 'window-group-tab-active' : ''}`}
            onClick={() => handleTabClick(window.id)}
          >
            <span className="window-group-tab-icon">
              {window.state === 'minimized' ? '📦' : 
               window.state === 'maximized' ? '⬜' : '📄'}
            </span>
            <span className="window-group-tab-title">{window.title}</span>
            <button
              className="window-group-tab-close"
              onClick={(e) => handleTabClose(e, window.id)}
              title="Close tab"
            >
              ×
            </button>
          </div>
        ))}
      </div>
      {activeWindow && (
        <div className="window-group-content">
          {/* The actual window content would be rendered here */}
          <div className="window-group-content-placeholder">
            Window: {activeWindow.title}
          </div>
        </div>
      )}
    </div>
  );
}

