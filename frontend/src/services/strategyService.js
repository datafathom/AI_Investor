/**
 * Strategy Service (Phase 4)
 * Handles Strategy building, validation, and execution lifecycle.
 */

import apiClient from './apiClient';

const strategyService = {
  /**
   * Create a new strategy.
   */
  createStrategy: async (userId, name, description, rules) => {
    return apiClient.post('/strategy/create', {
      user_id: userId,
      strategy_name: name,
      description,
      rules
    });
  },

  /**
   * Get all strategies for a user.
   */
  getStrategies: async (userId) => {
    return apiClient.get('/strategy/strategies', { params: { user_id: userId } });
  },

  /**
   * Start strategy execution.
   */
  startStrategy: async (strategyId, portfolioId) => {
    return apiClient.post(`/strategy/${strategyId}/start`, { portfolio_id: portfolioId });
  },

  /**
   * Stop strategy execution.
   */
  stopStrategy: async (strategyId) => {
    return apiClient.post(`/strategy/${strategyId}/stop`);
  },

  /**
   * Get strategy performance.
   */
  getPerformance: async (strategyId) => {
    return apiClient.get(`/strategy/${strategyId}/performance`);
  }
};

export default strategyService;
