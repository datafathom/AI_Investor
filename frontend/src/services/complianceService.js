/**
 * Compliance Service (Phase 7)
 * Handles immutable record-keeping and wash-sale verification.
 */

import apiClient from './apiClient';

const complianceService = {
  /**
   * Check a transaction for compliance violations.
   */
  checkCompliance: async (userId, transaction) => {
    return apiClient.post('/compliance/check', { user_id: userId, transaction });
  },

  /**
   * Fetch the immutable audit trail from the RecordVault.
   */
  getAuditTrail: async (userId, limit = 50) => {
    return apiClient.get('/compliance/audit', { params: { user_id: userId, limit } });
  }
};

export default complianceService;
