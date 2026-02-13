import apiClient from './apiClient';

export const sectorService = {
  getRotation: async () => {
    const response = await apiClient.get('/analytics/sector-rotation');
    return response.data;
  },

  getSignals: async () => {
    const response = await apiClient.get('/analytics/sector-rotation/signals');
    return response.data;
  },

  getPerformance: async () => {
    const response = await apiClient.get('/analytics/sectors/performance');
    return response.data;
  },

  getPhase: async () => {
    const response = await apiClient.get('/analytics/cycle/phase');
    return response.data;
  }
};
