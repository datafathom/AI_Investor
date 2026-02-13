import apiClient from './apiClient';

export const webhookService = {
  getEvents: async () => {
    const response = await apiClient.get('/webhooks/events');
    return response.data;
  },

  getEvent: async (id) => {
    const response = await apiClient.get(`/webhooks/events/${id}`);
    return response.data;
  },

  // Helper to get the ingestion URL
  getIngestionUrl: (source) => {
    // In production this would be full URL, in dev it might be localhost
    const baseUrl = window.location.origin.replace('5173', '5050'); // Hack for dev port
    return `${baseUrl}/api/v1/webhooks/receiver/${source}`;
  }
};
