import apiClient from './apiClient';

const researchService = {
  getNotebooks: async () => {
    const response = await apiClient.get('/research/notebooks');
    return response.data;
  },

  createNotebook: async (name) => {
    const response = await apiClient.post('/research/notebooks', { name });
    return response.data;
  },

  getNotebook: async (id) => {
    const response = await apiClient.get(`/research/notebooks/${id}`);
    return response.data;
  },

  saveNotebook: async (id, notebook) => {
    const response = await apiClient.put(`/research/notebooks/${id}`, notebook);
    return response.data;
  },

  executeCell: async (id, code) => {
    const response = await apiClient.post(`/research/notebooks/${id}/execute`, { code });
    return response.data;
  },

  restartKernel: async (id) => {
    await apiClient.post(`/research/notebooks/${id}/restart`);
  }
};

export { researchService };
export default researchService;
