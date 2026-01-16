/**
 * useTheme Hook Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useTheme } from '../../src/hooks/useTheme';
import themeEngine from '../../src/themes/ThemeEngine';

vi.mock('../../src/themes/ThemeEngine', () => ({
  default: {
    getCurrentTheme: vi.fn(),
    getAllThemes: vi.fn(),
    applyTheme: vi.fn(),
    registerTheme: vi.fn(),
    createCustomTheme: vi.fn(),
    exportTheme: vi.fn(),
    importTheme: vi.fn(),
    on: vi.fn(),
    off: vi.fn(),
  },
}));

describe('useTheme', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    themeEngine.getCurrentTheme.mockReturnValue({ id: 'light', name: 'Light' });
    themeEngine.getAllThemes.mockReturnValue([
      { id: 'light', name: 'Light' },
      { id: 'dark', name: 'Dark' },
    ]);
  });

  it('should return current theme', () => {
    const { result } = renderHook(() => useTheme());

    expect(result.current.currentTheme).toEqual({ id: 'light', name: 'Light' });
  });

  it('should apply theme', () => {
    const { result } = renderHook(() => useTheme());

    act(() => {
      result.current.applyTheme('dark');
    });

    expect(themeEngine.applyTheme).toHaveBeenCalledWith('dark');
  });

  it('should register theme', () => {
    const { result } = renderHook(() => useTheme());

    act(() => {
      result.current.registerTheme({ id: 'custom', name: 'Custom' });
    });

    expect(themeEngine.registerTheme).toHaveBeenCalledWith({
      id: 'custom',
      name: 'Custom',
    });
  });
});

