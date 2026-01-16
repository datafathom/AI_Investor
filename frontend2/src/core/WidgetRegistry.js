/**
 * Widget Registry
 * 
 * Central registry for managing available widgets.
 * Tracks widget metadata, versions, dependencies, and capabilities.
 */

class WidgetRegistry {
  constructor() {
    this.widgets = new Map(); // widgetId -> widgetData
    this.categories = new Map(); // category -> [widgetIds]
    this.listeners = new Set();
  }

  /**
   * Register a widget
   */
  register(widgetData) {
    const {
      id,
      name,
      version,
      author,
      description,
      category = 'uncategorized',
      icon,
      component,
      dependencies = [],
      permissions = [],
      metadata = {},
    } = widgetData;

    if (!id || !name || !component) {
      throw new Error('Widget must have id, name, and component');
    }

    const widget = {
      id,
      name,
      version: version || '1.0.0',
      author: author || 'Unknown',
      description: description || '',
      category,
      icon: icon || '📦',
      component,
      dependencies,
      permissions,
      metadata,
      registeredAt: new Date(),
      updatedAt: new Date(),
    };

    // Check for existing widget
    if (this.widgets.has(id)) {
      const existing = this.widgets.get(id);
      if (existing.version === widget.version) {
        console.warn(`Widget ${id} version ${version} already registered`);
        return existing;
      }
      // Update existing
      widget.updatedAt = new Date();
    }

    this.widgets.set(id, widget);

    // Add to category
    if (!this.categories.has(category)) {
      this.categories.set(category, []);
    }
    if (!this.categories.get(category).includes(id)) {
      this.categories.get(category).push(id);
    }

    this.emit('widget:registered', widget);
    return widget;
  }

  /**
   * Unregister a widget
   */
  unregister(widgetId) {
    if (!this.widgets.has(widgetId)) {
      return false;
    }

    const widget = this.widgets.get(widgetId);
    this.widgets.delete(widgetId);

    // Remove from category
    const categoryWidgets = this.categories.get(widget.category);
    if (categoryWidgets) {
      const index = categoryWidgets.indexOf(widgetId);
      if (index > -1) {
        categoryWidgets.splice(index, 1);
      }
    }

    this.emit('widget:unregistered', widget);
    return true;
  }

  /**
   * Get widget by ID
   */
  get(widgetId) {
    return this.widgets.get(widgetId) || null;
  }

  /**
   * Get all widgets
   */
  getAll() {
    return Array.from(this.widgets.values());
  }

  /**
   * Get widgets by category
   */
  getByCategory(category) {
    const widgetIds = this.categories.get(category) || [];
    return widgetIds.map(id => this.widgets.get(id)).filter(Boolean);
  }

  /**
   * Get all categories
   */
  getCategories() {
    return Array.from(this.categories.keys());
  }

  /**
   * Search widgets
   */
  search(query) {
    const lowerQuery = query.toLowerCase();
    return this.getAll().filter(widget =>
      widget.name.toLowerCase().includes(lowerQuery) ||
      widget.description.toLowerCase().includes(lowerQuery) ||
      widget.id.toLowerCase().includes(lowerQuery) ||
      widget.author.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Check if widget dependencies are satisfied
   */
  checkDependencies(widgetId) {
    const widget = this.get(widgetId);
    if (!widget) {
      return { satisfied: false, missing: [] };
    }

    const missing = widget.dependencies.filter(dep => {
      if (typeof dep === 'string') {
        return !this.widgets.has(dep);
      }
      // Support versioned dependencies: { id: 'widget-id', version: '^1.0.0' }
      const depWidget = this.get(dep.id);
      if (!depWidget) return true;
      // Simple version check (could be enhanced with semver)
      return depWidget.version !== dep.version;
    });

    return {
      satisfied: missing.length === 0,
      missing,
    };
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
   * Clear all widgets
   */
  clear() {
    this.widgets.clear();
    this.categories.clear();
    this.emit('registry:cleared');
  }
}

// Singleton instance
const widgetRegistry = new WidgetRegistry();

export default widgetRegistry;

