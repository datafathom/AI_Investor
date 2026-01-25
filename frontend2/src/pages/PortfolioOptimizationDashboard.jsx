/**
 * ==============================================================================
 * FILE: frontend2/src/pages/PortfolioOptimizationDashboard.jsx
 * ROLE: Portfolio Optimization & Rebalancing Dashboard
 * PURPOSE: Phase 2 - Portfolio Optimization & Automated Rebalancing
 *          Displays portfolio optimization results and rebalancing recommendations.
 * 
 * INTEGRATION POINTS:
 *    - OptimizationAPI: /api/v1/optimization endpoints
 *    - PortfolioStore: Portfolio data
 * 
 * FEATURES:
 *    - Portfolio optimization (MVO, Risk Parity, etc.)
 *    - Rebalancing recommendations
 *    - Rebalancing history
 *    - Optimization constraints
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PortfolioOptimizationDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const PortfolioOptimizationDashboard = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'results', x: 0, y: 0, w: 12, h: 6 },
      { i: 'recs', x: 0, y: 6, w: 6, h: 8 },
      { i: 'history', x: 6, y: 6, w: 6, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_optimization_dashboard';

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

  const [optimizationResult, setOptimizationResult] = useState(null);
  const [rebalancingRecs, setRebalancingRecs] = useState([]);
  const [rebalancingHistory, setRebalancingHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');
  const [optimizationType, setOptimizationType] = useState('mean_variance');

  useEffect(() => {
    loadRebalancingRecs();
    loadRebalancingHistory();
  }, []);

  const loadRebalancingRecs = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/optimization/rebalancing-recommendations`, {
        params: { portfolio_id: portfolioId }
      });
      setRebalancingRecs(res.data.data || []);
    } catch (error) {
      console.error('Error loading rebalancing recommendations:', error);
    }
  };

  const loadRebalancingHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/optimization/rebalancing-history`, {
        params: { portfolio_id: portfolioId }
      });
      setRebalancingHistory(res.data.data || []);
    } catch (error) {
      console.error('Error loading rebalancing history:', error);
    }
  };

  const runOptimization = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/optimization/optimize`, {
        portfolio_id: portfolioId,
        optimization_type: optimizationType,
        objective: 'maximize_sharpe',
        constraints: []
      });
      setOptimizationResult(res.data.data);
    } catch (error) {
      console.error('Error running optimization:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page portfolio-optimization-dashboard">
      <div className="dashboard-header">
        <h1>Portfolio Optimization & Rebalancing</h1>
        <p className="subtitle">Phase 2: Portfolio Optimization & Automated Rebalancing</p>
      </div>

      <div className="scrollable-content-wrapper">
        <div className="optimization-controls">
          <div className="form-group" style={{ minWidth: '300px' }}>
            <span className="form-label">Optimization Strategy</span>
            <select
              value={optimizationType}
              onChange={(e) => setOptimizationType(e.target.value)}
              className="form-input"
            >
              <option value="mean_variance">Mean-Variance Optimization</option>
              <option value="risk_parity">Risk Parity</option>
              <option value="minimum_variance">Minimum Variance</option>
              <option value="black_litterman">Black-Litterman</option>
            </select>
          </div>
          <button onClick={runOptimization} disabled={loading} className="optimize-button">
            {loading ? 'Optimizing...' : 'Run Optimization'}
          </button>
        </div>

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
          {/* Optimization Results */}
          <div key="results">
            {optimizationResult ? (
              <div className="optimization-card h-full">
                <h2>Optimization Results</h2>
                <div className="optimization-metrics">
                  <div className="metric">
                    <span className="label">Expected Return:</span>
                    <span className="value">{(optimizationResult.expected_return * 100).toFixed(2)}%</span>
                  </div>
                  <div className="metric">
                    <span className="label">Expected Risk:</span>
                    <span className="value">{(optimizationResult.expected_risk * 100).toFixed(2)}%</span>
                  </div>
                  <div className="metric">
                    <span className="label">Sharpe Ratio:</span>
                    <span className="value">{optimizationResult.sharpe_ratio?.toFixed(2)}</span>
                  </div>
                </div>
                <div className="allocations">
                  <h3>Optimal Allocations</h3>
                  {optimizationResult.allocations?.map((alloc, idx) => (
                    <div key={idx} className="allocation-item">
                      <span className="symbol">{alloc.symbol}</span>
                      <span className="allocation">{(alloc.allocation * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="optimization-card h-full flex items-center justify-center text-slate-500">
                 <h2>Optimization Results</h2>
                 <p>Run optimization to see results</p>
              </div>
            )}
          </div>

          {/* Rebalancing Recommendations */}
          <div key="recs" className="rebalancing-card">
            <h2>Rebalancing Recommendations</h2>
            {rebalancingRecs.length > 0 ? (
              <div className="recommendations-list">
                {rebalancingRecs.map((rec, idx) => (
                  <div key={idx} className="recommendation-item">
                    <div className="rec-header">
                      <span className="symbol">{rec.symbol}</span>
                      <span className={`action ${rec.action}`}>{rec.action}</span>
                    </div>
                    <div className="rec-details">
                      <span>Current: {(rec.current_allocation * 100).toFixed(1)}%</span>
                      <span>Target: {(rec.target_allocation * 100).toFixed(1)}%</span>
                      <span>Amount: ${rec.trade_amount?.toFixed(2)}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No rebalancing recommendations at this time</div>
            )}
          </div>

          {/* Rebalancing History */}
          <div key="history" className="history-card">
            <h2>Rebalancing History</h2>
            {rebalancingHistory.length > 0 ? (
              <div className="history-list">
                {rebalancingHistory.slice(0, 10).map((entry, idx) => (
                  <div key={idx} className="history-item">
                    <div className="history-date">
                      {new Date(entry.rebalancing_date).toLocaleDateString()}
                    </div>
                    <div className="history-status">{entry.status}</div>
                    <div className="history-trades">
                      {entry.trades_executed} trades executed
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No rebalancing history</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default PortfolioOptimizationDashboard;
