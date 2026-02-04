/**
 * Theme Editor Component
 * 
 * Visual theme editor with live preview.
 * Allows users to customize colors, spacing, typography, etc.
 */

import React, { useState } from 'react';
import { useTheme } from '../../hooks/useTheme';
import themeEngine from '../../themes/ThemeEngine';
import './ThemeEditor.css';

export default function ThemeEditor({ onClose }) {
  const { currentTheme, themes, applyTheme, createCustomTheme, exportTheme, importTheme } = useTheme();
  const [editingTheme, setEditingTheme] = useState(currentTheme);
  const [customizations, setCustomizations] = useState({});
  const [showImport, setShowImport] = useState(false);
  const [importText, setImportText] = useState('');

  const handleColorChange = (path, value) => {
    const newCustomizations = { ...customizations };
    const keys = path.split('.');
    let current = newCustomizations;
    
    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) {
        current[keys[i]] = {};
      }
      current = current[keys[i]];
    }
    
    current[keys[keys.length - 1]] = value;
    setCustomizations(newCustomizations);

    // Apply preview
    const previewTheme = {
      ...editingTheme,
      colors: {
        ...editingTheme.colors,
        ...newCustomizations.colors,
      },
    };
    themeEngine.applyTheme(previewTheme.id);
  };

  const handleSaveCustomTheme = () => {
    const name = prompt('Enter theme name:');
    if (!name) return;

    const customTheme = createCustomTheme(name, customizations);
    applyTheme(customTheme.id);
    setCustomizations({});
    alert(`Theme "${name}" saved!`);
  };

  const handleExport = () => {
    const json = exportTheme(currentTheme.id);
    navigator.clipboard.writeText(json);
    alert('Theme exported to clipboard!');
  };

  const handleImport = () => {
    try {
      const theme = importTheme(importText);
      applyTheme(theme.id);
      setShowImport(false);
      setImportText('');
      alert('Theme imported successfully!');
    } catch (error) {
      alert(`Failed to import theme: ${error.message}`);
    }
  };

  const renderColorPicker = (label, path, value) => {
    if (typeof value === 'object') {
      return (
        <div key={path} className="theme-editor-section">
          <h4>{label}</h4>
          {Object.entries(value).map(([key, val]) =>
            renderColorPicker(key, `${path}.${key}`, val)
          )}
        </div>
      );
    }

    return (
      <div key={path} className="theme-editor-color-item">
        <label>{label}</label>
        <div className="theme-editor-color-inputs">
          <input
            type="color"
            value={value}
            onChange={(e) => handleColorChange(path, e.target.value)}
            className="theme-editor-color-picker"
          />
          <input
            type="text"
            value={value}
            onChange={(e) => handleColorChange(path, e.target.value)}
            className="theme-editor-color-text"
          />
        </div>
      </div>
    );
  };

  return (
    <div className="theme-editor">
      <div className="theme-editor-header">
        <h2>Theme Editor</h2>
        <button onClick={onClose} className="theme-editor-close"></button>
      </div>

      <div className="theme-editor-content">
        <div className="theme-editor-sidebar">
          <h3>Available Themes</h3>
          <div className="theme-editor-theme-list">
            {themes.map(theme => (
              <div
                key={theme.id}
                className={`theme-editor-theme-item ${currentTheme?.id === theme.id ? 'active' : ''}`}
                onClick={() => {
                  setEditingTheme(theme);
                  applyTheme(theme.id);
                  setCustomizations({});
                }}
              >
                <span className="theme-editor-theme-name">{theme.name}</span>
                {currentTheme?.id === theme.id && (
                  <span className="theme-editor-theme-badge">Active</span>
                )}
              </div>
            ))}
          </div>

          <div className="theme-editor-actions">
            <button onClick={handleExport} className="theme-editor-btn">
              Export Theme
            </button>
            <button onClick={() => setShowImport(!showImport)} className="theme-editor-btn">
              Import Theme
            </button>
            {Object.keys(customizations).length > 0 && (
              <button onClick={handleSaveCustomTheme} className="theme-editor-btn theme-editor-btn-primary">
                Save Custom Theme
              </button>
            )}
          </div>

          {showImport && (
            <div className="theme-editor-import">
              <textarea
                value={importText}
                onChange={(e) => setImportText(e.target.value)}
                placeholder="Paste theme JSON here..."
                className="theme-editor-import-textarea"
              />
              <button onClick={handleImport} className="theme-editor-btn theme-editor-btn-primary">
                Import
              </button>
            </div>
          )}
        </div>

        <div className="theme-editor-main">
          {editingTheme && (
            <>
              <h3>Customize: {editingTheme.name}</h3>
              <div className="theme-editor-sections">
                {editingTheme.colors && (
                  <div className="theme-editor-section">
                    <h4>Colors</h4>
                    {Object.entries(editingTheme.colors).map(([key, value]) =>
                      renderColorPicker(key, `colors.${key}`, value)
                    )}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

