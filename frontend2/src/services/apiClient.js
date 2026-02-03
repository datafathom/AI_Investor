/**
 * Centralized API Client
 * 
 * Standardized request/response handling, global error management, and auto-retries.
 * Uses Axios for robust HTTP capabilities.
 */

import axios from 'axios';
import { useStore } from '../store/store';
import useHardwareStore from '../stores/hardwareStore';
import hardwareService from './hardwareService';
import { StorageService } from '../utils/storageService';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5050/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// --- Caching Configuration ---
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes default
const cache = {
  get: async (key) => {
    const item = await StorageService.get(`api_cache_${key}`);
    if (!item) return null;
    
    // StorageService automatically parses JSON if it was stored as an object
    const { data, expiry } = item;
    if (Date.now() > expiry) {
      await StorageService.remove(`api_cache_${key}`);
      return null;
    }
    return data;
  },
  set: async (key, data, ttl = CACHE_TTL) => {
    const item = {
      data,
      expiry: Date.now() + ttl,
    };
    await StorageService.set(`api_cache_${key}`, item);
  }
};

// Request Interceptor
apiClient.interceptors.request.use(
  async (config) => {
    console.log(`[API Debug] Request to ${config.url} started`);
    // Check Cache for GET requests
    if (config.method === 'get' && config.useCache) {
      const cachedData = await cache.get(config.url + JSON.stringify(config.params || {}));
      if (cachedData) {
        config.adapter = () => Promise.resolve({
          data: cachedData,
          status: 200,
          statusText: 'OK',
          headers: {},
          config,
          request: {}
        });
      }
    }
    // Set global loading state
    const setLoading = useStore.getState().setLoading;
    setLoading(true);

    // Add Auth Token if available
    const token = await StorageService.get('widget_os_token') || 
                  await StorageService.get('token') || 
                  await StorageService.get('auth_token');

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    // Add Tenant ID
    const tenantId = await StorageService.get('widget_os_tenant_id');
    config.headers['X-Tenant-ID'] = tenantId || 'default';

    // Phase 6 / Sprint 6: Hardware Signature for high-value transactions (Multi-Sig)
    const HIGH_VALUE_THRESHOLD = 200000; // $200k threshold for hardware signature
    const sensitiveEndpoints = ['/withdraw', '/execute_large_trade', '/brokerage/trade'];
    const alwaysRequireHardware = ['/risk/kill-switch']; // Always require hardware for critical ops
    
    const isSensitive = sensitiveEndpoints.some(ep => config.url && config.url.includes(ep));
    const isAlwaysRequired = alwaysRequireHardware.some(ep => config.url && config.url.includes(ep));
    
    // Extract transaction amount from payload
    const transactionAmount = config.data?.amount || config.data?.value || config.data?.total || 0;
    const isHighValue = transactionAmount >= HIGH_VALUE_THRESHOLD;

    if ((isSensitive && isHighValue) || isAlwaysRequired) {
      if (config.method === 'post') {
        try {
          // Trigger the global hardware signature flow (modal + service call)
          const signature = await useHardwareStore.getState().requestSignature({
            ...config.data,
            endpoint: config.url,
            amount: transactionAmount
          });
          
          config.headers['X-Hardware-Signature'] = signature;
          console.log(`[API] Hardware signature attached (amount: $${transactionAmount})`);
        } catch (err) {
          setLoading(false);
          const errorMsg = isAlwaysRequired 
            ? 'Hardware signature required for this critical operation'
            : `Hardware signature required for transactions over $${HIGH_VALUE_THRESHOLD.toLocaleString()}`;
          return Promise.reject(new Error(errorMsg));
        }
      }
    }

    return config;
  },
  (error) => {
    const setLoading = useStore.getState().setLoading;
    setLoading(false);
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    const setLoading = useStore.getState().setLoading;
    setLoading(false);

    // Populate Cache for GET requests
    const config = response.config;
    if (config.method === 'get' && config.useCache) {
      // Async set, don't await
      cache.set(config.url + JSON.stringify(config.params || {}), response.data, config.cacheTTL);
    }

    return response.data;
  },
  async (error) => {
    const setLoading = useStore.getState().setLoading;
    setLoading(false);

    const originalRequest = error.config;

    // 401 Unauthorized - Redirect to login
    if (error.response?.status === 401 && !originalRequest._retry) {
      console.error(`[API] 401 Unauthorized for ${originalRequest.url}. Redirecting to login.`);
      
      // CRITICAL: Clear token to prevent infinite loops if the token is invalid/expired
      await StorageService.remove('widget_os_token');
      await StorageService.remove('widget_os_user');
      await StorageService.remove('widget_os_tenant_id');
      
      window.location.href = '/'; // Redirect to root, AuthGuard will handle showing the modal
      return Promise.reject(error);
    }

    // 429 Too Many Requests - Rate Limiting
    if (error.response?.status === 429) {
      console.error('Rate limit exceeded');
      // Could implement a wait and retry logic here if needed
      // For now, just notify user via global state if we had a notification service
      return Promise.reject(error);
    }

    // 5xx Server Errors - Simple Retry Logic
    if (error.response?.status >= 500 && !originalRequest._retry) {
      originalRequest._retry = true;
      console.warn('Server error, retrying request...', originalRequest.url);
      return apiClient(originalRequest);
    }

    return Promise.reject(error);
  }
);

if (process.env.NODE_ENV === 'development') {
  window.apiClient = apiClient;
}

export default apiClient;
