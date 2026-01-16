/**
 * usePermissions Hook Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { usePermissions } from '../../src/hooks/usePermissions';
import permissionService from '../../src/services/permissionService';
import { authService } from '../../src/utils/authService';

// Mock services
vi.mock('../../src/services/permissionService', () => ({
  default: {
    getUserPermissions: vi.fn(),
    hasPermission: vi.fn(),
    hasRole: vi.fn(),
    hasAnyPermission: vi.fn(),
    hasAllPermissions: vi.fn(),
  },
}));

vi.mock('../../src/utils/authService', () => ({
  authService: {
    getUser: vi.fn(),
  },
}));

describe('usePermissions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return empty permissions when user is not logged in', async () => {
    authService.getUser.mockReturnValue(null);
    permissionService.getUserPermissions.mockResolvedValue([]);

    const { result } = renderHook(() => usePermissions());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.user).toBeNull();
    expect(result.current.permissions).toEqual([]);
  });

  it('should load permissions for logged in user', async () => {
    const mockUser = { id: 1, username: 'testuser' };
    const mockPermissions = ['widget:read', 'widget:write'];
    
    authService.getUser.mockReturnValue(mockUser);
    permissionService.getUserPermissions.mockResolvedValue(mockPermissions);

    const { result } = renderHook(() => usePermissions());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.permissions).toEqual(mockPermissions);
    expect(permissionService.getUserPermissions).toHaveBeenCalledWith(1);
  });

  it('should check permission', async () => {
    const mockUser = { id: 1, username: 'testuser' };
    authService.getUser.mockReturnValue(mockUser);
    permissionService.getUserPermissions.mockResolvedValue([]);
    permissionService.hasPermission.mockResolvedValue(true);

    const { result } = renderHook(() => usePermissions());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const hasPermission = await result.current.hasPermission('widget', 'read');
    expect(hasPermission).toBe(true);
    expect(permissionService.hasPermission).toHaveBeenCalledWith(1, 'widget', 'read');
  });

  it('should return false for permission check when user is not logged in', async () => {
    authService.getUser.mockReturnValue(null);
    permissionService.getUserPermissions.mockResolvedValue([]);

    const { result } = renderHook(() => usePermissions());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const hasPermission = await result.current.hasPermission('widget', 'read');
    expect(hasPermission).toBe(false);
    expect(permissionService.hasPermission).not.toHaveBeenCalled();
  });

  it('should check role', async () => {
    const mockUser = { id: 1, username: 'testuser' };
    authService.getUser.mockReturnValue(mockUser);
    permissionService.getUserPermissions.mockResolvedValue([]);
    permissionService.hasRole.mockResolvedValue(true);

    const { result } = renderHook(() => usePermissions());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    const hasRole = await result.current.hasRole('admin');
    expect(hasRole).toBe(true);
    expect(permissionService.hasRole).toHaveBeenCalledWith(1, 'admin');
  });
});


