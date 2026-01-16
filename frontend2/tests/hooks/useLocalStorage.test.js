/**
 * useLocalStorage Hook Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useLocalStorage } from '../../src/hooks/useLocalStorage';

describe('useLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  it('should return initial value when localStorage is empty', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', 'initial'));
    expect(result.current[0]).toBe('initial');
  });

  it('should read value from localStorage', () => {
    localStorage.setItem('test-key', JSON.stringify('stored-value'));
    const { result } = renderHook(() => useLocalStorage('test-key', 'initial'));
    expect(result.current[0]).toBe('stored-value');
  });

  it('should update localStorage when value changes', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', 'initial'));

    act(() => {
      result.current[1]('updated-value');
    });

    expect(result.current[0]).toBe('updated-value');
    expect(localStorage.getItem('test-key')).toBe(JSON.stringify('updated-value'));
  });

  it('should handle function updates', () => {
    const { result } = renderHook(() => useLocalStorage('test-key', 0));

    act(() => {
      result.current[1]((prev) => prev + 1);
    });

    expect(result.current[0]).toBe(1);
    expect(localStorage.getItem('test-key')).toBe('1');
  });

  it('should handle complex objects', () => {
    const initialValue = { name: 'test', count: 0 };
    const { result } = renderHook(() => useLocalStorage('test-key', initialValue));

    act(() => {
      result.current[1]({ name: 'updated', count: 5 });
    });

    expect(result.current[0]).toEqual({ name: 'updated', count: 5 });
    expect(JSON.parse(localStorage.getItem('test-key'))).toEqual({ name: 'updated', count: 5 });
  });

  it('should handle localStorage errors gracefully', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    // Mock localStorage.getItem to throw
    const originalGetItem = localStorage.getItem;
    localStorage.getItem = vi.fn(() => {
      throw new Error('Storage error');
    });

    const { result } = renderHook(() => useLocalStorage('test-key', 'fallback'));
    expect(result.current[0]).toBe('fallback');

    localStorage.getItem = originalGetItem;
    consoleError.mockRestore();
  });
});


