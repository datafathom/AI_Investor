/**
 * useWidgetLayout Hook
 * 
 * Manages draggable and resizable widget layout state.
 * Persists layout to localStorage and provides layout management functions.
 */

import { useState, useEffect } from 'react';

const STORAGE_KEY = 'react_node_template_workspaces';
const ACTIVE_WORKSPACE_KEY = 'react_node_template_active_workspace';

// Default layout for the AI Investor Dashboard widgets
const DEFAULT_LAYOUT = [
  { i: 'monitor-view', x: 0, y: 0, w: 24, h: 20, minW: 16, minH: 14, maxW: 48 },
  { i: 'command-view', x: 24, y: 0, w: 24, h: 10, minW: 16, minH: 10, maxW: 48 },
  { i: 'portfolio-view', x: 24, y: 10, w: 24, h: 16, minW: 16, minH: 12, maxW: 48 },
  { i: 'research-view', x: 0, y: 20, w: 24, h: 18, minW: 16, minH: 12, maxW: 48 },
  { i: 'homeostasis-view', x: 24, y: 26, w: 24, h: 16, minW: 16, minH: 12, maxW: 48 },
  { i: 'options-chain-view', x: 0, y: 38, w: 24, h: 15, minW: 16, minH: 12, maxW: 48 },
  { i: 'market-depth-view', x: 24, y: 42, w: 12, h: 15, minW: 8, minH: 12, maxW: 24 },
  { i: 'trade-tape-view', x: 36, y: 42, w: 12, h: 15, minW: 8, minH: 12, maxW: 24 },
  { i: 'terminal-view', x: 0, y: 53, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 },
  { i: 'bar-chart', x: 24, y: 57, w: 24, h: 12, minW: 16, minH: 10, maxW: 48 },
  { i: 'socketio', x: 0, y: 63, w: 48, h: 8, minW: 16, minH: 6, maxW: 48 },
];

/**
 * Validates a layout to ensure no corruption.
 */
const validateLayout = (layout) => {
  if (!Array.isArray(layout)) return false;
  return layout.every(item => (
    typeof item.i === 'string' &&
    typeof item.x === 'number' &&
    typeof item.y === 'number' &&
    typeof item.w === 'number' &&
    typeof item.h === 'number'
  ));
};

export function useWidgetLayout() {
  const [workspaces, setWorkspaces] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        // Validate each workspace layout
        const validated = {};
        Object.entries(parsed).forEach(([name, layout]) => {
          if (validateLayout(layout)) {
            validated[name] = layout;
          }
        });
        if (Object.keys(validated).length > 0) return validated;
      }
    } catch (e) {
      console.warn('Failed to load workspaces:', e);
    }
    return { 'Default': DEFAULT_LAYOUT };
  });

  const [activeWorkspace, setActiveWorkspace] = useState(() => {
    return localStorage.getItem(ACTIVE_WORKSPACE_KEY) || 'Default';
  });

  const layout = workspaces[activeWorkspace] || DEFAULT_LAYOUT;

  const setLayout = (newLayout) => {
    if (!validateLayout(newLayout)) {
      console.error('Refusing to save invalid layout');
      return;
    }
    setWorkspaces(prev => {
      const updated = { ...prev, [activeWorkspace]: newLayout };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  };

  const saveWorkspace = (name) => {
    setWorkspaces(prev => {
      const updated = { ...prev, [name]: layout };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
    setActiveWorkspace(name);
    localStorage.setItem(ACTIVE_WORKSPACE_KEY, name);
  };

  const loadWorkspace = (name) => {
    if (workspaces[name]) {
      setActiveWorkspace(name);
      localStorage.setItem(ACTIVE_WORKSPACE_KEY, name);
    }
  };

  const resetLayout = () => {
    setWorkspaces({ 'Default': DEFAULT_LAYOUT });
    setActiveWorkspace('Default');
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(ACTIVE_WORKSPACE_KEY);
  };

  const deleteWorkspace = (name) => {
    if (name === 'Default') return;
    setWorkspaces(prev => {
      const { [name]: removed, ...rest } = prev;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(rest));
      return rest;
    });
    if (activeWorkspace === name) {
      setActiveWorkspace('Default');
    }
  };

  return {
    layout,
    setLayout,
    resetLayout,
    activeWorkspace,
    workspaces: Object.keys(workspaces),
    saveWorkspace,
    loadWorkspace,
    deleteWorkspace
  };
}

