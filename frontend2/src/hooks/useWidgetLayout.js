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
  { i: 'monitor-view', x: 0, y: 0, w: 24, h: 20, minW: 16, minH: 10, maxW: 48 },
  { i: 'command-view', x: 24, y: 0, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 },
  { i: 'options-chain-view', x: 0, y: 20, w: 24, h: 12, minW: 12, minH: 8, maxW: 48 },
  { i: 'market-depth-view', x: 24, y: 10, w: 12, h: 15, minW: 8, minH: 10, maxW: 24 },
  { i: 'trade-tape-view', x: 36, y: 10, w: 12, h: 15, minW: 8, minH: 10, maxW: 24 },
  { i: 'socketio', x: 0, y: 32, w: 24, h: 7, minW: 16, minH: 4, maxW: 48 },
];

export function useWidgetLayout() {
  const [workspaces, setWorkspaces] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        return JSON.parse(saved);
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

