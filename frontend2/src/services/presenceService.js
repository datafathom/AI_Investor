/**
 * Presence Service
 * 
 * Tracks user presence and activity.
 * Shows who's online and what they're viewing.
 */

import io from 'socket.io-client';

class PresenceService {
  constructor() {
    this.socket = null;
    this.users = new Map(); // userId -> userData
    this.currentUser = null;
    this.listeners = new Set();
    this.activityInterval = null;
  }

  /**
   * Initialize presence service
   */
  initialize(userId, username) {
    if (this.socket) {
      this.disconnect();
    }

    this.currentUser = { id: userId, username };
    // Use relative path to leverage Vite proxy correctly in all environments
    this.socket = io({
      path: '/socket.io',
      transports: ['websocket', 'polling'],
      reconnectionAttempts: 5
    });

    // Register user
    this.socket.emit('presence:register', {
      userId,
      username,
      timestamp: new Date().toISOString(),
    });

    // Listen for presence updates
    this.socket.on('presence:update', (data) => {
      this.users.set(data.userId, data);
      this.emit('presence:updated', data);
    });

    this.socket.on('presence:user-joined', (data) => {
      this.users.set(data.userId, data);
      this.emit('presence:user-joined', data);
    });

    this.socket.on('presence:user-left', (data) => {
      this.users.delete(data.userId);
      this.emit('presence:user-left', data);
    });

    this.socket.on('presence:list', (users) => {
      this.users.clear();
      users.forEach(user => {
        this.users.set(user.userId, user);
      });
      this.emit('presence:list-updated', Array.from(this.users.values()));
    });

    // Risk & Trade Events (Phase 48)
    this.socket.on('risk:alert', (data) => {
      this.emit('risk:alert', data);
    });

    this.socket.on('trade:fill', (data) => {
      this.emit('trade:fill', data);
    });

    this.socket.on('system:log', (data) => {
      this.emit('system:log', data);
    });

    // Send activity updates periodically
    this.activityInterval = setInterval(() => {
      this.updateActivity();
    }, 30000); // Every 30 seconds
  }

  /**
   * Update user activity
   */
  updateActivity(page = null, action = null) {
    if (!this.socket || !this.currentUser) return;

    this.socket.emit('presence:activity', {
      userId: this.currentUser.id,
      page,
      action,
      timestamp: new Date().toISOString(),
    });
  }

  /**
   * Get all online users
   */
  getOnlineUsers() {
    return Array.from(this.users.values());
  }

  /**
   * Get user by ID
   */
  getUser(userId) {
    return this.users.get(userId) || null;
  }

  /**
   * Disconnect
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }

    if (this.activityInterval) {
      clearInterval(this.activityInterval);
      this.activityInterval = null;
    }

    this.users.clear();
    this.currentUser = null;
  }

  /**
   * Event listener management
   */
  on(event, callback) {
    this.listeners.add({ event, callback });
  }

  off(event, callback) {
    this.listeners.forEach(listener => {
      if (listener.event === event && listener.callback === callback) {
        this.listeners.delete(listener);
      }
    });
  }

  emit(event, ...args) {
    this.listeners.forEach(listener => {
      if (listener.event === event) {
        listener.callback(...args);
      }
    });
  }
}

// Singleton instance
const presenceService = new PresenceService();

export default presenceService;

