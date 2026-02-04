/**
 * Window Registry Component
 * 
 * Displays a list of all open windows with their state and controls.
 * Allows users to manage windows (bring to front, minimize, close, etc.)
 */

import React, { useState } from 'react';
import { useWindowManager } from '../../hooks/useWindowManager';
import './WindowRegistry.css';

export default function WindowRegistry({ onSelectWindow, onClose }) {
  const {
    windows,
    windowStack,
    bringToFront,
    minimizeWindow,
    maximizeWindow,
    restoreWindow,
    toggleLock,
    unregisterWindow,
  } = useWindowManager();

  const [filter, setFilter] = useState('');
  const [sortBy, setSortBy] = useState('zIndex'); // zIndex, title, createdAt

  const filteredWindows = windows
    .filter(w => 
      w.title.toLowerCase().includes(filter.toLowerCase()) ||
      w.id.toLowerCase().includes(filter.toLowerCase())
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'createdAt':
          return new Date(a.createdAt) - new Date(b.createdAt);
        case 'zIndex':
        default:
          return b.zIndex - a.zIndex; // Higher z-index first (top windows)
      }
    });

  const handleBringToFront = (windowId) => {
    bringToFront(windowId);
    if (onSelectWindow) {
      onSelectWindow(windowId);
    }
  };

  const handleMinimize = (windowId) => {
    const window = windows.find(w => w.id === windowId);
    if (window?.state === 'minimized') {
      restoreWindow(windowId);
    } else {
      minimizeWindow(windowId);
    }
  };

  const handleMaximize = (windowId) => {
    const window = windows.find(w => w.id === windowId);
    if (window?.state === 'maximized') {
      restoreWindow(windowId);
    } else {
      maximizeWindow(windowId);
    }
  };

  const handleClose = (windowId) => {
    unregisterWindow(windowId);
  };

  const handleToggleLock = (windowId) => {
    toggleLock(windowId);
  };

  const getStateIcon = (state) => {
    switch (state) {
      case 'minimized':
        return '';
      case 'maximized':
        return '';
      case 'fullscreen':
        return '';
      default:
        return '';
    }
  };

  const getStateLabel = (state) => {
    switch (state) {
      case 'minimized':
        return 'Minimized';
      case 'maximized':
        return 'Maximized';
      case 'fullscreen':
        return 'Fullscreen';
      default:
        return 'Normal';
    }
  };

  return (
    <div className="window-registry">
      <div className="window-registry-header">
        <h3>Window Registry</h3>
        <span className="window-count">{windows.length} window{windows.length !== 1 ? 's' : ''}</span>
      </div>

      <div className="window-registry-controls">
        <input
          type="text"
          placeholder="Filter windows..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="window-registry-filter"
        />
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="window-registry-sort"
        >
          <option value="zIndex">Z-Order</option>
          <option value="title">Title</option>
          <option value="createdAt">Created</option>
        </select>
      </div>

      <div className="window-registry-list">
        {filteredWindows.length === 0 ? (
          <div className="window-registry-empty">
            {filter ? 'No windows match your filter' : 'No windows open'}
          </div>
        ) : (
          filteredWindows.map((window) => {
            const isTop = windowStack[windowStack.length - 1] === window.id;
            return (
              <div
                key={window.id}
                className={`window-registry-item ${isTop ? 'window-registry-item-top' : ''} ${window.isLocked ? 'window-registry-item-locked' : ''}`}
                onClick={() => handleBringToFront(window.id)}
              >
                <div className="window-registry-item-header">
                  <div className="window-registry-item-info">
                    <span className="window-registry-item-icon">
                      {getStateIcon(window.state)}
                    </span>
                    <div className="window-registry-item-details">
                      <div className="window-registry-item-title">{window.title}</div>
                      <div className="window-registry-item-meta">
                        {getStateLabel(window.state)}
                        {window.isLocked && '  Locked'}
                        {window.isGrouped && `  Group: ${window.groupId}`}
                      </div>
                    </div>
                  </div>
                  {isTop && <span className="window-registry-item-badge">Top</span>}
                </div>

                <div className="window-registry-item-actions">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleMinimize(window.id);
                    }}
                    title={window.state === 'minimized' ? 'Restore' : 'Minimize'}
                    className="window-registry-action-btn"
                  >
                    {window.state === 'minimized' ? '' : ''}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleMaximize(window.id);
                    }}
                    title={window.state === 'maximized' ? 'Restore' : 'Maximize'}
                    className="window-registry-action-btn"
                  >
                    {window.state === 'maximized' ? '' : ''}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleToggleLock(window.id);
                    }}
                    title={window.isLocked ? 'Unlock' : 'Lock'}
                    className="window-registry-action-btn"
                  >
                    {window.isLocked ? '' : ''}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleClose(window.id);
                    }}
                    title="Close"
                    className="window-registry-action-btn window-registry-action-btn-danger"
                  >
                    
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

