/**
 * Notification Center Component
 * 
 * Centralized notification system with history and preferences.
 */

import React, { useState, useEffect } from 'react';
import { useStore } from '../../store/store';
import './NotificationCenter.css';

export default function NotificationCenter({ onClose }) {
  const { notifications, removeNotification, clearNotifications } = useStore();
  const [filter, setFilter] = useState('all'); // 'all', 'unread', 'read'

  const filteredNotifications = notifications.filter(notif => {
    if (filter === 'unread') return !notif.read;
    if (filter === 'read') return notif.read;
    return true;
  });

  const unreadCount = notifications.filter(n => !n.read).length;

  const handleMarkRead = (id) => {
    // Update notification in store
    const updated = notifications.map(n =>
      n.id === id ? { ...n, read: true } : n
    );
    useStore.setState({ notifications: updated });
  };

  const handleMarkAllRead = () => {
    const updated = notifications.map(n => ({ ...n, read: true }));
    useStore.setState({ notifications: updated });
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success': return '✓';
      case 'error': return '✕';
      case 'warning': return '⚠';
      case 'info': return 'ℹ';
      default: return '•';
    }
  };

  return (
    <div className="notification-center">
      <div className="notification-center-header">
        <h2>Notifications</h2>
        {unreadCount > 0 && (
          <span className="notification-center-badge">{unreadCount}</span>
        )}
        <button onClick={onClose} className="notification-center-close">×</button>
      </div>

      <div className="notification-center-filters">
        <button
          onClick={() => setFilter('all')}
          className={`notification-center-filter ${filter === 'all' ? 'active' : ''}`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('unread')}
          className={`notification-center-filter ${filter === 'unread' ? 'active' : ''}`}
        >
          Unread {unreadCount > 0 && `(${unreadCount})`}
        </button>
        <button
          onClick={() => setFilter('read')}
          className={`notification-center-filter ${filter === 'read' ? 'active' : ''}`}
        >
          Read
        </button>
      </div>

      <div className="notification-center-actions">
        {unreadCount > 0 && (
          <button
            onClick={handleMarkAllRead}
            className="notification-center-action-btn"
          >
            Mark all as read
          </button>
        )}
        {notifications.length > 0 && (
          <button
            onClick={clearNotifications}
            className="notification-center-action-btn notification-center-action-btn-danger"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="notification-center-list">
        {filteredNotifications.length === 0 ? (
          <div className="notification-center-empty">
            {filter === 'all' ? 'No notifications' : `No ${filter} notifications`}
          </div>
        ) : (
          filteredNotifications.map(notification => (
            <div
              key={notification.id}
              className={`notification-center-item ${notification.read ? 'read' : 'unread'} notification-center-item-${notification.type}`}
              onClick={() => handleMarkRead(notification.id)}
            >
              <div className="notification-center-item-icon">
                {getNotificationIcon(notification.type)}
              </div>
              <div className="notification-center-item-content">
                <div className="notification-center-item-title">
                  {notification.title || notification.message}
                </div>
                {notification.message && notification.title && (
                  <div className="notification-center-item-message">
                    {notification.message}
                  </div>
                )}
                <div className="notification-center-item-time">
                  {notification.timestamp
                    ? new Date(notification.timestamp).toLocaleTimeString()
                    : 'Just now'}
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeNotification(notification.id);
                }}
                className="notification-center-item-close"
                title="Dismiss"
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

