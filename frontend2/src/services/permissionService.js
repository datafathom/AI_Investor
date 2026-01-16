/**
 * Permission Service
 * 
 * Handles permission checking and role-based access control.
 * Provides efficient permission checking with caching.
 */

class PermissionService {
  constructor() {
    this.permissionCache = new Map(); // userId -> Set of permissions
    this.roleCache = new Map(); // userId -> Set of roles
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    this.cacheTimestamps = new Map();
  }

  /**
   * Check if user has permission
   */
  async hasPermission(userId, resource, action) {
    const cacheKey = `${userId}:${resource}:${action}`;
    
    // Check cache first
    if (this.permissionCache.has(cacheKey)) {
      const cached = this.permissionCache.get(cacheKey);
      const timestamp = this.cacheTimestamps.get(cacheKey);
      if (Date.now() - timestamp < this.cacheTimeout) {
        return cached;
      }
    }

    // Fetch from API
    try {
      const response = await fetch(`/api/permissions/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, resource, action }),
      });

      if (!response.ok) {
        return false;
      }

      const { hasPermission } = await response.json();
      
      // Cache result
      this.permissionCache.set(cacheKey, hasPermission);
      this.cacheTimestamps.set(cacheKey, Date.now());
      
      return hasPermission;
    } catch (error) {
      console.error('Permission check failed:', error);
      return false;
    }
  }

  /**
   * Check if user has any of the specified permissions
   */
  async hasAnyPermission(userId, permissions) {
    for (const perm of permissions) {
      const [resource, action] = perm.split(':');
      if (await this.hasPermission(userId, resource, action)) {
        return true;
      }
    }
    return false;
  }

  /**
   * Check if user has all of the specified permissions
   */
  async hasAllPermissions(userId, permissions) {
    for (const perm of permissions) {
      const [resource, action] = perm.split(':');
      if (!(await this.hasPermission(userId, resource, action))) {
        return false;
      }
    }
    return true;
  }

  /**
   * Check if user has role
   */
  async hasRole(userId, roleName) {
    const cacheKey = `${userId}:role:${roleName}`;
    
    if (this.roleCache.has(cacheKey)) {
      const cached = this.roleCache.get(cacheKey);
      const timestamp = this.cacheTimestamps.get(cacheKey);
      if (Date.now() - timestamp < this.cacheTimeout) {
        return cached;
      }
    }

    try {
      const response = await fetch(`/api/users/${userId}/roles`);
      if (!response.ok) {
        return false;
      }

      const roles = await response.json();
      const hasRole = roles.some(r => r.name === roleName);
      
      this.roleCache.set(cacheKey, hasRole);
      this.cacheTimestamps.set(cacheKey, Date.now());
      
      return hasRole;
    } catch (error) {
      console.error('Role check failed:', error);
      return false;
    }
  }

  /**
   * Get all user permissions
   */
  async getUserPermissions(userId) {
    try {
      const response = await fetch(`/api/users/${userId}/permissions`);
      if (!response.ok) {
        return [];
      }

      const permissions = await response.json();
      return permissions;
    } catch (error) {
      console.error('Failed to get user permissions:', error);
      return [];
    }
  }

  /**
   * Clear cache for user
   */
  clearCache(userId) {
    const keysToDelete = [];
    this.permissionCache.forEach((_, key) => {
      if (key.startsWith(`${userId}:`)) {
        keysToDelete.push(key);
      }
    });
    keysToDelete.forEach(key => {
      this.permissionCache.delete(key);
      this.cacheTimestamps.delete(key);
    });
    this.roleCache.delete(`${userId}:role`);
  }

  /**
   * Clear all caches
   */
  clearAllCache() {
    this.permissionCache.clear();
    this.roleCache.clear();
    this.cacheTimestamps.clear();
  }
}

// Singleton instance
const permissionService = new PermissionService();

export default permissionService;

