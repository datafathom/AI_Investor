import apiClient from './apiClient';

export const chartService = {
  getCandles: async (ticker, timeframe = '1day') => {
    const response = await apiClient.get(`/charting/candles/${ticker}`, { params: { timeframe } });
    return response.data;
  },

  getDrawings: async (chartId) => {
    const response = await apiClient.get(`/charting/drawings/${chartId}`);
    return response.data;
  },

  saveDrawings: async (chartId, drawings) => {
    const response = await apiClient.post(`/charting/drawings/${chartId}`, { drawings });
    return response.data;
  },

  getLayouts: async () => {
    const response = await apiClient.get('/charting/layouts');
    return response.data;
  },

  saveLayout: async (name, config) => {
    const response = await apiClient.post('/charting/layouts', { name, config });
    return response.data;
  },

  getMTFAnalysis: async (ticker) => {
    const response = await apiClient.get(`/charting/mtf/${ticker}`);
    return response.data;
  },

  getCorrelationHeatmap: async () => {
    const response = await apiClient.get('/charting/heatmaps/correlation');
    return response.data;
  },

  getSectorHeatmap: async () => {
    const response = await apiClient.get('/charting/heatmaps/sector');
    return response.data;
  },

  exportChart: async (format) => {
    const response = await apiClient.post('/charting/export', { format });
    return response.data;
  },

  shareChart: async () => {
    const response = await apiClient.post('/charting/share', {});
    return response.data;
  }
};
