/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedPortfolioAnalytics.jsx
 * ROLE: Advanced Portfolio Analytics Dashboard
 * PURPOSE: Phase 1 - Portfolio Performance Attribution & Risk Decomposition
 *          Displays comprehensive portfolio analytics with performance attribution,
 *          risk decomposition, and holding contributions.
 * 
 * INTEGRATION POINTS:
 *    - AnalyticsAPI: /api/v1/analytics endpoints
 *    - PortfolioStore: Portfolio data
 *    - AnalyticsStore: Analytics state
 * 
 * FEATURES:
 *    - Performance attribution breakdown
 *    - Risk decomposition by factors
 *    - Holding contribution analysis
 *    - Factor exposure visualization
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdvancedPortfolioAnalytics.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const AdvancedPortfolioAnalytics = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'attribution', x: 0, y: 0, w: 6, h: 8 },
      { i: 'risk', x: 6, y: 0, w: 6, h: 8 },
      { i: 'contributions', x: 0, y: 8, w: 12, h: 6 }
    ]
  };
  const STORAGE_KEY = 'layout_advanced_analytics';

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

  const [attribution, setAttribution] = useState(null);
  const [riskDecomp, setRiskDecomp] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      // Load performance attribution
      const attrRes = await axios.get(`${API_BASE}/api/v1/analytics/performance-attribution`, {
        params: { portfolio_id: portfolioId }
      });
      setAttribution(attrRes.data.data);

      // Load risk decomposition
      const riskRes = await axios.get(`${API_BASE}/api/v1/analytics/risk-decomposition`, {
        params: { portfolio_id: portfolioId }
      });
      setRiskDecomp(riskRes.data.data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="advanced-portfolio-analytics">
        <div className="loading">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="full-bleed-page advanced-portfolio-analytics">
      <div className="analytics-header">
        <h1>Advanced Portfolio Analytics</h1>
        <p className="subtitle">Phase 1: Performance Attribution & Risk Decomposition</p>
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
          draggableHandle=".analytics-card h2"
          margin={[16, 16]}
        >
          {/* Performance Attribution */}
          <div key="attribution" className="analytics-card">
            <h2>Performance Attribution</h2>
            {attribution ? (
              <div className="attribution-details">
                <div className="metric">
                  <span className="label">Total Return:</span>
                  <span className="value">{attribution.total_return?.toFixed(2)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Benchmark Return:</span>
                  <span className="value">{attribution.benchmark_return?.toFixed(2)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Active Return:</span>
                  <span className="value">{attribution.active_return?.toFixed(2)}%</span>
                </div>
                <div className="breakdown">
                  <h3>Attribution Breakdown</h3>
                  {attribution.breakdown?.map((item, idx) => (
                    <div key={idx} className="breakdown-item">
                      <span>{item.factor}: {item.contribution?.toFixed(2)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="no-data">No attribution data available</div>
            )}
          </div>

          {/* Risk Decomposition */}
          <div key="risk" className="analytics-card">
            <h2>Risk Decomposition</h2>
            {riskDecomp ? (
              <div className="risk-details">
                <div className="metric">
                  <span className="label">Total Risk:</span>
                  <span className="value">{riskDecomp.total_risk?.toFixed(2)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Systematic Risk:</span>
                  <span className="value">{riskDecomp.systematic_risk?.toFixed(2)}%</span>
                </div>
                <div className="metric">
                  <span className="label">Idiosyncratic Risk:</span>
                  <span className="value">{riskDecomp.idiosyncratic_risk?.toFixed(2)}%</span>
                </div>
                <div className="breakdown">
                  <h3>Factor Exposures</h3>
                  {riskDecomp.factor_exposures?.map((factor, idx) => (
                    <div key={idx} className="breakdown-item">
                      <span>{factor.factor}: {factor.exposure?.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="no-data">No risk data available</div>
            )}
          </div>

          {/* Holding Contributions */}
          <div key="contributions" className="analytics-card">
            <h2>Holding Contributions</h2>
            {attribution?.holding_contributions ? (
              <div className="contributions-list">
                {attribution.holding_contributions.slice(0, 10).map((holding, idx) => (
                  <div key={idx} className="contribution-item">
                    <span className="symbol">{holding.symbol}</span>
                    <span className="contribution">{holding.contribution?.toFixed(2)}%</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No contribution data available</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer for scrolling within the grid wrapper */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default AdvancedPortfolioAnalytics;
