/**
 * Presence Service Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import presenceService from '../../src/services/presenceService';

// Mock socket.io-client
const mockSocket = {
  emit: vi.fn(),
  on: vi.fn(),
  off: vi.fn(),
  disconnect: vi.fn(),
  connected: true,
};

vi.mock('socket.io-client', () => ({
  default: vi.fn(() => mockSocket),
}));

describe('PresenceService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset service state
    presenceService.socket = null;
    presenceService.users.clear();
    presenceService.currentUser = null;
    presenceService.listeners.clear();
  });

  it('should initialize with user', () => {
    presenceService.initialize(1, 'testuser');

    expect(presenceService.currentUser).toEqual({ id: 1, username: 'testuser' });
    expect(mockSocket.emit).toHaveBeenCalledWith('presence:register', {
      userId: 1,
      username: 'testuser',
      timestamp: expect.any(String),
    });
  });

  it('should get online users', () => {
    presenceService.users.set(1, { userId: 1, username: 'user1' });
    presenceService.users.set(2, { userId: 2, username: 'user2' });

    const users = presenceService.getOnlineUsers();
    expect(users.length).toBe(2);
  });

  it('should update activity', () => {
    presenceService.initialize(1, 'testuser');
    presenceService.updateActivity('/dashboard', 'viewing');

    expect(mockSocket.emit).toHaveBeenCalledWith('presence:activity', {
      userId: 1,
      page: '/dashboard',
      action: 'viewing',
      timestamp: expect.any(String),
    });
  });

  it('should disconnect', () => {
    presenceService.initialize(1, 'testuser');
    presenceService.disconnect();

    expect(mockSocket.disconnect).toHaveBeenCalled();
    expect(presenceService.socket).toBeNull();
  });

  it('should emit events', () => {
    const listener = vi.fn();
    presenceService.on('presence:updated', listener);

    // Simulate presence update
    const updateData = { userId: 1, username: 'user1' };
    presenceService.emit('presence:updated', updateData);

    expect(listener).toHaveBeenCalledWith(updateData);
    presenceService.off('presence:updated', listener);
  });
});

