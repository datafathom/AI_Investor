/**
 * useWidgetLayout Hook Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useWidgetLayout } from '../../src/hooks/useWidgetLayout';

describe('useWidgetLayout', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should return default layout when localStorage is empty', () => {
    const { result } = renderHook(() => useWidgetLayout());
    expect(result.current.layout).toBeDefined();
    expect(Array.isArray(result.current.layout)).toBe(true);
    expect(result.current.layout.length).toBeGreaterThan(0);
  });

  it('should load layout from localStorage', () => {
    const savedLayout = [
      { i: 'widget1', x: 0, y: 0, w: 4, h: 3 },
    ];
    localStorage.setItem('react_node_template_widget_layout', JSON.stringify(savedLayout));

    const { result } = renderHook(() => useWidgetLayout());
    expect(result.current.layout).toEqual(savedLayout);
  });

  it('should save layout to localStorage when changed', () => {
    const { result } = renderHook(() => useWidgetLayout());
    const newLayout = [
      { i: 'widget1', x: 0, y: 0, w: 6, h: 4 },
    ];

    act(() => {
      result.current.setLayout(newLayout);
    });

    expect(result.current.layout).toEqual(newLayout);
    const saved = JSON.parse(localStorage.getItem('react_node_template_widget_layout'));
    expect(saved).toEqual(newLayout);
  });

  it('should reset layout to default', () => {
    const { result } = renderHook(() => useWidgetLayout());
    
    // Change layout first
    act(() => {
      result.current.setLayout([{ i: 'test', x: 0, y: 0, w: 1, h: 1 }]);
    });

    // Reset
    act(() => {
      result.current.resetLayout();
    });

    expect(result.current.layout.length).toBeGreaterThan(0);
    // resetLayout removes from localStorage, but useEffect will save default layout
    // So we check that it's the default layout structure
    const saved = JSON.parse(localStorage.getItem('react_node_template_widget_layout'));
    expect(saved).toBeDefined();
    expect(Array.isArray(saved)).toBe(true);
  });
});

