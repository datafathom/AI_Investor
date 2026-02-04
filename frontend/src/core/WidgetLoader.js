/**
 * Widget Loader
 * 
 * Handles dynamic loading of widgets from various sources:
 * - Local components
 * - npm packages
 * - CDN URLs
 * - Local files
 */

import widgetRegistry from './WidgetRegistry.js';
import { widgetManager } from './WidgetAPI.js';

class WidgetLoader {
  constructor() {
    this.loadedWidgets = new Map(); // widgetId -> loaded component
    this.loadingPromises = new Map(); // widgetId -> Promise
  }

  /**
   * Load widget from various sources
   */
  async load(widgetId, source) {
    // Check if already loaded
    if (this.loadedWidgets.has(widgetId)) {
      return this.loadedWidgets.get(widgetId);
    }

    // Check if currently loading
    if (this.loadingPromises.has(widgetId)) {
      return this.loadingPromises.get(widgetId);
    }

    // Start loading
    const loadPromise = this._loadWidget(widgetId, source);
    this.loadingPromises.set(widgetId, loadPromise);

    try {
      const component = await loadPromise;
      this.loadedWidgets.set(widgetId, component);
      this.loadingPromises.delete(widgetId);
      return component;
    } catch (error) {
      this.loadingPromises.delete(widgetId);
      console.error(`Failed to load widget ${widgetId}:`, error);
      throw error;
    }
  }

  /**
   * Internal widget loading logic
   */
  async _loadWidget(widgetId, source) {
    if (!source) {
      throw new Error(`No source specified for widget ${widgetId}`);
    }

    // Determine source type
    if (typeof source === 'function') {
      // Already a component
      return source;
    }

    if (typeof source === 'string') {
      // String source - could be URL, npm package, or local path
      if (source.startsWith('http://') || source.startsWith('https://')) {
        return this._loadFromURL(source);
      } else if (source.startsWith('npm:')) {
        return this._loadFromNPM(source.substring(4));
      } else {
        return this._loadFromLocal(source);
      }
    }

    if (source.type === 'url') {
      return this._loadFromURL(source.url);
    }

    if (source.type === 'npm') {
      return this._loadFromNPM(source.package, source.version);
    }

    if (source.type === 'local') {
      return this._loadFromLocal(source.path);
    }

    throw new Error(`Unknown source type for widget ${widgetId}`);
  }

  /**
   * Load widget from URL (CDN)
   */
  async _loadFromURL(url) {
    try {
      // Load script dynamically
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = url;
        script.type = 'module';
        script.onload = () => {
          // Widget should expose itself globally or via module
          // This is a simplified version - real implementation would need
          // proper module handling
          resolve(window.__widget__ || null);
        };
        script.onerror = () => reject(new Error(`Failed to load widget from ${url}`));
        document.head.appendChild(script);
      });
    } catch (error) {
      throw new Error(`Failed to load widget from URL: ${error.message}`);
    }
  }

  /**
   * Load widget from npm package
   */
  async _loadFromNPM(packageName, version = 'latest') {
    // In a real implementation, this would:
    // 1. Check if package is installed
    // 2. If not, dynamically install it (requires build system support)
    // 3. Import the package
    try {
      // For now, we'll try to import it directly
      // In production, you'd need a bundler plugin or dynamic import system
      const module = await import(packageName);
      return module.default || module;
    } catch (error) {
      throw new Error(`Failed to load widget from npm package ${packageName}: ${error.message}`);
    }
  }

  /**
   * Load widget from local file
   */
  async _loadFromLocal(path) {
    try {
      // Dynamic import of local component
      const module = await import(/* @vite-ignore */ path);
      return module.default || module;
    } catch (error) {
      throw new Error(`Failed to load widget from local path ${path}: ${error.message}`);
    }
  }

  /**
   * Unload widget
   */
  unload(widgetId) {
    this.loadedWidgets.delete(widgetId);
    widgetManager.destroyInstance(widgetId);
  }

  /**
   * Check if widget is loaded
   */
  isLoaded(widgetId) {
    return this.loadedWidgets.has(widgetId);
  }

  /**
   * Get loaded widget component
   */
  getLoaded(widgetId) {
    return this.loadedWidgets.get(widgetId) || null;
  }

  /**
   * Clear all loaded widgets
   */
  clear() {
    this.loadedWidgets.forEach((_, widgetId) => {
      widgetManager.destroyInstance(widgetId);
    });
    this.loadedWidgets.clear();
    this.loadingPromises.clear();
  }
}

// Singleton instance
const widgetLoader = new WidgetLoader();

export default widgetLoader;

