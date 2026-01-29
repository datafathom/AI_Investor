/**
 * Wave APIs Frontend Service
 * Consolidates API calls for Wave-related dashboards (Phases 57-68)
 * 
 * This module provides typed service functions for:
 * - Philanthropy (ESG, Carbon, Donations)
 * - Estate (Trusts, Heartbeat)
 * - Scenario (What-If, Monte Carlo, Bank Run)
 * - Compliance (SAR, Audit)
 * - Corporate (Earnings, Actions)
 * - Margin (Status, Requirements)
 * - Backtest (Monte Carlo, Overfit Detection)
 */
import apiClient from './apiClient';

/**
 * Generic fetch wrapper with error handling
 * @param {string} endpoint - API endpoint path
 * @param {object} options - Request options
 * @returns {Promise<object>} - API response data
 */
async function apiCall(endpoint, options = {}) {
  const method = (options.method || 'GET').toUpperCase();
  const data = options.body ? JSON.parse(options.body) : undefined;

  switch (method) {
    case 'POST':
      return apiClient.post(endpoint, data, options);
    case 'PUT':
      return apiClient.put(endpoint, data, options);
    case 'PATCH':
      return apiClient.patch(endpoint, data, options);
    case 'DELETE':
      return apiClient.delete(endpoint, options);
    case 'GET':
    default:
      return apiClient.get(endpoint, options);
  }
}

// ============================================
// PHILANTHROPY SERVICE
// ============================================

export const philanthropyService = {
  /**
   * Get ESG scores for portfolio
   * @returns {Promise<object>} ESG score breakdown
   */
  getESGScores: () => apiCall('/philanthropy/esg'),

  /**
   * Get carbon footprint metrics
   * @returns {Promise<object>} Carbon offset data
   */
  getCarbonFootprint: () => apiCall('/philanthropy/carbon'),

  /**
   * Get donation history
   * @returns {Promise<object>} List of donations
   */
  getDonationHistory: () => apiCall('/philanthropy/history'),

  /**
   * Submit a new donation
   * @param {object} data - Donation details (charity_id, amount, etc.)
   * @returns {Promise<object>} Donation receipt
   */
  submitDonation: (data) => apiCall('/philanthropy/donate', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
};

// ============================================
// ESTATE SERVICE
// ============================================

export const estateService = {
  /**
   * Get estate heartbeat (trust health check)
   * @returns {Promise<object>} Trust status and beneficiary info
   */
  getHeartbeat: () => apiCall('/estate/heartbeat'),
};

// ============================================
// SCENARIO SERVICE
// ============================================

export const scenarioService = {
  /**
   * Run what-if simulation
   * @param {object} params - Simulation parameters (shock_type, magnitude, etc.)
   * @returns {Promise<object>} Projected portfolio impact
   */
  runSimulation: (params) => apiCall('/scenario/simulate', {
    method: 'POST',
    body: JSON.stringify(params),
  }),

  /**
   * Run refined Monte Carlo simulation
   * @param {object} params - Monte Carlo parameters
   * @returns {Promise<object>} Distribution of outcomes
   */
  runMonteCarlo: (params) => apiCall('/scenario/monte-carlo-refined', {
    method: 'POST',
    body: JSON.stringify(params),
  }),

  /**
   * Simulate bank run scenario
   * @returns {Promise<object>} Liquidity stress results
   */
  simulateBankRun: () => apiCall('/scenario/bank-run'),
};

// ============================================
// COMPLIANCE SERVICE
// ============================================

export const complianceService = {
  /**
   * Get compliance overview
   * @returns {Promise<object>} Compliance status summary
   */
  getOverview: () => apiCall('/compliance/overview'),

  /**
   * Get audit trail
   * @returns {Promise<object>} Recent compliance events
   */
  getAuditTrail: () => apiCall('/compliance/audit'),

  /**
   * Get SAR (Suspicious Activity Report) queue
   * @returns {Promise<object>} Pending SARs
   */
  getSARQueue: () => apiCall('/compliance/sar'),

  /**
   * Update SAR status
   * @param {string} sarId - SAR identifier
   * @param {string} status - New status (pending, reviewed, filed)
   * @returns {Promise<object>} Updated SAR
   */
  updateSARStatus: (sarId, status) => apiCall(`/compliance/sar/${sarId}/status`, {
    method: 'POST',
    body: JSON.stringify({ status }),
  }),

  /**
   * Verify compliance checklist
   * @returns {Promise<object>} Verification results
   */
  verifyCompliance: () => apiCall('/compliance/verify'),
};

// ============================================
// CORPORATE SERVICE
// ============================================

export const corporateService = {
  /**
   * Get upcoming earnings calendar
   * @returns {Promise<object>} Earnings events
   */
  getEarnings: () => apiCall('/corporate/earnings'),
};

// ============================================
// MARGIN SERVICE
// ============================================

export const marginService = {
  /**
   * Get margin status and requirements
   * @returns {Promise<object>} Margin health and cushion
   */
  getStatus: () => apiCall('/margin/status'),
};

// ============================================
// BACKTEST SERVICE
// ============================================

export const backtestService = {
  /**
   * Run Monte Carlo backtest
   * @param {object} params - Backtest parameters
   * @returns {Promise<object>} Backtest distribution results
   */
  runMonteCarlo: (params) => apiCall('/backtest/monte-carlo', {
    method: 'POST',
    body: JSON.stringify(params),
  }),

  /**
   * Check for overfitting in strategy
   * @param {object} params - Strategy parameters
   * @returns {Promise<object>} Overfit detection metrics
   */
  checkOverfit: (params) => apiCall('/backtest/overfit', {
    method: 'POST',
    body: JSON.stringify(params),
  }),
};

// ============================================
// SYSTEM SERVICE
// ============================================

export const systemService = {
  /**
   * Get system health status
   * @returns {Promise<object>} Health check results
   */
  getHealth: () => apiCall('/system/health'),

  /**
   * Get Kafka stats
   * @returns {Promise<object>} Kafka cluster metrics
   */
  getKafkaStats: () => apiCall('/system/kafka/stats'),
};

// ============================================
// MOBILE SERVICE
// ============================================

export const mobileService = {
  /**
   * Activate kill switch (emergency halt)
   * @returns {Promise<object>} Kill switch activation status
   */
  activateKillSwitch: () => apiCall('/mobile/kill-switch', { method: 'POST' }),
};

// ============================================
// INTEGRATIONS SERVICE
// ============================================

export const integrationsService = {
  /**
   * Get available connectors
   * @returns {Promise<object>} List of configured integrations
   */
  getConnectors: () => apiCall('/integrations/connectors'),
};

export default {
  philanthropyService,
  estateService,
  scenarioService,
  complianceService,
  corporateService,
  marginService,
  backtestService,
  systemService,
  mobileService,
  integrationsService,
};
