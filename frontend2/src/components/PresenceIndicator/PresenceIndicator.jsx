/**
 * Presence Indicator Component
 * 
 * Shows online users and their current activity.
 */

import React, { useState, useEffect } from 'react';
import presenceService from '../../services/presenceService';
import './PresenceIndicator.css';

export default function PresenceIndicator() {
  const [users, setUsers] = useState([]);
  const [showList, setShowList] = useState(false);

  useEffect(() => {
    const updateUsers = () => {
      setUsers(presenceService.getOnlineUsers());
    };

    presenceService.on('presence:list-updated', updateUsers);
    presenceService.on('presence:user-joined', updateUsers);
    presenceService.on('presence:user-left', updateUsers);

    updateUsers();

    return () => {
      presenceService.off('presence:list-updated', updateUsers);
      presenceService.off('presence:user-joined', updateUsers);
      presenceService.off('presence:user-left', updateUsers);
    };
  }, []);

  if (users.length === 0) {
    return null;
  }

  return (
    <div className="presence-indicator">
      <button
        onClick={() => setShowList(!showList)}
        className="presence-indicator-button"
        title={`${users.length} user${users.length !== 1 ? 's' : ''} online`}
      >
        <span className="presence-indicator-icon">👥</span>
        <span className="presence-indicator-count">{users.length}</span>
      </button>

      {showList && (
        <div className="presence-indicator-list">
          <div className="presence-indicator-list-header">
            <h4>Online Users</h4>
            <button
              onClick={() => setShowList(false)}
              className="presence-indicator-close"
            >
              ×
            </button>
          </div>
          <div className="presence-indicator-list-content">
            {users.map(user => (
              <div key={user.userId} className="presence-indicator-user">
                <span className="presence-indicator-user-status" />
                <span className="presence-indicator-user-name">
                  {user.username || `User ${user.userId}`}
                </span>
                {user.page && (
                  <span className="presence-indicator-user-activity">
                    {user.page}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

