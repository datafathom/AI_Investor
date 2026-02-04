import React from 'react';
import './GlobalStatusBar.css';

const GlobalStatusBar = ({ globalLock, socketConnected, currentUser }) => {
  return (
    <div className="global-status-bar">
      <div className="status-left">
        <span className="status-item">
          {globalLock ? (
            <>
              <span className="status-icon">🔒</span>
              <span className="status-text">Layout Locked</span>
            </>
          ) : (
            <>
              <span className="status-icon">🔓</span>
              <span className="status-text">Layout Unlocked</span>
            </>
          )}
        </span>
        
        <span className="status-divider">|</span>
        
        <span className="status-item">
          <span className={`status-dot ${socketConnected ? 'connected' : 'disconnected'}`}></span>
          <span className="status-text">
            {socketConnected ? 'Connected' : 'Disconnected'}
          </span>
        </span>
      </div>
      
      <div className="status-center">
        {currentUser && (
          <span className="status-item">
            <span className="status-text">Signed in as <strong>{currentUser.username}</strong></span>
          </span>
        )}
      </div>
      
      <div className="status-right">
        <span className="status-item status-hint">
          <kbd>Cmd+K</kbd> for Commands
        </span>
      </div>
    </div>
  );
};

export default GlobalStatusBar;
