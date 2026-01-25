/**
 * ==============================================================================
 * FILE: frontend2/src/pages/EstatePlanningDashboard.jsx
 * ROLE: Estate Planning Dashboard
 * PURPOSE: Phase 9 - Estate Planning & Inheritance Tools
 *          Displays estate plans, beneficiaries, and inheritance projections.
 * 
 * INTEGRATION POINTS:
 *    - EstateAPI: /api/v1/estate endpoints
 * 
 * FEATURES:
 *    - Estate plan management
 *    - Beneficiary management
 *    - Inheritance simulation
 *    - Estate tax calculations
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './EstatePlanningDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const EstatePlanningDashboard = () => {
  const [estatePlan, setEstatePlan] = useState(null);
  const [beneficiaries, setBeneficiaries] = useState([]);
  const [inheritanceSim, setInheritanceSim] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newBeneficiary, setNewBeneficiary] = useState({ name: '', relationship: '', allocation_percent: '' });

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'summary', x: 0, y: 0, w: 12, h: 3 },
      { i: 'beneficiaries', x: 0, y: 3, w: 7, h: 6 },
      { i: 'simulation', x: 7, y: 3, w: 5, h: 6 }
    ]
  };
  const STORAGE_KEY = 'layout_estate_planning';

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

  useEffect(() => {
    loadEstatePlan();
    loadBeneficiaries();
  }, []);

  const loadEstatePlan = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/estate/plan`, {
        params: { user_id: userId }
      });
      setEstatePlan(res.data.data);
    } catch (error) {
      console.error('Error loading estate plan:', error);
    }
  };

  const loadBeneficiaries = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/estate/beneficiaries`, {
        params: { user_id: userId }
      });
      setBeneficiaries(res.data.data || []);
    } catch (error) {
      console.error('Error loading beneficiaries:', error);
    }
  };

  const addBeneficiary = async () => {
    if (!newBeneficiary.name || !newBeneficiary.allocation_percent) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/estate/beneficiary/add`, {
        user_id: userId,
        beneficiary_name: newBeneficiary.name,
        relationship: newBeneficiary.relationship,
        allocation_percent: parseFloat(newBeneficiary.allocation_percent)
      });
      setNewBeneficiary({ name: '', relationship: '', allocation_percent: '' });
      loadBeneficiaries();
    } catch (error) {
      console.error('Error adding beneficiary:', error);
    } finally {
      setLoading(false);
    }
  };

  const runInheritanceSimulation = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/estate/inheritance/simulate`, {
        user_id: userId
      });
      setInheritanceSim(res.data.data);
    } catch (error) {
      console.error('Error running inheritance simulation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page estate-planning-dashboard">
      <div className="dashboard-header">
        <h1>Estate Planning</h1>
        <p className="subtitle">Phase 9: Estate Planning & Inheritance Tools</p>
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
          {/* Estate Plan Summary */}
          <div key="summary" className="estate-plan-panel">
            <h2>Estate Plan Summary</h2>
            {estatePlan ? (
              <div className="estate-metrics">
                <div className="metric-card">
                  <div className="metric-label">Total Estate Value</div>
                  <div className="metric-value">${estatePlan.total_estate_value?.toLocaleString()}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Estimated Estate Tax</div>
                  <div className="metric-value" style={{ color: '#ff4444' }}>
                    ${estatePlan.estimated_estate_tax?.toLocaleString()}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Net Inheritance</div>
                  <div className="metric-value" style={{ color: '#00ff88' }}>
                    ${estatePlan.net_inheritance?.toLocaleString()}
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Number of Beneficiaries</div>
                  <div className="metric-value">{estatePlan.beneficiary_count || 0}</div>
                </div>
              </div>
            ) : (
              <div className="no-data">Loading estate plan...</div>
            )}
          </div>

          {/* Beneficiaries */}
          <div key="beneficiaries" className="beneficiaries-panel">
            <h2>Beneficiaries</h2>
            <div className="add-beneficiary-form">
              <div className="form-group">
                <span className="form-label">Beneficiary Name</span>
                <input
                  type="text"
                  placeholder="e.g. John Doe"
                  value={newBeneficiary.name}
                  onChange={(e) => setNewBeneficiary({ ...newBeneficiary, name: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Relationship</span>
                <input
                  type="text"
                  placeholder="e.g. Spouse"
                  value={newBeneficiary.relationship}
                  onChange={(e) => setNewBeneficiary({ ...newBeneficiary, relationship: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Allocation (%)</span>
                <input
                  type="number"
                  placeholder="0"
                  value={newBeneficiary.allocation_percent}
                  onChange={(e) => setNewBeneficiary({ ...newBeneficiary, allocation_percent: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group" style={{ justifyContent: 'flex-end' }}>
                <button onClick={addBeneficiary} disabled={loading} className="add-button">
                  Add Beneficiary
                </button>
              </div>
            </div>
            <div className="beneficiaries-list">
              {beneficiaries.length > 0 ? (
                beneficiaries.map((beneficiary) => (
                  <div key={beneficiary.beneficiary_id} className="beneficiary-card">
                    <div className="beneficiary-header">
                      <h3>{beneficiary.beneficiary_name}</h3>
                      <span className="relationship">{beneficiary.relationship}</span>
                    </div>
                    <div className="beneficiary-allocation">
                      <span className="allocation-percent">{beneficiary.allocation_percent}%</span>
                      {estatePlan && (
                        <span className="allocation-value">
                          ${((estatePlan.total_estate_value * beneficiary.allocation_percent) / 100).toLocaleString()}
                        </span>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-data">No beneficiaries added yet</div>
              )}
            </div>
          </div>

          {/* Inheritance Simulation */}
          <div key="simulation" className="simulation-panel">
            <h2>Inheritance Simulation</h2>
            <button onClick={runInheritanceSimulation} disabled={loading} className="simulate-button">
              {loading ? 'Running Simulation...' : 'Run Simulation'}
            </button>
            {inheritanceSim ? (
              <div className="simulation-results">
                <div className="sim-metric">
                  <span className="label">Total Inheritance:</span>
                  <span className="value">${inheritanceSim.total_inheritance?.toLocaleString()}</span>
                </div>
                <div className="sim-metric">
                  <span className="label">Tax Impact:</span>
                  <span className="value" style={{ color: '#ff4444' }}>
                    ${inheritanceSim.tax_impact?.toLocaleString()}
                  </span>
                </div>
                <div className="sim-metric">
                  <span className="label">Step-Up in Basis:</span>
                  <span className="value" style={{ color: '#00ff88' }}>
                    ${inheritanceSim.step_up_basis?.toLocaleString()}
                  </span>
                </div>
                {inheritanceSim.beneficiary_outcomes && (
                  <div className="outcomes">
                    <h3>Beneficiary Outcomes</h3>
                    {inheritanceSim.beneficiary_outcomes.map((outcome, idx) => (
                      <div key={idx} className="outcome-item">
                        <span>{outcome.beneficiary_name}:</span>
                        <span>${outcome.inheritance_amount?.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="no-data">Run simulation to see results</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default EstatePlanningDashboard;
