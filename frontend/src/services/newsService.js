import apiClient from './apiClient';

export const newsService = {
  // Articles
  getArticles: async (params = {}) => {
    const response = await apiClient.get('/news/articles', { params });
    return response.data;
  },

  getArticle: async (id) => {
    const response = await apiClient.get(`/news/articles/${id}`);
    return response.data;
  },

  getSources: async () => {
    const response = await apiClient.get('/news/sources');
    return response.data;
  },

  saveSearch: async (name, filters) => {
    const response = await apiClient.post('/news/saved-searches', { name, filters });
    return response.data;
  },

  getSavedSearches: async () => {
    const response = await apiClient.get('/news/saved-searches');
    return response.data;
  },

  // Rumors
  getRumors: async () => {
    const response = await apiClient.get('/news/rumors');
    return response.data;
  },

  voteRumor: async (id, type) => {
    const response = await apiClient.post(`/news/rumors/${id}/vote`, null, { params: { vote_type: type } });
    return response.data;
  },
  
  // WebSocket URL helper
  getStreamUrl: () => {
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const host = window.location.hostname;
    // Assume backend is on same host but port 5050 for dev, or same port for prod proxy
    // Using simple dev logic here matching other services
    const port = '5050'; 
    return `${proto}://${host}:${port}/api/v1/news/stream`;
  }
};
