/**
 * API Client Utility
 * 
 * Centralized API client for making HTTP requests.
 * Handles authentication, error handling, and response formatting.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

class APIClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
    this.token = null;
  }

  /**
   * Set authentication token
   * @param {string} token - Authentication token
   */
  setToken(token) {
    this.token = token;
  }

  /**
   * Get authentication headers
   * @returns {Object} Headers object
   */
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
      'X-Tenant-ID': localStorage.getItem('widget_os_tenant_id') || 'default',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  /**
   * Make HTTP request
   * @param {string} endpoint - API endpoint
   * @param {Object} options - Request options
   * @returns {Promise<any>} Response data
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const error = await response.json().catch(() => ({
          message: `HTTP ${response.status}: ${response.statusText}`,
        }));
        throw new Error(error.message || `Request failed: ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }

      return await response.text();
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  }

  /**
   * GET request
   * @param {string} endpoint - API endpoint
   * @param {Object} params - Query parameters
   * @returns {Promise<any>} Response data
   */
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request(url, { method: 'GET' });
  }

  /**
   * POST request
   * @param {string} endpoint - API endpoint
   * @param {Object} data - Request body
   * @returns {Promise<any>} Response data
   */
  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * PUT request
   * @param {string} endpoint - API endpoint
   * @param {Object} data - Request body
   * @returns {Promise<any>} Response data
   */
  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * PATCH request
   * @param {string} endpoint - API endpoint
   * @param {Object} data - Request body
   * @returns {Promise<any>} Response data
   */
  async patch(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  /**
   * DELETE request
   * @param {string} endpoint - API endpoint
   * @returns {Promise<any>} Response data
   */
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Export singleton instance
export const apiClient = new APIClient();

// Export class for custom instances
export { APIClient };

