/**
 * Window Manager Service
 * 
 * Centralized service for managing window state, z-index, stacking, and persistence.
 * Provides a registry of all open windows with their properties.
 */

class WindowManager {
  constructor() {
    this.windows = new Map(); // windowId -> windowData
    this.windowStack = []; // Array of windowIds in z-order (last = top)
    this.listeners = new Set(); // Event listeners
    this.nextZIndex = 1000; // Starting z-index
    this.maxZIndex = 10000; // Maximum z-index
    this.snapZones = {
      left: { x: 0, width: '50%' },
      right: { x: '50%', width: '50%' },
      top: { y: 0, height: '50%' },
      bottom: { y: '50%', height: '50%' },
      topLeft: { x: 0, y: 0, width: '50%', height: '50%' },
      topRight: { x: '50%', y: 0, width: '50%', height: '50%' },
      bottomLeft: { x: 0, y: '50%', width: '50%', height: '50%' },
      bottomRight: { x: '50%', y: '50%', width: '50%', height: '50%' },
    };
  }

  /**
   * Register a new window
   */
  registerWindow(windowData) {
    const {
      id,
      title,
      component,
      position = { x: 100, y: 100 },
      size = { width: 400, height: 300 },
      state = 'normal', // normal, minimized, maximized, fullscreen
      isLocked = false,
      isGrouped = false,
      groupId = null,
      metadata = {},
    } = windowData;

    if (!id) {
      throw new Error('Window ID is required');
    }

    if (this.windows.has(id)) {
      console.warn(`Window ${id} already exists, updating instead`);
      return this.updateWindow(id, windowData);
    }

    const window = {
      id,
      title,
      component,
      position,
      size,
      state,
      isLocked,
      isGrouped,
      groupId,
      metadata,
      zIndex: this.getNextZIndex(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.windows.set(id, window);
    this.windowStack.push(id);
    this.emit('window:registered', window);
    return window;
  }

  /**
   * Unregister a window
   */
  unregisterWindow(windowId) {
    if (!this.windows.has(windowId)) {
      return false;
    }

    const window = this.windows.get(windowId);
    this.windows.delete(windowId);
    this.windowStack = this.windowStack.filter(id => id !== windowId);
    this.emit('window:unregistered', window);
    return true;
  }

  /**
   * Get window by ID
   */
  getWindow(windowId) {
    return this.windows.get(windowId) || null;
  }

  /**
   * Get all windows
   */
  getAllWindows() {
    return Array.from(this.windows.values());
  }

  /**
   * Get windows in z-order (top to bottom)
   */
  getWindowsInOrder() {
    return this.windowStack
      .slice()
      .reverse()
      .map(id => this.windows.get(id))
      .filter(Boolean);
  }

  /**
   * Update window properties
   */
  updateWindow(windowId, updates) {
    const window = this.windows.get(windowId);
    if (!window) {
      throw new Error(`Window ${windowId} not found`);
    }

    const updatedWindow = {
      ...window,
      ...updates,
      updatedAt: new Date(),
    };

    this.windows.set(windowId, updatedWindow);
    this.emit('window:updated', updatedWindow, updates);
    return updatedWindow;
  }

  /**
   * Bring window to front
   */
  bringToFront(windowId) {
    if (!this.windows.has(windowId)) {
      return false;
    }

    // Remove from stack
    this.windowStack = this.windowStack.filter(id => id !== windowId);
    // Add to top
    this.windowStack.push(windowId);

    // Update z-index
    const newZIndex = this.getNextZIndex();
    this.updateWindow(windowId, { zIndex: newZIndex });

    this.emit('window:broughtToFront', this.windows.get(windowId));
    return true;
  }

  /**
   * Send window to back
   */
  sendToBack(windowId) {
    if (!this.windows.has(windowId)) {
      return false;
    }

    // Remove from stack
    this.windowStack = this.windowStack.filter(id => id !== windowId);
    // Add to bottom
    this.windowStack.unshift(windowId);

    // Update z-index
    const newZIndex = this.getNextZIndex();
    this.updateWindow(windowId, { zIndex: newZIndex });

    this.emit('window:sentToBack', this.windows.get(windowId));
    return true;
  }

  /**
   * Minimize window
   */
  minimizeWindow(windowId) {
    const window = this.windows.get(windowId);
    if (!window) return false;

    // Store original size before minimizing
    if (window.state !== 'minimized') {
      window._originalSize = { ...window.size };
      window._originalPosition = { ...window.position };
    }

    this.updateWindow(windowId, {
      state: 'minimized',
      size: { width: window.size.width, height: 28 }, // Header height
    });

    this.emit('window:minimized', this.windows.get(windowId));
    return true;
  }

  /**
   * Maximize window
   */
  maximizeWindow(windowId) {
    const window = this.windows.get(windowId);
    if (!window) return false;

    // Store original size/position before maximizing
    if (window.state !== 'maximized' && window.state !== 'fullscreen') {
      window._originalSize = { ...window.size };
      window._originalPosition = { ...window.position };
    }

    this.updateWindow(windowId, {
      state: 'maximized',
      position: { x: 0, y: 30 }, // Account for menu bar
      size: {
        width: window.innerWidth || window.screen?.width || 1920,
        height: (window.innerHeight || window.screen?.height || 1080) - 30,
      },
    });

    this.emit('window:maximized', this.windows.get(windowId));
    return true;
  }

  /**
   * Restore window to normal state
   */
  restoreWindow(windowId) {
    const window = this.windows.get(windowId);
    if (!window) return false;

    const originalSize = window._originalSize || { width: 400, height: 300 };
    const originalPosition = window._originalPosition || { x: 100, y: 100 };

    this.updateWindow(windowId, {
      state: 'normal',
      size: originalSize,
      position: originalPosition,
    });

    // Clean up stored values
    delete window._originalSize;
    delete window._originalPosition;

    this.emit('window:restored', this.windows.get(windowId));
    return true;
  }

  /**
   * Toggle window lock
   */
  toggleLock(windowId) {
    const window = this.windows.get(windowId);
    if (!window) return false;

    const newLockState = !window.isLocked;
    this.updateWindow(windowId, { isLocked: newLockState });
    this.emit('window:lockToggled', this.windows.get(windowId), newLockState);
    return newLockState;
  }

  /**
   * Snap window to zone
   */
  snapToZone(windowId, zone) {
    const window = this.windows.get(windowId);
    if (!window) return false;

    const snapZone = this.snapZones[zone];
    if (!snapZone) {
      console.warn(`Unknown snap zone: ${zone}`);
      return false;
    }

    const updates = {
      position: {},
      size: {},
    };

    if (snapZone.x !== undefined) updates.position.x = snapZone.x;
    if (snapZone.y !== undefined) updates.position.y = snapZone.y;
    if (snapZone.width !== undefined) updates.size.width = snapZone.width;
    if (snapZone.height !== undefined) updates.size.height = snapZone.height;

    this.updateWindow(windowId, updates);
    this.emit('window:snapped', this.windows.get(windowId), zone);
    return true;
  }

  /**
   * Get next available z-index
   */
  getNextZIndex() {
    if (this.nextZIndex >= this.maxZIndex) {
      // Reset and redistribute z-indices
      this.redistributeZIndices();
    }
    return this.nextZIndex++;
  }

  /**
   * Redistribute z-indices when we reach max
   */
  redistributeZIndices() {
    this.nextZIndex = 1000;
    this.windowStack.forEach((id, index) => {
      this.windows.get(id).zIndex = 1000 + index;
    });
  }

  /**
   * Create window group
   */
  createGroup(groupId, windowIds) {
    windowIds.forEach(id => {
      if (this.windows.has(id)) {
        this.updateWindow(id, {
          isGrouped: true,
          groupId,
        });
      }
    });
    this.emit('group:created', { groupId, windowIds });
  }

  /**
   * Get windows in a group
   */
  getGroupWindows(groupId) {
    return this.getAllWindows().filter(w => w.groupId === groupId);
  }

  /**
   * Save layout to storage
   */
  saveLayout(layoutName = 'default') {
    const layout = {
      name: layoutName,
      windows: this.getAllWindows().map(w => ({
        id: w.id,
        title: w.title,
        position: w.position,
        size: w.size,
        state: w.state,
        isLocked: w.isLocked,
        groupId: w.groupId,
        metadata: w.metadata,
      })),
      windowStack: [...this.windowStack],
      savedAt: new Date().toISOString(),
    };

    try {
      const layouts = this.getSavedLayouts();
      layouts[layoutName] = layout;
      localStorage.setItem('window_layouts', JSON.stringify(layouts));
      this.emit('layout:saved', layout);
      return layout;
    } catch (error) {
      console.error('Failed to save layout:', error);
      return null;
    }
  }

  /**
   * Load layout from storage
   */
  loadLayout(layoutName = 'default') {
    try {
      const layouts = this.getSavedLayouts();
      const layout = layouts[layoutName];
      if (!layout) {
        console.warn(`Layout ${layoutName} not found`);
        return null;
      }

      // Clear current windows
      this.windows.clear();
      this.windowStack = [];

      // Restore windows
      layout.windows.forEach(windowData => {
        this.registerWindow(windowData);
      });

      // Restore stack order
      this.windowStack = layout.windowStack.filter(id => this.windows.has(id));

      this.emit('layout:loaded', layout);
      return layout;
    } catch (error) {
      console.error('Failed to load layout:', error);
      return null;
    }
  }

  /**
   * Get all saved layouts
   */
  getSavedLayouts() {
    try {
      const stored = localStorage.getItem('window_layouts');
      return stored ? JSON.parse(stored) : {};
    } catch (error) {
      console.error('Failed to get saved layouts:', error);
      return {};
    }
  }

  /**
   * Delete saved layout
   */
  deleteLayout(layoutName) {
    try {
      const layouts = this.getSavedLayouts();
      delete layouts[layoutName];
      localStorage.setItem('window_layouts', JSON.stringify(layouts));
      this.emit('layout:deleted', layoutName);
      return true;
    } catch (error) {
      console.error('Failed to delete layout:', error);
      return false;
    }
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

  /**
   * Clear all windows
   */
  clear() {
    this.windows.clear();
    this.windowStack = [];
    this.nextZIndex = 1000;
    this.emit('windows:cleared');
  }
}

// Singleton instance
const windowManager = new WindowManager();

export default windowManager;

