/**
 * Layout Builder Component
 * 
 * Visual drag-and-drop layout editor.
 * Allows users to create custom layouts with different layout types.
 */

import React, { useState } from 'react';
import { useWidgetLayout } from '../../hooks/useWidgetLayout';
import './LayoutBuilder.css';

const LAYOUT_TYPES = [
  { id: 'grid', name: 'Grid Layout', icon: '' },
  { id: 'split', name: 'Split Panes', icon: '' },
  { id: 'tabs', name: 'Tabbed', icon: '' },
  { id: 'accordion', name: 'Accordion', icon: '' },
];

export default function LayoutBuilder({ onSave, onClose }) {
  const { layout, setLayout } = useWidgetLayout();
  const [selectedType, setSelectedType] = useState('grid');
  const [layoutName, setLayoutName] = useState('');
  const [previewMode, setPreviewMode] = useState(false);

  const handleSaveLayout = () => {
    if (!layoutName.trim()) {
      alert('Please enter a layout name');
      return;
    }

    const layoutData = {
      type: selectedType,
      name: layoutName,
      layout: [...layout],
      createdAt: new Date().toISOString(),
    };

    if (onSave) {
      onSave(layoutData);
    }

    alert(`Layout "${layoutName}" saved!`);
    setLayoutName('');
  };

  const handleResetLayout = () => {
    if (confirm('Reset layout to default?')) {
      setLayout([]);
    }
  };

  return (
    <div className="layout-builder">
      <div className="layout-builder-header">
        <h2>Layout Builder</h2>
        <button onClick={onClose} className="layout-builder-close"></button>
      </div>

      <div className="layout-builder-content">
        <div className="layout-builder-sidebar">
          <div className="layout-builder-section">
            <h3>Layout Type</h3>
            <div className="layout-builder-types">
              {LAYOUT_TYPES.map(type => (
                <button
                  key={type.id}
                  onClick={() => setSelectedType(type.id)}
                  className={`layout-builder-type ${selectedType === type.id ? 'active' : ''}`}
                >
                  <span className="layout-builder-type-icon">{type.icon}</span>
                  <span className="layout-builder-type-name">{type.name}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="layout-builder-section">
            <h3>Save Layout</h3>
            <input
              type="text"
              placeholder="Layout name..."
              value={layoutName}
              onChange={(e) => setLayoutName(e.target.value)}
              className="layout-builder-input"
            />
            <div className="layout-builder-actions">
              <button
                onClick={handleSaveLayout}
                className="layout-builder-btn layout-builder-btn-primary"
              >
                Save Layout
              </button>
              <button
                onClick={handleResetLayout}
                className="layout-builder-btn"
              >
                Reset
              </button>
            </div>
          </div>

          <div className="layout-builder-section">
            <h3>Preview</h3>
            <button
              onClick={() => setPreviewMode(!previewMode)}
              className={`layout-builder-btn ${previewMode ? 'active' : ''}`}
            >
              {previewMode ? 'Exit Preview' : 'Preview Layout'}
            </button>
          </div>
        </div>

        <div className="layout-builder-main">
          {previewMode ? (
            <div className="layout-builder-preview">
              <p>Layout preview will show here</p>
              <p>Current layout has {layout.length} items</p>
            </div>
          ) : (
            <div className="layout-builder-editor">
              <p>Layout editor for {selectedType} layout</p>
              <p>Drag and drop widgets to arrange them</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

