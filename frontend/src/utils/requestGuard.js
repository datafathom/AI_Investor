/**
 * RequestGuard.js
 * 
 * Enforces centralized API usage by intercepting and rejecting direct 
 * native fetch() and XMLHttpRequest calls that don't originate from authorized services.
 */

const AUTHORIZED_CLIENTS = ['apiClient.js', 'socket.io-client', 'vite'];
const IS_DEV = import.meta.env.DEV;

export const initRequestGuard = () => {
  if (!IS_DEV) return; // Only enforce in development to help devs maintain patterns

  console.log('[RequestGuard] Initialized. Direct fetch/XHR is restricted.');

  // 1. Intercept fetch
  const originalFetch = window.fetch;
  window.fetch = function(input, init) {
    const stack = new Error().stack;
    const isAuthorized = AUTHORIZED_CLIENTS.some(client => stack && stack.includes(client));

    if (!isAuthorized) {
      const url = typeof input === 'string' ? input : input.url;
      console.error(`[RequestGuard] BLOCKED direct fetch to: ${url}`);
      console.warn('[RequestGuard] Please use "apiClient" from "@services/apiClient" instead.');
      return Promise.reject(new Error(`Direct fetch to ${url} is blocked by RequestGuard.`));
    }

    return originalFetch.apply(this, arguments);
  };

  // 2. Intercept XMLHttpRequest
  const originalOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(method, url) {
    const stack = new Error().stack;
    const isAuthorized = AUTHORIZED_CLIENTS.some(client => stack && stack.includes(client));

    if (!isAuthorized) {
      console.error(`[RequestGuard] BLOCKED direct XHR to: ${url}`);
      console.warn('[RequestGuard] Please use "apiClient" from "@services/apiClient" instead.');
      this.send = () => {
         throw new Error(`Direct XHR to ${url} is blocked by RequestGuard.`);
      };
    }

    return originalOpen.apply(this, arguments);
  };
};
