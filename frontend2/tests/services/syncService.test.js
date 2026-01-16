/**
 * Sync Service Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import syncService from '../../src/services/syncService';

// Mock fetch
global.fetch = vi.fn();

describe('SyncService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset online status
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      configurable: true,
      value: true,
    });
    // Clear queue
    syncService.queue = [];
    syncService.isOnline = navigator.onLine;
  });

  it('should queue action when offline', () => {
    syncService.isOnline = false;
    const action = { type: 'save', data: { id: 1 } };
    const actionId = syncService.queueAction(action);

    expect(actionId).toBeDefined();
    expect(syncService.getQueueStatus().length).toBe(1);
  });

  it('should process queue when online', async () => {
    syncService.isOnline = true;
    fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ success: true }) });

    const action = { type: 'save', url: '/api/test', method: 'POST', data: { id: 1 } };
    syncService.queueAction(action);

    // Wait for processing
    await new Promise(resolve => setTimeout(resolve, 100));

    expect(fetch).toHaveBeenCalled();
    expect(syncService.getQueueStatus().length).toBe(0);
  });

  it('should get queue status', () => {
    syncService.isOnline = false;
    syncService.queueAction({ type: 'save', data: { id: 1 } });
    syncService.queueAction({ type: 'delete', data: { id: 2 } });

    const status = syncService.getQueueStatus();
    expect(status.length).toBe(2);
  });

  it('should clear queue', () => {
    syncService.isOnline = false;
    syncService.queueAction({ type: 'save', data: { id: 1 } });
    syncService.clearQueue();

    expect(syncService.getQueueStatus().length).toBe(0);
  });

  it('should emit events when queueing', () => {
    const listener = vi.fn();
    syncService.on('action:queued', listener);

    syncService.queueAction({ type: 'save', data: { id: 1 } });

    expect(listener).toHaveBeenCalled();
    syncService.off('action:queued', listener);
  });
});

