/**
 * AuthService Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { authService } from '../../src/utils/authService';

// Mock fetch globally
global.fetch = vi.fn();

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    fetch.mockClear();
  });

  describe('register', () => {
    it('should register a new user successfully', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ message: 'User registered successfully' }),
      };
      fetch.mockResolvedValueOnce(mockResponse);

      const result = await authService.register('newuser', 'password123');

      expect(fetch).toHaveBeenCalledWith('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'newuser', password: 'password123' }),
      });
      expect(result).toEqual({ message: 'User registered successfully' });
    });

    it('should throw error on registration failure', async () => {
      const mockResponse = {
        ok: false,
        json: async () => ({ error: 'Username already exists' }),
      };
      fetch.mockResolvedValueOnce(mockResponse);

      await expect(authService.register('existinguser', 'password123')).rejects.toThrow(
        'Username already exists'
      );
    });
  });

  describe('login', () => {
    it('should login successfully and store token', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          token: 'test-token-123',
          user: { id: 1, username: 'testuser' },
        }),
      };
      fetch.mockResolvedValueOnce(mockResponse);

      const result = await authService.login('testuser', 'password123');

      expect(fetch).toHaveBeenCalledWith('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'testuser', password: 'password123' }),
      });

      expect(localStorage.setItem).toHaveBeenCalledWith('widget_os_token', 'test-token-123');
      expect(localStorage.setItem).toHaveBeenCalledWith(
        'widget_os_user',
        JSON.stringify({ id: 1, username: 'testuser' })
      );
      expect(result).toEqual({
        token: 'test-token-123',
        user: { id: 1, username: 'testuser' },
      });
    });

    it('should throw error on login failure', async () => {
      const mockResponse = {
        ok: false,
        json: async () => ({ error: 'Invalid credentials' }),
      };
      fetch.mockResolvedValueOnce(mockResponse);

      await expect(authService.login('testuser', 'wrongpass')).rejects.toThrow(
        'Invalid credentials'
      );
    });
  });

  describe('logout', () => {
    it('should remove token and user from localStorage', () => {
      localStorage.setItem('widget_os_token', 'test-token');
      localStorage.setItem('widget_os_user', JSON.stringify({ id: 1, username: 'testuser' }));

      authService.logout();

      expect(localStorage.removeItem).toHaveBeenCalledWith('widget_os_token');
      expect(localStorage.removeItem).toHaveBeenCalledWith('widget_os_user');
    });
  });

  describe('getCurrentUser', () => {
    it('should return current user from localStorage', () => {
      const user = { id: 1, username: 'testuser' };
      localStorage.setItem('widget_os_user', JSON.stringify(user));
      localStorage.getItem.mockReturnValueOnce(JSON.stringify(user));

      const result = authService.getCurrentUser();

      expect(result).toEqual(user);
    });

    it('should return null when no user in localStorage', () => {
      localStorage.getItem.mockReturnValueOnce(null);

      const result = authService.getCurrentUser();

      expect(result).toBeNull();
    });
  });

  describe('getToken', () => {
    it('should return token from localStorage', () => {
      localStorage.setItem('widget_os_token', 'test-token-123');
      localStorage.getItem.mockReturnValueOnce('test-token-123');

      const result = authService.getToken();

      expect(result).toBe('test-token-123');
    });

    it('should return null when no token in localStorage', () => {
      localStorage.getItem.mockReturnValueOnce(null);

      const result = authService.getToken();

      expect(result).toBeNull();
    });
  });

  describe('isAuthenticated', () => {
    it('should return true when token exists', () => {
      localStorage.setItem('widget_os_token', 'test-token');
      localStorage.getItem.mockReturnValueOnce('test-token');

      const result = authService.isAuthenticated();

      expect(result).toBe(true);
    });

    it('should return false when no token exists', () => {
      localStorage.getItem.mockReturnValueOnce(null);

      const result = authService.isAuthenticated();

      expect(result).toBe(false);
    });
  });

  describe('getAuthHeaders', () => {
    it('should return headers with token when authenticated', () => {
      localStorage.setItem('widget_os_token', 'test-token');
      localStorage.getItem.mockReturnValueOnce('test-token');

      const headers = authService.getAuthHeaders();

      expect(headers).toEqual({
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token',
      });
    });

    it('should return headers without token when not authenticated', () => {
      localStorage.getItem.mockReturnValueOnce(null);

      const headers = authService.getAuthHeaders();

      expect(headers).toEqual({
        'Content-Type': 'application/json',
      });
    });
  });

  describe('authenticatedFetch', () => {
    it('should add auth headers to fetch request', async () => {
      localStorage.setItem('widget_os_token', 'test-token');
      localStorage.getItem.mockReturnValueOnce('test-token');

      const mockResponse = {
        ok: true,
        status: 200,
        json: async () => ({ data: 'test' }),
      };
      fetch.mockResolvedValueOnce(mockResponse);

      const response = await authService.authenticatedFetch('/api/test');

      expect(fetch).toHaveBeenCalledWith('/api/test', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token',
        },
      });
      expect(response).toEqual(mockResponse);
    });

    it('should handle 401 by logging out and reloading', async () => {
      localStorage.setItem('widget_os_token', 'expired-token');
      localStorage.getItem.mockReturnValueOnce('expired-token');

      const mockResponse = {
        ok: false,
        status: 401,
      };
      fetch.mockResolvedValueOnce(mockResponse);

      // Mock window.location.reload
      const reloadSpy = vi.fn();
      Object.defineProperty(window, 'location', {
        value: { reload: reloadSpy },
        writable: true,
      });

      await expect(authService.authenticatedFetch('/api/test')).rejects.toThrow(
        'Session expired. Please log in again.'
      );

      expect(localStorage.removeItem).toHaveBeenCalledWith('widget_os_token');
      expect(localStorage.removeItem).toHaveBeenCalledWith('widget_os_user');
    });

    it('should merge custom headers with auth headers', async () => {
      localStorage.setItem('widget_os_token', 'test-token');
      localStorage.getItem.mockReturnValueOnce('test-token');

      const mockResponse = {
        ok: true,
        status: 200,
        json: async () => ({}),
      };
      fetch.mockResolvedValueOnce(mockResponse);

      await authService.authenticatedFetch('/api/test', {
        method: 'POST',
        headers: { 'X-Custom-Header': 'custom-value' },
        body: JSON.stringify({ data: 'test' }),
      });

      expect(fetch).toHaveBeenCalledWith('/api/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token',
          'X-Custom-Header': 'custom-value',
        },
        body: JSON.stringify({ data: 'test' }),
      });
    });
  });
});

