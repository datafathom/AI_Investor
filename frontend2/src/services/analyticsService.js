/**
 * Analytics Service
 * Handles advanced portfolio analytics, risk decomposition, and optimization.
 */

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `/api/v1`; // Relative for proxy compatibility, or use Vite proxy

/**
 * Perform an authenticated fetch with standard error handling.
 */
async function authenticatedFetch(config) {
  const token = localStorage.getItem('token');
  const response = await fetch(`${config.url}`, {
    method: config.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...config.headers
    },
    body: config.body ? JSON.stringify(config.body) : undefined
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.message || `HTTP Error: ${response.status}`);
  }

  return response.json();
}

export const analyticsService = {
  /**
   * Get performance attribution for a portfolio.
   */
  async getPerformanceAttribution(portfolioId) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/analytics/performance-attribution?portfolio_id=${portfolioId}`
    });
    return data.data;
  },

  /**
   * Get risk decomposition for a portfolio.
   */
  async getRiskDecomposition(portfolioId) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/analytics/risk-decomposition?portfolio_id=${portfolioId}`
    });
    return data.data;
  },

  /**
   * Get portfolio optimization results.
   */
  async optimizePortfolio(params) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/optimization/optimize`,
      method: 'POST',
      body: params
    });
    return data.data;
  },

  /**
   * Get rebalancing recommendations.
   */
  async getRebalancingRecommendations(portfolioId) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/optimization/rebalancing-recommendations?portfolio_id=${portfolioId}`
    });
    return data.data;
  },

  /**
   * Get advance risk metrics (VaR, Sharpe, etc.)
   */
  async getRiskMetrics(portfolioId, confidenceLevel = 0.95) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/advanced-risk/risk-metrics?portfolio_id=${portfolioId}&confidence_level=${confidenceLevel}`
    });
    return data.data;
  },

  /**
   * Run stress test scenario.
   */
  async runStressTest(portfolioId, scenario) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/advanced-risk/stress-test`,
      method: 'POST',
      body: { portfolio_id: portfolioId, scenario }
    });
    return data.data;
  },

  /**
   * Run Monte Carlo simulation.
   */
  async runMonteCarlo(params) {
    const data = await authenticatedFetch({
        url: `${API_BASE}/advanced-risk/monte-carlo`,
        method: 'POST',
        body: params
    });
    return data.data;
  },

  /**
   * Get tax-loss harvesting candidates.
   */
  async getTaxHarvestCandidates(portfolioId) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/tax-optimization/harvest-candidates?portfolio_id=${portfolioId}`
    });
    return data.data;
  },

  /**
   * Get tax projection for a year.
   */
  async getTaxProjection(portfolioId, year) {
    const data = await authenticatedFetch({
      url: `${API_BASE}/tax-optimization/tax-projection?portfolio_id=${portfolioId}&tax_year=${year}`
    });
    return data.data;
  }
};
