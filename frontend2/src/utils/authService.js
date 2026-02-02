import apiClient from '../services/apiClient';

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
            
            // Save to localStorage
            localStorage.setItem('widget_os_token', data.token);
            localStorage.setItem('widget_os_user', JSON.stringify(data.user));

            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    logout() {
        localStorage.removeItem('widget_os_token');
        localStorage.removeItem('widget_os_user');
        localStorage.removeItem('widget_os_tenant_id');
        // Optional: Call logout endpoint if exists
        // apiClient.post('/auth/logout').catch(() => {});
        window.location.href = '/login';
    },

    setTenantId(tenantId) {
        localStorage.setItem('widget_os_tenant_id', tenantId);
    },

    getTenantId() {
        return localStorage.getItem('widget_os_tenant_id') || 'default';
    },

    getCurrentUser() {
        const user = localStorage.getItem('widget_os_user');
        return user ? JSON.parse(user) : null;
    },

    getToken() {
        return localStorage.getItem('widget_os_token');
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
        localStorage.setItem('widget_os_token', token);
        localStorage.setItem('widget_os_user', JSON.stringify(user));
    }
};
