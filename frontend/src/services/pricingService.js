import apiClient from './apiClient';

export const pricingService = {
  getProbabilityCone: async (ticker, price, iv, days) => {
    const response = await apiClient.get(`/pricing/probability-cone/${ticker}`, { params: { price, iv, days } });
    return response.data;
  },

  getExpectedMove: async (ticker, price, iv, dte) => {
    const response = await apiClient.get(`/pricing/expected-move/${ticker}`, { params: { price, iv, dte } });
    return response.data;
  }
};
