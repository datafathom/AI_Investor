/**
 * Permission Service Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import permissionService from '../../src/services/permissionService';

import { describe, it, expect, beforeEach, vi } from 'vitest';
import permissionService from '../../src/services/permissionService';
import apiClient from '../../src/services/apiClient';

// Mock apiClient
vi.mock('../../src/services/apiClient');

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
    expect(result).toBe(true);
    expect(apiClient.post).toHaveBeenCalledWith(
      expect.stringContaining('/permissions/check'),
      expect.anything()
    );
  });

  it('should cache permission results', async () => {
    const mockResponse = { hasPermission: true };
    apiClient.post.mockResolvedValueOnce({
      data: mockResponse,
    });

    await permissionService.hasPermission(1, 'widget', 'read');
    await permissionService.hasPermission(1, 'widget', 'read');

    // Should only call fetch once due to caching
    expect(apiClient.post).toHaveBeenCalledTimes(1);
  });

  it('should get user permissions', async () => {
    const mockPermissions = ['widget:read', 'widget:write'];
    apiClient.get.mockResolvedValue({
      data: mockPermissions,
    });

    const result = await permissionService.getUserPermissions(1);

    expect(result).toEqual(mockPermissions);
    expect(result).toEqual(mockPermissions);
    expect(apiClient.get).toHaveBeenCalledWith(
      expect.stringContaining('/users/1/permissions')
    );
  });
});

