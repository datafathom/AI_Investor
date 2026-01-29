/**
 * API Store - Zustand State Management for API Marketplace
 * Phase 66: Manages data connectors, API keys, and webhooks.
 */
import { create } from 'zustand';

const useAPIStore = create((set, get) => ({
    // State
    connectors: [],
    apiKeys: [],
    webhooks: [],
    providerHealth: {},
    rateLimits: {},
    error: null,
    
    // Actions
    setConnectors: (connectors) => set({ connectors }),
    addConnector: (connector) => set((s) => ({ connectors: [...s.connectors, connector] })),
    removeConnector: (id) => set((s) => ({ connectors: s.connectors.filter(c => c.id !== id) })),
    setApiKeys: (keys) => set({ apiKeys: keys }),
    addApiKey: (key) => set((s) => ({ apiKeys: [...s.apiKeys, key] })),
    revokeApiKey: (id) => set((s) => ({ apiKeys: s.apiKeys.filter(k => k.id !== id) })),
    setWebhooks: (webhooks) => set({ webhooks }),
    addWebhook: (webhook) => set((s) => ({ webhooks: [...s.webhooks, webhook] })),
    removeWebhook: (id) => set((s) => ({ webhooks: s.webhooks.filter(w => w.id !== id) })),
    setProviderHealth: (provider, health) => set((s) => ({ providerHealth: { ...s.providerHealth, [provider]: health } })),
    setRateLimits: (limits) => set({ rateLimits: limits }),
    setError: (error) => set({ error }),
    
    // Async: Fetch connectors
    fetchConnectors: async () => {
        try {
            const response = await fetch('/api/v1/integrations/connectors');
            const data = await response.json();
            set({ connectors: data || [] });
        } catch (error) {
            console.error('Fetch connectors failed:', error);
        }
    },
    
    // Async: Fetch webhooks
    fetchWebhooks: async () => {
        try {
            const response = await fetch('/api/v1/integrations/webhooks');
            const data = await response.json();
            set({ webhooks: data || [] });
        } catch (error) {
            console.error('Fetch webhooks failed:', error);
        }
    },

    // Async: Test connector
    testConnector: async (connectorId) => {
        try {
            const response = await fetch(`/api/v1/integrations/connectors/${connectorId}/test`, { method: 'POST' });
            return await response.json();
        } catch (error) {
            console.error('Test connector failed:', error);
            throw error;
        }
    },

    // Async: Test webhook
    testWebhook: async (webhookId) => {
        try {
            // Assuming endpoint for testing a specific webhook
            const response = await fetch(`/api/v1/integrations/webhooks/${webhookId}/test`, { method: 'POST' });
            return await response.json();
        } catch (error) {
            console.error('Test webhook failed:', error);
            throw error;
        }
    },
    
    reset: () => set({
        connectors: [], apiKeys: [], webhooks: [], providerHealth: {}, rateLimits: {}, error: null
    })
}));

export default useAPIStore;
