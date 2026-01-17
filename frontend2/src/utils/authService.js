const API_URL = '/api/auth';

export const authService = {
    async register(username, password) {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Registration failed');
        return data;
    },

    async login(username, password) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5s timeout

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Login failed');

            // Save to localStorage
            localStorage.setItem('widget_os_token', data.token);
            localStorage.setItem('widget_os_user', JSON.stringify(data.user));

            return data;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Login request timed out. Check backend connection.');
            }
            throw error;
        }
    },

    logout() {
        localStorage.removeItem('widget_os_token');
        localStorage.removeItem('widget_os_user');
        localStorage.removeItem('widget_os_tenant_id');
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

    // Helper to add auth headers to fetch requests
    getAuthHeaders() {
        const token = this.getToken();
        const tenantId = this.getTenantId();
        return {
            'Content-Type': 'application/json',
            'X-Tenant-ID': tenantId,
            ...(token && { 'Authorization': `Bearer ${token}` })
        };
    },

    // Wrapper for authenticated fetch requests
    async authenticatedFetch(url, options = {}) {
        const headers = {
            ...this.getAuthHeaders(),
            ...options.headers
        };

        const response = await fetch(url, {
            ...options,
            headers
        });

        // If unauthorized, clear auth and redirect to login
        if (response.status === 401) {
            this.logout();
            window.location.reload();
            throw new Error('Session expired. Please log in again.');
        }

        return response;
    }
};
