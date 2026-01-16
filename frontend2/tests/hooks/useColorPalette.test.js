/**
 * useColorPalette Hook Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useColorPalette } from '../../src/hooks/useColorPalette';

// Mock colorPalette utils
const mockPalette = {
  burgundy: {
    primary: '#5a1520',
    dark: '#3d0e15',
  },
  cream: {
    primary: '#fefae8',
    light: '#fffef0',
  },
};

const mockApplyColorPalette = vi.fn();
const mockGetColorPalette = vi.fn(() => mockPalette);

vi.mock('../../src/utils/colorPalette', () => ({
  getColorPalette: () => mockGetColorPalette(),
  applyColorPalette: (palette) => mockApplyColorPalette(palette),
}));

describe('useColorPalette', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return palette object', () => {
    const { result } = renderHook(() => useColorPalette());
    expect(result.current.palette).toEqual(mockPalette);
  });

  it('should call applyColorPalette on mount', () => {
    renderHook(() => useColorPalette());
    expect(mockApplyColorPalette).toHaveBeenCalledWith(mockPalette);
  });

  it('should return same palette object on re-render', () => {
    const { result, rerender } = renderHook(() => useColorPalette());
    const firstPalette = result.current.palette;

    rerender();
    expect(result.current.palette).toBe(firstPalette);
  });
});

