/**
 * Analytics Service
 * Handles advanced portfolio analytics, risk decomposition, and optimization.
 */

import apiClient from './apiClient';

export const analyticsService = {
  /**
   * Get performance attribution for a portfolio.
   */
  async getPerformanceAttribution(portfolioId) {
    return await apiClient.get(`/analytics/performance-attribution`, {
      params: { portfolio_id: portfolioId }
    });
  },

  /**
   * Get risk decomposition for a portfolio.
   */
  async getRiskDecomposition(portfolioId) {
    return await apiClient.get(`/analytics/risk-decomposition`, {
      params: { portfolio_id: portfolioId }
    });
  },

  /**
   * Get portfolio optimization results.
   */
  async optimizePortfolio(params) {
    return await apiClient.post(`/optimization/optimize`, params);
  },

  /**
   * Get rebalancing recommendations.
   */
  async getRebalancingRecommendations(portfolioId) {
    return await apiClient.get(`/optimization/rebalancing-recommendations`, {
      params: { portfolio_id: portfolioId }
    });
  },

  /**
   * Get advance risk metrics (VaR, Sharpe, etc.)
   */
  async getRiskMetrics(portfolioId, confidenceLevel = 0.95) {
    return await apiClient.get(`/advanced-risk/risk-metrics`, {
      params: { portfolio_id: portfolioId, confidence_level: confidenceLevel }
    });
  },

  /**
   * Run stress test scenario.
   */
  async runStressTest(portfolioId, scenario) {
    return await apiClient.post(`/advanced-risk/stress-test`, { 
      portfolio_id: portfolioId, 
      scenario 
    });
  },

  /**
   * Run Monte Carlo simulation.
   */
  async runMonteCarlo(params) {
    return await apiClient.post(`/advanced-risk/monte-carlo`, params);
  },

  /**
   * Get tax-loss harvesting candidates.
   */
  async getTaxHarvestCandidates(portfolioId) {
    return await apiClient.get(`/tax-optimization/harvest-candidates`, {
      params: { portfolio_id: portfolioId }
    });
  },

  /**
   * Get tax projection for a year.
   */
  async getTaxProjection(portfolioId, year) {
    return await apiClient.get(`/tax-optimization/tax-projection`, {
      params: { portfolio_id: portfolioId, tax_year: year }
    });
  }
};
