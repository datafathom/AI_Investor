/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedRiskDashboard.jsx
 * ROLE: Advanced Risk Management Dashboard
 * PURPOSE: Phase 3 - Advanced Risk Management & Stress Testing
 *          Displays risk metrics, stress test results, and Monte Carlo simulations.
 * 
 * INTEGRATION POINTS:
 *    - AdvancedRiskAPI: /api/v1/advanced-risk endpoints
 * 
 * FEATURES:
 *    - VaR and CVaR calculations
 *    - Stress testing scenarios
 *    - Monte Carlo simulations
 *    - Risk-adjusted ratios
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdvancedRiskDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const AdvancedRiskDashboard = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'metrics', x: 0, y: 0, w: 12, h: 6 },
      { i: 'stress', x: 0, y: 6, w: 6, h: 8 },
      { i: 'monte_carlo', x: 6, y: 6, w: 6, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_advanced_risk_dashboard';

  const [layouts, setLayouts] = useState(() => {
     try {
         const saved = localStorage.getItem(STORAGE_KEY);
         return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
     } catch (e) {
         return DEFAULT_LAYOUT;
     }
  });

  const onLayoutChange = (currentLayout, allLayouts) => {
      setLayouts(allLayouts);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
  };

  const [riskMetrics, setRiskMetrics] = useState(null);
  const [stressTestResult, setStressTestResult] = useState(null);
  const [monteCarloResult, setMonteCarloResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');
  const [selectedScenario, setSelectedScenario] = useState('market_crash_2008');

  useEffect(() => {
    loadRiskMetrics();
  }, []);

  const loadRiskMetrics = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/api/v1/advanced-risk/risk-metrics`, {
        params: { portfolio_id: portfolioId, confidence_level: 0.95 }
      });
      setRiskMetrics(res.data.data);
    } catch (error) {
      console.error('Error loading risk metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  const runStressTest = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/advanced-risk/stress-test`, {
        portfolio_id: portfolioId,
        scenario: selectedScenario
      });
      setStressTestResult(res.data.data);
    } catch (error) {
      console.error('Error running stress test:', error);
    } finally {
      setLoading(false);
    }
  };

  const runMonteCarlo = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/advanced-risk/monte-carlo`, {
        portfolio_id: portfolioId,
        simulations: 10000,
        time_horizon_days: 30
      });
      setMonteCarloResult(res.data.data);
    } catch (error) {
      console.error('Error running Monte Carlo:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page advanced-risk-dashboard">
      <div className="dashboard-header">
        <h1>Advanced Risk Management</h1>
        <p className="subtitle">Phase 3: Advanced Risk Management & Stress Testing</p>
      </div>

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          onLayoutChange={onLayoutChange}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          isDraggable={true}
          isResizable={true}
          draggableHandle="h2"
          margin={[16, 16]}
        >
          {/* ... (widgets remain the same) ... */}
          <div key="metrics" className="risk-metrics-panel">
            <h2>Risk Metrics</h2>
            {loading && !riskMetrics ? (
              <div className="loading">Loading risk metrics...</div>
            ) : riskMetrics ? (
              <div className="metrics-grid">
                <div className="metric-card">
                  <div className="metric-label">Value at Risk (VaR)</div>
                  <div className="metric-value" style={{ color: '#ff4444' }}>
                    ${Math.abs(riskMetrics.var?.toFixed(2))}
                  </div>
                  <div className="metric-subtitle">95% Confidence</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Conditional VaR (CVaR)</div>
                  <div className="metric-value" style={{ color: '#ff8844' }}>
                    ${Math.abs(riskMetrics.cvar?.toFixed(2))}
                  </div>
                  <div className="metric-subtitle">Expected Tail Loss</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Maximum Drawdown</div>
                  <div className="metric-value" style={{ color: '#ff4444' }}>
                    {(riskMetrics.max_drawdown * 100).toFixed(2)}%
                  </div>
                  <div className="metric-subtitle">Peak to Trough</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Sharpe Ratio</div>
                  <div className="metric-value" style={{ color: '#00ff88' }}>
                    {riskMetrics.sharpe_ratio?.toFixed(2)}
                  </div>
                  <div className="metric-subtitle">Risk-Adjusted Return</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Sortino Ratio</div>
                  <div className="metric-value" style={{ color: '#00ff88' }}>
                    {riskMetrics.sortino_ratio?.toFixed(2)}
                  </div>
                  <div className="metric-subtitle">Downside Risk Adjusted</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Calmar Ratio</div>
                  <div className="metric-value" style={{ color: '#00ff88' }}>
                    {riskMetrics.calmar_ratio?.toFixed(2)}
                  </div>
                  <div className="metric-subtitle">Return / Max Drawdown</div>
                </div>
              </div>
            ) : (
              <div className="no-data">No risk metrics available</div>
            )}
          </div>

          <div key="stress" className="stress-test-panel">
            <h2>Stress Testing</h2>
            <div className="stress-controls">
              <select
                value={selectedScenario}
                onChange={(e) => setSelectedScenario(e.target.value)}
                className="scenario-select"
              >
                <option value="market_crash_2008">2008 Financial Crisis</option>
                <option value="covid_2020">2020 COVID-19 Crash</option>
                <option value="inflation_2022">2022 Inflation Spike</option>
                <option value="sector_shock_tech">Tech Sector Shock</option>
              </select>
              <button onClick={runStressTest} disabled={loading} className="run-button">
                Run Stress Test
              </button>
            </div>
            {stressTestResult && (
              <div className="stress-results">
                <div className="stress-metric">
                  <span className="label">Portfolio Impact:</span>
                  <span className="value" style={{ color: stressTestResult.portfolio_impact < 0 ? '#ff4444' : '#00ff88' }}>
                    {(stressTestResult.portfolio_impact * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="stress-metric">
                  <span className="label">Value Loss:</span>
                  <span className="value" style={{ color: '#ff4444' }}>
                    ${Math.abs(stressTestResult.value_loss?.toFixed(2))}
                  </span>
                </div>
                <div className="scenario-details">
                  <h3>Scenario Details</h3>
                  {stressTestResult.scenario_impacts?.map((impact, idx) => (
                    <div key={idx} className="impact-item">
                      <span>{impact.symbol}: {(impact.impact * 100).toFixed(2)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div key="monte_carlo" className="monte-carlo-panel">
            <h2>Monte Carlo Simulation</h2>
            <button onClick={runMonteCarlo} disabled={loading} className="run-button">
              Run Simulation
            </button>
            {monteCarloResult && (
              <div className="monte-carlo-results">
                <div className="simulation-metric">
                  <span className="label">Expected Value:</span>
                  <span className="value">${monteCarloResult.expected_value?.toFixed(2)}</span>
                </div>
                <div className="simulation-metric">
                  <span className="label">5th Percentile:</span>
                  <span className="value" style={{ color: '#ff4444' }}>
                    ${monteCarloResult.percentile_5?.toFixed(2)}
                  </span>
                </div>
                <div className="simulation-metric">
                  <span className="label">95th Percentile:</span>
                  <span className="value" style={{ color: '#00ff88' }}>
                    ${monteCarloResult.percentile_95?.toFixed(2)}
                  </span>
                </div>
                <div className="simulation-metric">
                  <span className="label">Probability of Loss:</span>
                  <span className="value">
                    {(monteCarloResult.probability_of_loss * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};;

export default AdvancedRiskDashboard;
