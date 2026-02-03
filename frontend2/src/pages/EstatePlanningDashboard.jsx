/**
 * ==============================================================================
 * FILE: frontend2/src/pages/EstatePlanningDashboard.jsx
 * ROLE: Estate Planning Dashboard
 * PURPOSE: Phase 9 - Estate Planning & Inheritance Tools
 * 
 * INTEGRATION POINTS:
 *    - EstateStore: Uses apiClient for all API calls (User Rule 6)
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-30
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import useEstateStore from '../stores/estateStore';
import './EstatePlanningDashboard.css';
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const EstatePlanningDashboard = () => {
  const userId = 'user_1'; // TODO: Get from authStore
  
  const {
    estatePlan,
    beneficiaries,
    inheritanceSim,
    isLoading,
    fetchEstatePlan,
    fetchBeneficiaries,
    addBeneficiary,
    runInheritanceSimulation
  } = useEstateStore();

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
    StorageService.set(STORAGE_KEY, allLayouts);
  };

  useEffect(() => {
    fetchEstatePlan(userId);
    fetchBeneficiaries(userId);
  }, [fetchEstatePlan, fetchBeneficiaries]);

  const handleAddBeneficiary = async () => {
    if (!newBeneficiary.name || !newBeneficiary.allocation_percent) return;
    const success = await addBeneficiary({
      user_id: userId,
      beneficiary_name: newBeneficiary.name,
      relationship: newBeneficiary.relationship,
      allocation_percent: parseFloat(newBeneficiary.allocation_percent)
    });
    if (success) {
      setNewBeneficiary({ name: '', relationship: '', allocation_percent: '' });
    }
  };

  const handleRunSimulation = async () => {
    await runInheritanceSimulation(userId);
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
                <button onClick={handleAddBeneficiary} disabled={isLoading} className="add-button">
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
            <button onClick={handleRunSimulation} disabled={isLoading} className="simulate-button">
              {isLoading ? 'Running Simulation...' : 'Run Simulation'}
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
