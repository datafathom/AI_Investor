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
    const response = await apiClient.get(`/analytics/performance-attribution`, {
      params: { portfolio_id: portfolioId }
    });
    return response.data;
  },

  /**
   * Get risk decomposition for a portfolio.
   */
  async getRiskDecomposition(portfolioId) {
    const response = await apiClient.get(`/analytics/risk-decomposition`, {
      params: { portfolio_id: portfolioId }
    });
    return response.data;
  },

  /**
   * Get portfolio optimization results.
   */
  async optimizePortfolio(params) {
    const response = await apiClient.post(`/optimization/optimize`, params);
    return response.data;
  },

  /**
   * Get rebalancing recommendations.
   */
  async getRebalancingRecommendations(portfolioId) {
    const response = await apiClient.get(`/optimization/rebalancing-recommendations`, {
      params: { portfolio_id: portfolioId }
    });
    return response.data;
  },

  /**
   * Get advance risk metrics (VaR, Sharpe, etc.)
   */
  async getRiskMetrics(portfolioId, confidenceLevel = 0.95) {
    const response = await apiClient.get(`/advanced-risk/risk-metrics`, {
      params: { portfolio_id: portfolioId, confidence_level: confidenceLevel }
    });
    return response.data;
  },

  /**
   * Run stress test scenario.
   */
  async runStressTest(portfolioId, scenario) {
    const response = await apiClient.post(`/advanced-risk/stress-test`, { 
      portfolio_id: portfolioId, 
      scenario 
    });
    return response.data;
  },

  /**
   * Run Monte Carlo simulation.
   */
  async runMonteCarlo(params) {
    const response = await apiClient.post(`/advanced-risk/monte-carlo`, params);
    return response.data;
  },

  /**
   * Get tax-loss harvesting candidates.
   */
  async getTaxHarvestCandidates(portfolioId) {
    const response = await apiClient.get(`/tax-optimization/harvest-candidates`, {
      params: { portfolio_id: portfolioId }
    });
    return response.data;
  },

  /**
   * Get tax projection for a year.
   */
  async getTaxProjection(portfolioId, year) {
    const response = await apiClient.get(`/tax-optimization/tax-projection`, {
      params: { portfolio_id: portfolioId, tax_year: year }
    });
    return response.data;
  }
};
