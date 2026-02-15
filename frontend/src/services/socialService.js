import apiClient from './apiClient';

const socialService = {
  // Sentiment
  getTopSentiment: async (limit = 10) => {
    const response = await apiClient.get('/social/sentiment/top', { params: { limit } });
    return response.data;
  },

  getTickerSentiment: async (ticker) => {
    const response = await apiClient.get(`/social/sentiment/${ticker}`);
    return response.data;
  },

  getSentimentHistory: async (ticker, days = 7) => {
    const response = await apiClient.get(`/social/sentiment/${ticker}/history`, { params: { days } });
    return response.data;
  },
  
  getCorrelation: async (ticker) => {
      const response = await apiClient.get(`/social/correlation/${ticker}`);
      return response.data;
  },

  // Trends
  getTrends: async () => {
    const response = await apiClient.get('/social/trends');
    return response.data;
  },

  getTrendDetails: async (topic) => {
    const response = await apiClient.get(`/social/trends/${topic}`);
    return response.data;
  }
};

export { socialService };
export default socialService;
