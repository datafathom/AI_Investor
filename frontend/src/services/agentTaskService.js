import apiClient from './apiClient';

export const agentTaskService = {
  getTasks: async (status) => {
    const response = await apiClient.get('/tasks/status', { params: { status } });
    return response.data.jobs;
  },

  submitTask: async (taskData) => {
    const response = await apiClient.post('/tasks/run', taskData);
    return response.data;
  },

  cancelTask: async (taskId) => {
    const response = await apiClient.post(`/tasks/kill/${taskId}`);
    return response.data;
  },

  retryTask: async (taskId) => {
    const response = await apiClient.post(`/tasks/${taskId}/retry`);
    return response.data;
  }
};
