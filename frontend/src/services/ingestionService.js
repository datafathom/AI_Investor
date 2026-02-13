import apiClient from './apiClient';

export const ingestionService = {
  // Pipelines
  listPipelines: async () => {
    const response = await apiClient.get('/ingestion/pipelines');
    return response.data;
  },

  getPipeline: async (id) => {
    const response = await apiClient.get(`/ingestion/pipelines/${id}`);
    return response.data;
  },

  triggerPipeline: async (id) => {
    const response = await apiClient.post(`/ingestion/pipelines/${id}/trigger`);
    return response.data;
  },

  getPipelineRuns: async (id) => {
    const response = await apiClient.get(`/ingestion/pipelines/${id}/runs`);
    return response.data;
  },

  updatePipeline: async (id, config) => {
    const response = await apiClient.patch(`/ingestion/pipelines/${id}`, config);
    return response.data;
  },

  // Quality
  getQualitySummary: async () => {
    const response = await apiClient.get('/ingestion/quality/summary');
    return response.data;
  },

  listQualityIssues: async () => {
    const response = await apiClient.get('/ingestion/quality/issues');
    return response.data;
  },

  resolveIssue: async (id) => {
    const response = await apiClient.post(`/ingestion/quality/issues/${id}/resolve`);
    return response.data;
  }
};
