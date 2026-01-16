/**
 * LogCenter Component
 * 
 * Unified notification and log center drawer that slides in from the right.
 * Displays live logs and history with tabs.
 * Uses react-window for virtualization to handle large log lists efficiently.
 */

import React, { useState, useMemo } from 'react';
import { List } from 'react-window';
import './LogCenter.css';

export default function LogCenter({ isOpen, onClose, logHistory }) {
  const [activeTab, setActiveTab] = useState('live');

  // Prepare data for virtualization
  const liveLogs = useMemo(() => {
    return logHistory.slice(-50).reverse(); // Show last 50 for live view
  }, [logHistory]);

  const historyLogs = useMemo(() => {
    return [...logHistory].reverse(); // Reverse for chronological order (newest first)
  }, [logHistory]);

  if (!isOpen) return null;

  const currentData = activeTab === 'live' ? liveLogs : historyLogs;
  const listHeight = 600; // Fixed height for the virtualized list

  // Row component for react-window (new API)
  const LogRow = ({ index, style }) => {
    const entry = currentData[index];
    if (!entry) return null;
    
    return (
      <div style={style} className={`log-entry log-entry-${entry.type}`}>
        <span className="log-timestamp">
          {activeTab === 'live' 
            ? new Date(entry.timestamp).toLocaleTimeString()
            : new Date(entry.timestamp).toLocaleString()}
        </span>
        <span className="log-message">{entry.message}</span>
      </div>
    );
  };

  return (
    <div className="log-center-overlay" onClick={onClose}>
      <div className="log-center-drawer" onClick={(e) => e.stopPropagation()}>
        <div className="log-center-header">
          <h2>Log Center</h2>
          <button className="log-center-close" onClick={onClose} aria-label="Close log center">
            ×
          </button>
        </div>
        <div className="log-center-tabs">
          <button
            className={`log-center-tab ${activeTab === 'live' ? 'active' : ''}`}
            onClick={() => setActiveTab('live')}
          >
            Live Logs
          </button>
          <button
            className={`log-center-tab ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            History
          </button>
        </div>
        <div className="log-center-content">
          {currentData.length === 0 ? (
            <p className="log-center-info">
              {activeTab === 'live' 
                ? 'Live logs will appear here as events occur.'
                : 'No log history yet.'}
            </p>
          ) : (
            <List
              height={listHeight}
              rowCount={currentData.length}
              rowHeight={60} // Estimated height per log entry
              rowComponent={LogRow}
              width="100%"
            />
          )}
        </div>
      </div>
    </div>
  );
}

