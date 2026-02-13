import apiClient from './apiClient';

export const quantService = {
  runBacktest: async (strategy) => {
    const response = await apiClient.post('/quantitative/backtest', strategy);
    return response.data;
  },

  getBacktestResults: async (id) => {
    const response = await apiClient.get(`/quantitative/backtest/${id}`);
    return response.data;
  },

  runMonteCarlo: async (params) => {
    const response = await apiClient.post('/quantitative/monte-carlo', params);
    return response.data;
  }
};
