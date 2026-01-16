/**
 * Widget API Standard
 * 
 * Standardized interface that all widgets must implement.
 * Provides lifecycle hooks, event system, and widget communication.
 */

export class WidgetAPI {
  constructor(widgetId, widgetManager) {
    this.id = widgetId;
    this.manager = widgetManager;
    this.state = {};
    this.listeners = new Map();
    this.lifecycleHooks = {
      onMount: null,
      onUnmount: null,
      onResize: null,
      onFocus: null,
      onBlur: null,
      onUpdate: null,
    };
  }

  /**
   * Set widget state
   */
  setState(updates) {
    this.state = { ...this.state, ...updates };
    if (this.lifecycleHooks.onUpdate) {
      this.lifecycleHooks.onUpdate(this.state);
    }
  }

  /**
   * Get widget state
   */
  getState() {
    return { ...this.state };
  }

  /**
   * Register lifecycle hook
   */
  onLifecycle(hook, callback) {
    if (Object.prototype.hasOwnProperty.call(this.lifecycleHooks, hook)) {
      this.lifecycleHooks[hook] = callback;
    } else {
      console.warn(`Unknown lifecycle hook: ${hook}`);
    }
  }

  /**
   * Emit event to other widgets
   */
  emit(event, data) {
    if (this.manager) {
      this.manager.emitWidgetEvent(this.id, event, data);
    }
  }

  /**
   * Listen to events from other widgets
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  /**
   * Remove event listener
   */
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  /**
   * Handle incoming event
   */
  handleEvent(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in widget ${this.id} event handler:`, error);
        }
      });
    }
  }

  /**
   * Request permission
   */
  async requestPermission(permission) {
    if (this.manager) {
      return this.manager.requestPermission(this.id, permission);
    }
    return false;
  }

  /**
   * Get widget configuration
   */
  getConfig() {
    if (this.manager) {
      return this.manager.getWidgetConfig(this.id);
    }
    return {};
  }

  /**
   * Save widget configuration
   */
  saveConfig(config) {
    if (this.manager) {
      this.manager.saveWidgetConfig(this.id, config);
    }
  }

  /**
   * Show notification
   */
  showNotification(message, type = 'info') {
    if (this.manager) {
      this.manager.showNotification(message, type);
    }
  }

  /**
   * Cleanup
   */
  destroy() {
    if (this.lifecycleHooks.onUnmount) {
      this.lifecycleHooks.onUnmount();
    }
    this.listeners.clear();
    this.lifecycleHooks = {};
  }
}

/**
 * Widget Manager
 * Manages widget instances and communication
 */
export class WidgetManager {
  constructor() {
    this.instances = new Map(); // widgetId -> WidgetAPI instance
    this.eventBus = new EventTarget();
  }

  /**
   * Create widget instance
   */
  createInstance(widgetId) {
    if (this.instances.has(widgetId)) {
      return this.instances.get(widgetId);
    }

    const api = new WidgetAPI(widgetId, this);
    this.instances.set(widgetId, api);
    return api;
  }

  /**
   * Get widget instance
   */
  getInstance(widgetId) {
    return this.instances.get(widgetId) || null;
  }

  /**
   * Destroy widget instance
   */
  destroyInstance(widgetId) {
    const instance = this.instances.get(widgetId);
    if (instance) {
      instance.destroy();
      this.instances.delete(widgetId);
    }
  }

  /**
   * Emit event to all widgets
   */
  emitWidgetEvent(sourceId, event, data) {
    this.instances.forEach((instance, widgetId) => {
      if (widgetId !== sourceId) {
        instance.handleEvent(event, data);
      }
    });
  }

  /**
   * Request permission (placeholder - would integrate with permission system)
   */
  async requestPermission(widgetId, permission) {
    // TODO: Integrate with permission system
    console.log(`Widget ${widgetId} requesting permission: ${permission}`);
    return true;
  }

  /**
   * Get widget configuration
   */
  getWidgetConfig(widgetId) {
    try {
      const stored = localStorage.getItem(`widget_config_${widgetId}`);
      return stored ? JSON.parse(stored) : {};
    } catch (error) {
      console.error(`Failed to get config for widget ${widgetId}:`, error);
      return {};
    }
  }

  /**
   * Save widget configuration
   */
  saveWidgetConfig(widgetId, config) {
    try {
      localStorage.setItem(`widget_config_${widgetId}`, JSON.stringify(config));
    } catch (error) {
      console.error(`Failed to save config for widget ${widgetId}:`, error);
    }
  }

  /**
   * Show notification (placeholder - would integrate with notification system)
   */
  showNotification(message, type) {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // TODO: Integrate with notification system
  }
}

// Singleton instance
export const widgetManager = new WidgetManager();

