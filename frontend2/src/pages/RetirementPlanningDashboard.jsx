/**
 * ==============================================================================
 * FILE: frontend2/src/pages/RetirementPlanningDashboard.jsx
 * ROLE: Retirement Planning Dashboard
 * PURPOSE: Phase 8 - Retirement Planning & Projection
 *          Displays retirement projections, withdrawal strategies, and Social Security optimization.
 * 
 * INTEGRATION POINTS:
 *    - RetirementAPI: /api/v1/retirement endpoints
 * 
 * FEATURES:
 *    - Retirement projections (Monte Carlo)
 *    - Withdrawal strategy optimization
 *    - Social Security timing
 *    - RMD calculations
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RetirementPlanningDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const RetirementPlanningDashboard = () => {
  const [projection, setProjection] = useState(null);
  const [withdrawalStrategy, setWithdrawalStrategy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [projectionParams, setProjectionParams] = useState({
    current_age: 35,
    retirement_age: 65,
    current_savings: 100000,
    monthly_contribution: 1000,
    expected_return: 0.07
  });

  useEffect(() => {
    loadWithdrawalStrategy();
  }, []);

  const loadWithdrawalStrategy = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/retirement/withdrawal-strategy`, {
        params: { user_id: userId }
      });
      setWithdrawalStrategy(res.data.data);
    } catch (error) {
      console.error('Error loading withdrawal strategy:', error);
    }
  };

  const runProjection = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/retirement/projection`, {
        user_id: userId,
        current_age: projectionParams.current_age,
        retirement_age: projectionParams.retirement_age,
        current_savings: projectionParams.current_savings,
        monthly_contribution: projectionParams.monthly_contribution,
        expected_return: projectionParams.expected_return
      });
      setProjection(res.data.data);
    } catch (error) {
      console.error('Error running projection:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page retirement-planning-dashboard">
      <div className="dashboard-header">
        <h1>Retirement Planning</h1>
        <p className="subtitle">Phase 8: Retirement Planning & Projection</p>
      </div>

      <div className="scrollable-content-wrapper">
        <div className="dashboard-content">
          {/* Projection Parameters */}
          <div className="parameters-panel">
            <h2>Retirement Projection Parameters</h2>
            <div className="params-grid">
              <div className="form-group">
                <span className="form-label">Current Age</span>
                <input
                  type="number"
                  value={projectionParams.current_age}
                  onChange={(e) => setProjectionParams({ ...projectionParams, current_age: parseInt(e.target.value) })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Retirement Age</span>
                <input
                  type="number"
                  value={projectionParams.retirement_age}
                  onChange={(e) => setProjectionParams({ ...projectionParams, retirement_age: parseInt(e.target.value) })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Current Savings ($)</span>
                <input
                  type="number"
                  value={projectionParams.current_savings}
                  onChange={(e) => setProjectionParams({ ...projectionParams, current_savings: parseFloat(e.target.value) })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Monthly Contribution ($)</span>
                <input
                  type="number"
                  value={projectionParams.monthly_contribution}
                  onChange={(e) => setProjectionParams({ ...projectionParams, monthly_contribution: parseFloat(e.target.value) })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Expected Return (%)</span>
                <input
                  type="number"
                  step="0.01"
                  value={projectionParams.expected_return * 100}
                  onChange={(e) => setProjectionParams({ ...projectionParams, expected_return: parseFloat(e.target.value) / 100 })}
                  className="form-input"
                />
              </div>
            </div>
            <button onClick={runProjection} disabled={loading} className="run-button">
              {loading ? 'Calculating...' : 'Run Projection'}
            </button>
          </div>

          {/* Projection Results */}
          {projection && (
            <div className="projection-panel">
              <h2>Retirement Projection</h2>
              <div className="projection-metrics">
                <div className="metric-card">
                  <div className="metric-label">Projected Retirement Savings</div>
                  <div className="metric-value">${projection.projected_savings?.toLocaleString()}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Success Probability</div>
                  <div className="metric-value" style={{ color: projection.success_probability > 0.8 ? '#00ff88' : '#ff8844' }}>
                    {(projection.success_probability * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Monthly Withdrawal Capacity</div>
                  <div className="metric-value">${projection.monthly_withdrawal?.toFixed(2)}</div>
                </div>
              </div>
              {projection.scenarios && (
                <div className="scenarios">
                  <h3>Scenario Analysis</h3>
                  <div className="scenarios-list">
                    {projection.scenarios.map((scenario, idx) => (
                      <div key={idx} className="scenario-item">
                        <span className="scenario-name">{scenario.name}</span>
                        <span className="scenario-value">${scenario.projected_value?.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Withdrawal Strategy */}
          {withdrawalStrategy && (
            <div className="withdrawal-panel">
              <h2>Optimal Withdrawal Strategy</h2>
              <div className="strategy-details">
                <div className="strategy-item">
                  <span className="label">Annual Withdrawal:</span>
                  <span className="value">${withdrawalStrategy.annual_withdrawal?.toFixed(2)}</span>
                </div>
                <div className="strategy-item">
                  <span className="label">Withdrawal Rate:</span>
                  <span className="value">{(withdrawalStrategy.withdrawal_rate * 100).toFixed(2)}%</span>
                </div>
                <div className="strategy-item">
                  <span className="label">Strategy Type:</span>
                  <span className="value">{withdrawalStrategy.strategy_type}</span>
                </div>
                {withdrawalStrategy.account_sequence && (
                  <div className="sequence">
                    <h3>Account Withdrawal Sequence</h3>
                    {withdrawalStrategy.account_sequence.map((account, idx) => (
                      <div key={idx} className="sequence-item">
                        {idx + 1}. {account.account_type} - ${account.withdrawal_amount?.toFixed(2)}/year
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default RetirementPlanningDashboard;
