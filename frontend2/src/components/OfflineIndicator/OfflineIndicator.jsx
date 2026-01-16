/**
 * Offline Indicator Component
 * 
 * Shows online/offline status and sync queue information.
 */

import React, { useState, useEffect } from 'react';
import syncService from '../../services/syncService';
import './OfflineIndicator.css';

export default function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [queueStatus, setQueueStatus] = useState(() => syncService.getQueueStatus());

  useEffect(() => {
    const updateStatus = () => {
      setIsOnline(navigator.onLine);
      setQueueStatus(syncService.getQueueStatus());
    };

    syncService.on('online', updateStatus);
    syncService.on('offline', updateStatus);
    syncService.on('action:queued', updateStatus);
    syncService.on('sync:completed', updateStatus);

    return () => {
      syncService.off('online', updateStatus);
      syncService.off('offline', updateStatus);
      syncService.off('action:queued', updateStatus);
      syncService.off('sync:completed', updateStatus);
    };
  }, []);

  if (isOnline && queueStatus.length === 0) {
    return null; // Don't show when online and no queue
  }

  return (
    <div className={`offline-indicator ${isOnline ? 'online' : 'offline'}`}>
      <div className="offline-indicator-content">
        <span className="offline-indicator-icon">
          {isOnline ? '✓' : '⚠'}
        </span>
        <span className="offline-indicator-text">
          {isOnline 
            ? queueStatus.length > 0 
              ? `Syncing ${queueStatus.length} action${queueStatus.length !== 1 ? 's' : ''}...`
              : 'Online'
            : 'Offline'}
        </span>
        {queueStatus.length > 0 && (
          <span className="offline-indicator-queue">
            {queueStatus.length} queued
          </span>
        )}
      </div>
    </div>
  );
}

