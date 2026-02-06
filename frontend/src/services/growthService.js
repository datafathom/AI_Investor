/**
 * Growth Service (Phase 8)
 * Handles Venture deal modeling and Cap-Table analysis.
 */

import apiClient from './apiClient';

const growthService = {
  /**
   * Calculate exit proceeds (Waterfall).
   */
  calculateWaterfall: async (exitValue, commonShares, capTable) => {
    return apiClient.post('/growth/waterfall', {
      exit_value: exitValue,
      common_shares: commonShares,
      cap_table: capTable
    });
  },

  /**
   * Fetch conglomerate growth metrics.
   */
  getMetrics: async () => {
    return apiClient.get('/growth/metrics');
  }
};

export default growthService;
