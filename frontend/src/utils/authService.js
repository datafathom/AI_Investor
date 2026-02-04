import apiClient from '../services/apiClient';
import { StorageService } from './storageService';

export const authService = {
    async register(email, password) {
        // apiClient autoconfigures base URL (e.g. /api/v1)
        const response = await apiClient.post('/auth/register', { email, password });
        return response.data;
    },

    async login(email, password) {
        // apiClient handles timeouts and errors
        try {
            const data = await apiClient.post('/auth/login', { email, password });
            
            // Save to StorageService (writes to IDB + LS + Memory)
            await StorageService.set('widget_os_token', data.token);
            await StorageService.set('widget_os_user', data.user);

            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    async logout() {
        await StorageService.remove('widget_os_token');
        await StorageService.remove('widget_os_user');
        await StorageService.remove('widget_os_tenant_id');
        // Optional: Call logout endpoint if exists
        // apiClient.post('/auth/logout').catch(() => {});
        window.location.href = '/';
    },

    setTenantId(tenantId) {
        StorageService.set('widget_os_tenant_id', tenantId);
    },

    getTenantId() {
        // Use sync for critical headers
        return StorageService.getSync('widget_os_tenant_id') || 'default';
    },

    _userCache: null,
    _lastUserRaw: null,

    getCurrentUser() {
        // Use sync get for immediate user availability
        const user = StorageService.getSync('widget_os_user');
        return user;
    },

    getToken() {
        return StorageService.getSync('widget_os_token');
    },

    isAuthenticated() {
        return !!this.getToken();
    },

    // Legacy helper kept for backward compatibility if any non-apiClient calls remain temporarily
    // Ideally this should be removed once full migration is complete
    getAuthHeaders() {
        const token = this.getToken();
        const tenantId = this.getTenantId();
        return {
            'Content-Type': 'application/json',
            'X-Tenant-ID': tenantId,
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    },

    setSession(token, user) {
        StorageService.set('widget_os_token', token);
        StorageService.set('widget_os_user', user);
    }
};

