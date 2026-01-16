/**
 * Sync Service
 * 
 * Handles data synchronization between client and server.
 * Supports offline queue and conflict resolution.
 */

class SyncService {
  constructor() {
    this.queue = [];
    this.isOnline = navigator.onLine;
    this.syncing = false;
    this.listeners = new Set();

    // Listen to online/offline events
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.emit('online');
      this.processQueue();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.emit('offline');
    });
  }

  /**
   * Queue an action for sync
   */
  queueAction(action) {
    const queuedAction = {
      id: `action-${Date.now()}-${Math.random()}`,
      ...action,
      timestamp: new Date(),
      retries: 0,
    };

    this.queue.push(queuedAction);
    this.emit('action:queued', queuedAction);

    // Try to process immediately if online
    if (this.isOnline) {
      this.processQueue();
    }

    return queuedAction.id;
  }

  /**
   * Process queued actions
   */
  async processQueue() {
    if (this.syncing || !this.isOnline || this.queue.length === 0) {
      return;
    }

    this.syncing = true;
    this.emit('sync:started');

    const actionsToProcess = [...this.queue];
    const results = [];

    for (const action of actionsToProcess) {
      try {
        const result = await this._executeAction(action);
        results.push({ action, result, success: true });
        
        // Remove from queue
        this.queue = this.queue.filter(a => a.id !== action.id);
      } catch (error) {
        action.retries++;
        
        if (action.retries >= 3) {
          // Max retries reached, remove from queue
          this.queue = this.queue.filter(a => a.id !== action.id);
          results.push({ action, error, success: false });
        } else {
          // Keep in queue for retry
          results.push({ action, error, success: false });
        }
      }
    }

    this.syncing = false;
    this.emit('sync:completed', results);
  }

  /**
   * Execute a single action
   */
  async _executeAction(action) {
    const { type, endpoint, method = 'POST', data } = action;

    const response = await fetch(endpoint, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) {
      throw new Error(`Sync failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get queue status
   */
  getQueueStatus() {
    return {
      length: this.queue.length,
      isOnline: this.isOnline,
      isSyncing: this.syncing,
    };
  }

  /**
   * Clear queue
   */
  clearQueue() {
    this.queue = [];
    this.emit('queue:cleared');
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
const syncService = new SyncService();

export default syncService;

