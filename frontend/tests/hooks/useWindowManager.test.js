/**
 * useWindowManager Hook Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useWindowManager } from '../../src/hooks/useWindowManager';
import windowManager from '../../src/services/windowManager';

vi.mock('../../src/services/windowManager', () => ({
  default: {
    getAllWindows: vi.fn(() => []),
    windowStack: [],
    registerWindow: vi.fn(),
    unregisterWindow: vi.fn(),
    getWindow: vi.fn(),
    updateWindow: vi.fn(),
    bringToFront: vi.fn(),
    sendToBack: vi.fn(),
    minimizeWindow: vi.fn(),
    maximizeWindow: vi.fn(),
    restoreWindow: vi.fn(),
    toggleLock: vi.fn(),
    snapToZone: vi.fn(),
    createGroup: vi.fn(),
    getGroupWindows: vi.fn(),
    saveLayout: vi.fn(),
    loadLayout: vi.fn(),
    getSavedLayouts: vi.fn(() => []),
    deleteLayout: vi.fn(),
    on: vi.fn(),
    off: vi.fn(),
  },
}));

describe('useWindowManager', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    windowManager.getAllWindows.mockReturnValue([]);
    windowManager.windowStack = [];
  });

  it('should return window manager functions', () => {
    const { result } = renderHook(() => useWindowManager());

    expect(result.current.windows).toEqual([]);
    expect(typeof result.current.registerWindow).toBe('function');
    expect(typeof result.current.unregisterWindow).toBe('function');
    expect(typeof result.current.minimizeWindow).toBe('function');
  });

  it('should open a window', () => {
    const mockWindow = { id: 'w1', title: 'Test Window' };
    windowManager.registerWindow.mockReturnValue(mockWindow);

    const { result } = renderHook(() => useWindowManager());

    act(() => {
      result.current.registerWindow({
        id: 'w1',
        title: 'Test Window',
        component: 'TestComponent',
      });
    });

    expect(windowManager.registerWindow).toHaveBeenCalledWith({
      id: 'w1',
      title: 'Test Window',
      component: 'TestComponent',
    });
  });

  it('should close a window', () => {
    const { result } = renderHook(() => useWindowManager());

    act(() => {
      result.current.unregisterWindow('w1');
    });

    expect(windowManager.unregisterWindow).toHaveBeenCalledWith('w1');
  });

  it('should minimize a window', () => {
    const { result } = renderHook(() => useWindowManager());

    act(() => {
      result.current.minimizeWindow('w1');
    });

    expect(windowManager.minimizeWindow).toHaveBeenCalledWith('w1');
  });
});

