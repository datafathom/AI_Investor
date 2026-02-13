import apiClient from './apiClient';

export const analysisService = {
  getMetrics: async () => {
    const response = await apiClient.get('/analysis/metrics');
    return response.data;
  },

  runScan: async (criteria) => {
    const response = await apiClient.post('/analysis/scan', { criteria });
    return response.data;
  },

  getCompany: async (ticker) => {
    const response = await apiClient.get(`/analysis/companies/${ticker}`);
    return response.data;
  }
};
