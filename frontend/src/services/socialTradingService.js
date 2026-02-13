import apiClient from './apiClient';

export const socialTradingService = {
  getFeed: async (limit = 20) => {
    const response = await apiClient.get('/social-trading/feed', { params: { limit } });
    return response.data;
  },

  getInfluencers: async () => {
    const response = await apiClient.get('/social-trading/influencers');
    return response.data;
  },

  toggleFollow: async (id) => {
    const response = await apiClient.post(`/social-trading/influencers/${id}/follow`);
    return response.data;
  }
};
