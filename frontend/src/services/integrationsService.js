import apiClient from './apiClient';

export const integrationsService = {
  getConnectors: async () => {
    const response = await apiClient.get('/integrations/connectors');
    return response.data;
  },

  getAvailableIntegrations: async () => {
    const response = await apiClient.get('/integrations/available');
    return response.data;
  },

  getConnectedIntegrations: async (userId) => {
    const response = await apiClient.get('/integrations/connected', { params: { user_id: userId } });
    return response.data;
  },

  getSyncHistory: async (userId) => {
    const response = await apiClient.get('/integrations/sync-history', { params: { user_id: userId } });
    return response.data;
  },

  testConnector: async (id) => {
    const response = await apiClient.post(`/integrations/connectors/${id}/test`);
    return response.data;
  },

  getApiKeys: async () => {
    const response = await apiClient.get('/integrations/keys');
    return response.data;
  },

  createApiKey: async (label) => {
    const response = await apiClient.post('/integrations/keys', null, { params: { label } });
    return response.data;
  },

  getWebhooks: async () => {
    const response = await apiClient.get('/integrations/webhooks');
    return response.data;
  },

  addWebhook: async (url, events) => {
    const response = await apiClient.post('/integrations/webhooks', { url, events });
    return response.data;
  }
};
