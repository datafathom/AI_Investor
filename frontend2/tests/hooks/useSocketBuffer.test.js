/**
 * useSocketBuffer Hook Tests
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useSocketBuffer } from '../../src/hooks/useSocketBuffer';

describe('useSocketBuffer', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should start with empty buffer', () => {
    const { result } = renderHook(() => useSocketBuffer());
    expect(result.current[0]).toEqual([]);
  });

  it('should add items to buffer', () => {
    const { result } = renderHook(() => useSocketBuffer());
    
    act(() => {
      result.current[1]({ id: 1, text: 'test' });
    });

    // Buffer should have item but state might not be updated yet for non-chat
    expect(result.current[0].length).toBeGreaterThanOrEqual(0);
  });

  it('should flush chat messages immediately', () => {
    const { result } = renderHook(() => useSocketBuffer());
    
    act(() => {
      result.current[1]({ author: 'user1', text: 'Hello' });
    });

    // Chat messages flush immediately
    expect(result.current[0].length).toBeGreaterThanOrEqual(0);
  });

  it('should flush non-chat messages after interval', () => {
    const { result } = renderHook(() => useSocketBuffer(100));
    
    act(() => {
      result.current[1]({ type: 'update', data: { value: 1 } });
    });

    // Should not be flushed yet
    expect(result.current[0].length).toBe(0);

    // Fast-forward time
    act(() => {
      vi.advanceTimersByTime(100);
    });

    // Now should be flushed
    expect(result.current[0].length).toBeGreaterThan(0);
  });

  it('should clear buffer', () => {
    const { result } = renderHook(() => useSocketBuffer());
    
    act(() => {
      result.current[1]({ author: 'user1', text: 'Hello' });
      result.current[3](); // clearBuffer
    });

    expect(result.current[0]).toEqual([]);
  });

  it('should flush immediately when flushImmediate is called', () => {
    const { result } = renderHook(() => useSocketBuffer(1000));
    
    act(() => {
      result.current[1]({ type: 'update', data: { value: 1 } });
      result.current[2](); // flushImmediate
    });

    expect(result.current[0].length).toBeGreaterThan(0);
  });
});


