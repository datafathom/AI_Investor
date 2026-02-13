import apiClient from './apiClient';

export const agentService = {
  // Legacy
  invokeAgent: async (agentId, payload) => {
    const response = await apiClient.post(`/agents/${agentId}/invoke`, payload);
    return response.data;
  },

  // Fleet Management
  getFleetAgents: async (department) => {
    const response = await apiClient.get('/agents/fleet/all', { params: { department } });
    return response.data;
  },

  restartAgent: async (agentId) => {
    const response = await apiClient.post(`/agents/fleet/${agentId}/restart`);
    return response.data;
  },

  getHeartbeats: async () => {
    const response = await apiClient.get('/agents/heartbeats');
    return response.data;
  },

  getKillHistory: async () => {
    const response = await apiClient.get('/agents/rogue/kills');
    return response.data;
  },

  killAgent: async (agentId, reason) => {
    const response = await apiClient.post(`/agents/rogue/${agentId}/kill`, null, { params: { reason } });
    return response.data;
  },

  getAgentLogs: async (agentId) => {
    const response = await apiClient.get(`/agents/${agentId}/logs`);
    return response.data;
  }
};
