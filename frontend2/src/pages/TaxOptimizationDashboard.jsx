/**
 * ==============================================================================
 * FILE: frontend2/src/pages/TaxOptimizationDashboard.jsx
 * ROLE: Tax Optimization Dashboard
 * PURPOSE: Phase 4 - Tax-Loss Harvesting & Optimization
 *          Displays tax-loss harvesting opportunities and optimization strategies.
 * 
 * INTEGRATION POINTS:
 *    - TaxOptimizationAPI: /api/v1/tax-optimization endpoints
 * 
 * FEATURES:
 *    - Tax-loss harvesting candidates
 *    - Wash-sale detection
 *    - Tax projections
 *    - Lot selection optimization
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TaxOptimizationDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const TaxOptimizationDashboard = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'projection', x: 0, y: 0, w: 12, h: 4 },
      { i: 'candidates', x: 0, y: 4, w: 12, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_tax_optimization_dashboard';

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

  const [harvestCandidates, setHarvestCandidates] = useState([]);
  const [taxProjection, setTaxProjection] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');
  const [selectedYear] = useState(new Date().getFullYear());

  useEffect(() => {
    loadHarvestCandidates();
    loadTaxProjection();
  }, []);

  const loadHarvestCandidates = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/tax-optimization/harvest-candidates`, {
        params: { portfolio_id: portfolioId }
      });
      setHarvestCandidates(res.data.data || []);
    } catch (error) {
      console.error('Error loading harvest candidates:', error);
    }
  };

  const loadTaxProjection = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/tax-optimization/tax-projection`, {
        params: { portfolio_id: portfolioId, tax_year: selectedYear }
      });
      setTaxProjection(res.data.data);
    } catch (error) {
      console.error('Error loading tax projection:', error);
    }
  };

  const checkWashSale = async (symbol) => {
    try {
      const res = await axios.post(`${API_BASE}/api/v1/tax-optimization/check-wash-sale`, {
        portfolio_id: portfolioId,
        symbol: symbol
      });
      alert(`Wash Sale Check: ${res.data.data.is_wash_sale ? 'WASH SALE DETECTED' : 'No wash sale'}`);
    } catch (error) {
      console.error('Error checking wash sale:', error);
    }
  };

  return (
    <div className="full-bleed-page tax-optimization-dashboard">
      <div className="dashboard-header">
        <h1>Tax Optimization & Harvesting</h1>
        <p className="subtitle">Phase 4: Tax-Loss Harvesting & Optimization</p>
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
          {/* Tax Projection */}
          <div key="projection" className="tax-projection-panel">
            <h2>Tax Projection ({selectedYear})</h2>
            {taxProjection ? (
              <div className="projection-metrics">
                <div className="projection-card">
                  <div className="projection-label">Estimated Capital Gains</div>
                  <div className="projection-value" style={{ color: '#ff8844' }}>
                    ${taxProjection.estimated_capital_gains?.toFixed(2)}
                  </div>
                </div>
                <div className="projection-card">
                  <div className="projection-label">Estimated Tax Liability</div>
                  <div className="projection-value" style={{ color: '#ff4444' }}>
                    ${taxProjection.estimated_tax_liability?.toFixed(2)}
                  </div>
                </div>
                <div className="projection-card">
                  <div className="projection-label">Realized Losses</div>
                  <div className="projection-value" style={{ color: '#00ff88' }}>
                    ${Math.abs(taxProjection.realized_losses || 0).toFixed(2)}
                  </div>
                </div>
                <div className="projection-card">
                  <div className="projection-label">Tax Savings Potential</div>
                  <div className="projection-value" style={{ color: '#00ff88' }}>
                    ${taxProjection.tax_savings_potential?.toFixed(2)}
                  </div>
                </div>
              </div>
            ) : (
              <div className="no-data">No tax projection available</div>
            )}
          </div>

          {/* Harvest Candidates */}
          <div key="candidates" className="harvest-candidates-panel">
            <h2>Tax-Loss Harvesting Candidates</h2>
            {harvestCandidates.length > 0 ? (
              <div className="candidates-list">
                {harvestCandidates.map((candidate, idx) => (
                  <div key={idx} className="candidate-card">
                    <div className="candidate-header">
                      <span className="symbol">{candidate.symbol}</span>
                      <span className="unrealized-loss" style={{ color: '#00ff88' }}>
                        ${Math.abs(candidate.unrealized_loss).toFixed(2)} loss
                      </span>
                    </div>
                    <div className="candidate-details">
                      <div className="detail-item">
                        <span className="label">Cost Basis:</span>
                        <span className="value">${candidate.cost_basis?.toFixed(2)}</span>
                      </div>
                      <div className="detail-item">
                        <span className="label">Current Value:</span>
                        <span className="value">${candidate.current_value?.toFixed(2)}</span>
                      </div>
                      <div className="detail-item">
                        <span className="label">Tax Benefit:</span>
                        <span className="value" style={{ color: '#00ff88' }}>
                          ${candidate.tax_benefit?.toFixed(2)}
                        </span>
                      </div>
                      {candidate.replacement_suggestion && (
                        <div className="replacement-suggestion">
                          <span className="label">Suggested Replacement:</span>
                          <span className="value">{candidate.replacement_suggestion}</span>
                        </div>
                      )}
                    </div>
                    <div className="candidate-actions">
                      <button
                        onClick={() => checkWashSale(candidate.symbol)}
                        className="check-button"
                      >
                        Check Wash Sale
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No harvest candidates at this time</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default TaxOptimizationDashboard;
