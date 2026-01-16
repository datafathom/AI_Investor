/**
 * usePermissions Hook
 * 
 * React hook for permission checking.
 */

import { useState, useEffect } from 'react';
import permissionService from '../services/permissionService';
import { authService } from '../utils/authService';

export function usePermissions() {
  const [user, setUser] = useState(() => authService.getUser());
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPermissions = async () => {
      const currentUser = authService.getUser();
      if (!currentUser) {
        setPermissions([]);
        setLoading(false);
        return;
      }

      setUser(currentUser);
      try {
        const userPerms = await permissionService.getUserPermissions(currentUser.id);
        setPermissions(userPerms);
      } catch (error) {
        console.error('Failed to load permissions:', error);
        setPermissions([]);
      } finally {
        setLoading(false);
      }
    };

    loadPermissions();
  }, []);

  const hasPermission = async (resource, action) => {
    if (!user) return false;
    return permissionService.hasPermission(user.id, resource, action);
  };

  const hasRole = async (roleName) => {
    if (!user) return false;
    return permissionService.hasRole(user.id, roleName);
  };

  const hasAnyPermission = async (permissionList) => {
    if (!user) return false;
    return permissionService.hasAnyPermission(user.id, permissionList);
  };

  const hasAllPermissions = async (permissionList) => {
    if (!user) return false;
    return permissionService.hasAllPermissions(user.id, permissionList);
  };

  return {
    user,
    permissions,
    loading,
    hasPermission,
    hasRole,
    hasAnyPermission,
    hasAllPermissions,
  };
}

