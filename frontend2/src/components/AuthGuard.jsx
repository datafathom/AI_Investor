/**
 * Authentication Guard Component
 * 
 * Protects routes/components that require authentication.
 * Shows login modal if user is not authenticated.
 */

import React, { useEffect, useState } from 'react';
import { authService } from '../utils/authService';

export default function AuthGuard({ children, onShowLogin }) {
  const [isAuthenticated, setIsAuthenticated] = useState(authService.isAuthenticated());

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);
      
      if (!authenticated && onShowLogin) {
        onShowLogin();
      }
    };

    checkAuth();
    
    // Listen for storage changes (when login happens in another tab/window)
    const handleStorageChange = (e) => {
      if (e.key === 'widget_os_token' || e.key === 'widget_os_user') {
        checkAuth();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    // Also check periodically in case localStorage was updated in same window
    const interval = setInterval(checkAuth, 500);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      clearInterval(interval);
    };
  }, [onShowLogin]);

  if (!isAuthenticated) {
    return null; // Don't render children if not authenticated
  }

  return <>{children}</>;
}

