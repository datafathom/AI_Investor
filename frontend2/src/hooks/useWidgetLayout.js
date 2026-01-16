/**
 * useWidgetLayout Hook
 * 
 * Manages draggable and resizable widget layout state.
 * Persists layout to localStorage and provides layout management functions.
 */

import { useState, useEffect } from 'react';

const STORAGE_KEY = 'react_node_template_widget_layout';
const DEFAULT_LAYOUT = [
  { i: 'api', x: 0, y: 0, w: 6, h: 5, minW: 4, minH: 3, maxW: 12 },
  { i: 'palette', x: 6, y: 0, w: 6, h: 5, minW: 4, minH: 3, maxW: 12 },
  { i: 'checklist', x: 0, y: 5, w: 6, h: 6, minW: 4, minH: 4, maxW: 12 },
  { i: 'telemetry', x: 6, y: 5, w: 6, h: 6, minW: 4, minH: 4, maxW: 12 },
  { i: 'ux', x: 0, y: 11, w: 6, h: 5, minW: 4, minH: 3, maxW: 12 },
  { i: 'socketio', x: 6, y: 11, w: 6, h: 7, minW: 4, minH: 4, maxW: 12 },
  { i: 'ping-api', x: 0, y: 18, w: 4, h: 3, minW: 3, minH: 2, maxW: 12 },
  { i: 'server-status', x: 4, y: 18, w: 8, h: 3, minW: 4, minH: 2, maxW: 12 },
];

export function useWidgetLayout() {
  const [layout, setLayout] = useState(() => {
    // Load from localStorage or use default
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        // Validate layout structure
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (error) {
      console.warn('[useWidgetLayout] Failed to load layout from localStorage:', error);
    }
    return DEFAULT_LAYOUT;
  });

  // Save to localStorage whenever layout changes
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(layout));
    } catch (error) {
      console.warn('[useWidgetLayout] Failed to save layout to localStorage:', error);
    }
  }, [layout]);

  const handleLayoutChange = (newLayout) => {
    setLayout(newLayout);
  };

  const resetLayout = () => {
    setLayout(DEFAULT_LAYOUT);
    localStorage.removeItem(STORAGE_KEY);
  };

  return {
    layout,
    setLayout: handleLayoutChange,
    resetLayout,
  };
}

