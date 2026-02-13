import apiClient from './apiClient';

export const factorService = {
  getFactors: async () => {
    const response = await apiClient.get('/quantitative/factors');
    return response.data;
  },

  getFactorReturns: async (days = 30) => {
    const response = await apiClient.get('/quantitative/factors/returns', { params: { days } });
    return response.data;
  },

  getExposure: async (ticker) => {
    const response = await apiClient.get(`/quantitative/factors/exposure/${ticker}`);
    return response.data;
  },

  analyzePortfolio: async (holdings) => {
    const response = await apiClient.post('/quantitative/factors/portfolio', { holdings });
    return response.data;
  }
};
