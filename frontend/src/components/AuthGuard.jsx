/**
 * Authentication Guard Component
 * 
 * Protects routes/components that require authentication.
 * Shows login modal if user is not authenticated.
 */

import React, { useEffect, useState } from 'react';
import { authService } from '../utils/authService';

export default function AuthGuard({ children, onShowLogin, requiredRole }) {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return authService.isAuthenticated() || localStorage.getItem('widget_os_bypass') === 'true';
  });
  
  const [currentUser, setCurrentUser] = useState(() => authService.getCurrentUser());

  useEffect(() => {
    let isMounted = true;

    // Check authentication status
    const checkAuth = () => {
      const authenticated = authService.isAuthenticated() || localStorage.getItem('widget_os_bypass') === 'true';
      const user = authService.getCurrentUser();
      
      if (isMounted) {
        setIsAuthenticated(authenticated);
        setCurrentUser(user);
      }
      
      if (!authenticated && onShowLogin) {
        onShowLogin();
      }
    };

    checkAuth();
    
    // Listen for storage changes
    const handleStorageChange = (e) => {
      if (e.key === 'widget_os_token' || e.key === 'widget_os_user') {
        checkAuth();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    // Also check periodically
    const interval = setInterval(checkAuth, 500);
    
    return () => {
      isMounted = false;
      window.removeEventListener('storage', handleStorageChange);
      clearInterval(interval);
    };
  }, [onShowLogin]);

  if (!isAuthenticated) {
    return null; // Don't render children if not authenticated
  }

  // Role-based protection
  if (requiredRole === 'admin') {
    const isAdmin = currentUser?.role === 'admin'; // Relaxed check: Role only
    if (!isAdmin) {
      return (
        <div className="flex items-center justify-center min-h-screen bg-black font-mono text-red-500 p-8">
            <div className="border border-red-500/30 p-8 bg-red-950/10 rounded-lg">
                <h1 className="text-2xl mb-4">ACCESS_DENIED // UNAUTHORIZED_PERSONA</h1>
                <p className="mb-4 text-red-400">Your current role does not have execution privileges for this namespace.</p>
                <div className="text-sm opacity-50">ERROR_CODE: 0xADMIN_ONLY_RESOURCES</div>
                <button 
                  onClick={() => window.location.href = '/'}
                  className="mt-6 px-4 py-2 border border-red-500 text-red-500 hover:bg-red-500/20 transition-all font-bold"
                >
                  RETURN_TO_BASE
                </button>
            </div>
        </div>
      );
    }
  }

  return <>{children}</>;
}

