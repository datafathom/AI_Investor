/**
 * Admin & Inbox Service (Phase 8)
 * Handles Zero-Noise email triage and administrative workflow.
 */

import apiClient from './apiClient';

const adminService = {
  /**
   * Request LLM triage for an email snippet.
   */
  triageEmail: async (subject, sender, body) => {
    return apiClient.post('/communication/inbox/triage', { subject, sender, body });
  },

  /**
   * Report device location for geofencing.
   */
  reportLocation: async (deviceId, lat, lon) => {
    return apiClient.post('/system/security/heartbeat', { device_id: deviceId, lat, lon });
  },

  /**
   * Check geofence status.
   */
  getSecurityStatus: async (primaryId, mobileId) => {
    return apiClient.get('/system/security/status', {
      params: { primary_device: primaryId, trusted_mobile: mobileId }
    });
  }
};

export default adminService;
