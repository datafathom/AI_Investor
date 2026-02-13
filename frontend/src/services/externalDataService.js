import apiClient from './apiClient';

export const externalDataService = {
  getSources: async () => {
    const response = await apiClient.get('/external-data/sources');
    return response.data;
  },

  toggleSource: async (id) => {
    const response = await apiClient.post(`/external-data/sources/${id}/toggle`);
    return response.data;
  },

  getStats: async () => {
    const response = await apiClient.get('/external-data/stats');
    return response.data;
  }
};
