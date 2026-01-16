/**
 * Permission Service Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import permissionService from '../../src/services/permissionService';

// Mock fetch
global.fetch = vi.fn();

describe('PermissionService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    // Clear the service cache between tests
    permissionService.clearAllCache();
  });

  it('should check permission', async () => {
    const mockResponse = { hasPermission: true };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await permissionService.hasPermission(1, 'widget', 'read');

    expect(result).toBe(true);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/permissions/check'),
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      })
    );
  });

  it('should cache permission results', async () => {
    const mockResponse = { hasPermission: true };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await permissionService.hasPermission(1, 'widget', 'read');
    await permissionService.hasPermission(1, 'widget', 'read');

    // Should only call fetch once due to caching
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it('should get user permissions', async () => {
    const mockPermissions = ['widget:read', 'widget:write'];
    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockPermissions,
    });

    const result = await permissionService.getUserPermissions(1);

    expect(result).toEqual(mockPermissions);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/users/1/permissions')
    );
  });
});

