import apiClient from './apiClient';

export const debateService = {
  startDebate: async (ticker, context) => {
    return await apiClient.post('/debate/sessions', { ticker, context });
  },

  getSession: async (sessionId) => {
    return await apiClient.get(`/debate/sessions/${sessionId}`);
  },

  injectArgument: async (sessionId, argument, sentiment) => {
    return await apiClient.post(`/debate/sessions/${sessionId}/intervene`, { argument, sentiment });
  },
  
  getVerdict: async (sessionId) => {
    return await apiClient.get(`/debate/sessions/${sessionId}/verdict`);
  },

  getHistory: async (filters = {}) => {
    return await apiClient.get('/debate/history', { params: filters });
  },

  getTranscript: async (sessionId) => {
    return await apiClient.get(`/debate/history/${sessionId}/transcript`);
  }
};
