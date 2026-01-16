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
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Login failed');

        // Save to localStorage
        localStorage.setItem('widget_os_token', data.token);
        localStorage.setItem('widget_os_user', JSON.stringify(data.user));

        return data;
    },

    logout() {
        localStorage.removeItem('widget_os_token');
        localStorage.removeItem('widget_os_user');
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
        return {
            'Content-Type': 'application/json',
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
