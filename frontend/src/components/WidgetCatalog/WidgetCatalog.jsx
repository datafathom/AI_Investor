/**
 * Widget Catalog Component
 * 
 * Browse and install widgets from a central repository.
 * Shows available widgets, their details, and installation status.
 */

import React, { useState, useEffect } from 'react';
import widgetRegistry from '../../core/WidgetRegistry.js';
import widgetLoader from '../../core/WidgetLoader.js';
import { widgetManager } from '../../core/WidgetAPI.js';
import './WidgetCatalog.css';

export default function WidgetCatalog({ onInstall, onClose }) {
  const [widgets, setWidgets] = useState(() => widgetRegistry.getAll());
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedWidget, setSelectedWidget] = useState(null);
  const [installing, setInstalling] = useState(new Set());

  useEffect(() => {
    const updateWidgets = () => {
      setWidgets(widgetRegistry.getAll());
    };

    widgetRegistry.on('widget:registered', updateWidgets);
    widgetRegistry.on('widget:unregistered', updateWidgets);

    return () => {
      widgetRegistry.off('widget:registered', updateWidgets);
      widgetRegistry.off('widget:unregistered', updateWidgets);
    };
  }, []);

  const categories = ['all', ...widgetRegistry.getCategories()];
  const filteredWidgets = widgets.filter(widget => {
    const matchesSearch = 
      widget.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      widget.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      widget.id.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = selectedCategory === 'all' || widget.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });

  const handleInstall = async (widget) => {
    if (installing.has(widget.id)) return;

    setInstalling(prev => new Set(prev).add(widget.id));

    try {
      // Check dependencies
      const deps = widgetRegistry.checkDependencies(widget.id);
      if (!deps.satisfied) {
        alert(`Missing dependencies: ${deps.missing.join(', ')}`);
        return;
      }

      // Load widget component
      if (widget.source) {
        await widgetLoader.load(widget.id, widget.source);
      }

      // Create widget instance
      widgetManager.createInstance(widget.id);

      // Call onInstall callback if provided
      if (onInstall) {
        onInstall(widget);
      }

      alert(`Widget "${widget.name}" installed successfully!`);
    } catch (error) {
      console.error('Failed to install widget:', error);
      alert(`Failed to install widget: ${error.message}`);
    } finally {
      setInstalling(prev => {
        const next = new Set(prev);
        next.delete(widget.id);
        return next;
      });
    }
  };

  const handleUninstall = (widget) => {
    if (confirm(`Uninstall widget "${widget.name}"?`)) {
      widgetLoader.unload(widget.id);
      widgetRegistry.unregister(widget.id);
      setSelectedWidget(null);
    }
  };

  const isInstalled = (widgetId) => {
    return widgetLoader.isLoaded(widgetId);
  };

  return (
    <div className="widget-catalog">
      <div className="widget-catalog-header">
        <h2>Widget Catalog</h2>
        <button onClick={onClose} className="widget-catalog-close"></button>
      </div>

      <div className="widget-catalog-search">
        <input
          type="text"
          placeholder="Search widgets..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="widget-catalog-search-input"
        />
      </div>

      <div className="widget-catalog-filters">
        {categories.map(category => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`widget-catalog-filter ${selectedCategory === category ? 'active' : ''}`}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="widget-catalog-content">
        <div className="widget-catalog-list">
          {filteredWidgets.length === 0 ? (
            <div className="widget-catalog-empty">
              {searchQuery ? 'No widgets match your search' : 'No widgets available'}
            </div>
          ) : (
            filteredWidgets.map(widget => (
              <div
                key={widget.id}
                className={`widget-catalog-item ${selectedWidget?.id === widget.id ? 'selected' : ''} ${isInstalled(widget.id) ? 'installed' : ''}`}
                onClick={() => setSelectedWidget(widget)}
              >
                <div className="widget-catalog-item-icon">{widget.icon}</div>
                <div className="widget-catalog-item-info">
                  <div className="widget-catalog-item-name">{widget.name}</div>
                  <div className="widget-catalog-item-meta">
                    {widget.author}  v{widget.version}  {widget.category}
                  </div>
                </div>
                {isInstalled(widget.id) && (
                  <span className="widget-catalog-item-badge">Installed</span>
                )}
              </div>
            ))
          )}
        </div>

        {selectedWidget && (
          <div className="widget-catalog-details">
            <div className="widget-catalog-details-header">
              <span className="widget-catalog-details-icon">{selectedWidget.icon}</span>
              <div>
                <h3>{selectedWidget.name}</h3>
                <p className="widget-catalog-details-meta">
                  by {selectedWidget.author}  v{selectedWidget.version}
                </p>
              </div>
            </div>

            <div className="widget-catalog-details-content">
              <p className="widget-catalog-details-description">
                {selectedWidget.description || 'No description available'}
              </p>

              {selectedWidget.dependencies.length > 0 && (
                <div className="widget-catalog-details-section">
                  <h4>Dependencies</h4>
                  <ul>
                    {selectedWidget.dependencies.map((dep, idx) => (
                      <li key={idx}>
                        {typeof dep === 'string' ? dep : `${dep.id} (${dep.version})`}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {selectedWidget.permissions.length > 0 && (
                <div className="widget-catalog-details-section">
                  <h4>Permissions</h4>
                  <ul>
                    {selectedWidget.permissions.map((perm, idx) => (
                      <li key={idx}>{perm}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="widget-catalog-details-actions">
              {isInstalled(selectedWidget.id) ? (
                <button
                  onClick={() => handleUninstall(selectedWidget)}
                  className="widget-catalog-btn widget-catalog-btn-danger"
                >
                  Uninstall
                </button>
              ) : (
                <button
                  onClick={() => handleInstall(selectedWidget)}
                  disabled={installing.has(selectedWidget.id)}
                  className="widget-catalog-btn widget-catalog-btn-primary"
                >
                  {installing.has(selectedWidget.id) ? 'Installing...' : 'Install'}
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

