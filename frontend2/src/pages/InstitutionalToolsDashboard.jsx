/**
 * ==============================================================================
 * FILE: frontend2/src/pages/InstitutionalToolsDashboard.jsx
 * ROLE: Institutional Tools Dashboard
 * PURPOSE: Phase 33 - Institutional & Professional Tools
 *          Displays multi-client management, white-labeling, and professional analytics.
 * 
 * INTEGRATION POINTS:
 *    - InstitutionalAPI: /api/v1/institutional endpoints
 * 
 * FEATURES:
 *    - Multi-client management
 *    - White-label configuration
 *    - Professional analytics
 *    - Custom reporting
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './InstitutionalToolsDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const InstitutionalToolsDashboard = () => {
  const [clients, setClients] = useState([]);
  const [whiteLabelConfig, setWhiteLabelConfig] = useState(null);
  const [professionalAnalytics, setProfessionalAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newClient, setNewClient] = useState({ name: '', email: '' });

  useEffect(() => {
    loadClients();
    loadWhiteLabelConfig();
    loadProfessionalAnalytics();
  }, []);

  const loadClients = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/institutional/clients`, {
        params: { user_id: userId }
      });
      setClients(res.data.data || []);
    } catch (error) {
      console.error('Error loading clients:', error);
    }
  };

  const loadWhiteLabelConfig = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/institutional/white-label`, {
        params: { user_id: userId }
      });
      setWhiteLabelConfig(res.data.data);
    } catch (error) {
      console.error('Error loading white-label config:', error);
    }
  };

  const loadProfessionalAnalytics = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/institutional/analytics`, {
        params: { user_id: userId }
      });
      setProfessionalAnalytics(res.data.data);
    } catch (error) {
      console.error('Error loading professional analytics:', error);
    }
  };

  const createClient = async () => {
    if (!newClient.name || !newClient.email) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/institutional/client/create`, {
        user_id: userId,
        client_name: newClient.name,
        client_email: newClient.email
      });
      setNewClient({ name: '', email: '' });
      loadClients();
    } catch (error) {
      console.error('Error creating client:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="institutional-tools-dashboard">
      <div className="dashboard-header">
        <h1>Institutional & Professional Tools</h1>
        <p className="subtitle">Phase 33: Institutional & Professional Tools</p>
      </div>

      <div className="dashboard-content">
        {/* Create Client */}
        <div className="create-client-panel">
          <h2>Add Client</h2>
          <div className="client-form">
            <input
              type="text"
              placeholder="Client Name"
              value={newClient.name}
              onChange={(e) => setNewClient({ ...newClient, name: e.target.value })}
              className="form-input"
            />
            <input
              type="email"
              placeholder="Client Email"
              value={newClient.email}
              onChange={(e) => setNewClient({ ...newClient, email: e.target.value })}
              className="form-input"
            />
            <button onClick={createClient} disabled={loading} className="create-button">
              Add Client
            </button>
          </div>
        </div>

        {/* Clients */}
        <div className="clients-panel">
          <h2>Client Accounts</h2>
          {clients.length > 0 ? (
            <div className="clients-list">
              {clients.map((client) => (
                <div key={client.client_id} className="client-card">
                  <div className="client-header">
                    <h3>{client.client_name}</h3>
                    <span className={`client-status ${client.status}`}>{client.status}</span>
                  </div>
                  <div className="client-details">
                    <span>Email: {client.client_email}</span>
                    <span>Portfolios: {client.portfolio_count || 0}</span>
                    <span>Total AUM: ${client.total_aum?.toLocaleString() || '0'}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No clients added yet</div>
          )}
        </div>

        {/* White-Label Configuration */}
        {whiteLabelConfig && (
          <div className="white-label-panel">
            <h2>White-Label Configuration</h2>
            <div className="config-details">
              <div className="config-item">
                <span className="label">Brand Name:</span>
                <span className="value">{whiteLabelConfig.brand_name || 'Default'}</span>
              </div>
              <div className="config-item">
                <span className="label">Primary Color:</span>
                <span className="value" style={{ color: whiteLabelConfig.primary_color || '#00d4ff' }}>
                  {whiteLabelConfig.primary_color || '#00d4ff'}
                </span>
              </div>
              <div className="config-item">
                <span className="label">Logo URL:</span>
                <span className="value">{whiteLabelConfig.logo_url || 'Not set'}</span>
              </div>
              <div className="config-item">
                <span className="label">Custom Domain:</span>
                <span className="value">{whiteLabelConfig.custom_domain || 'Not configured'}</span>
              </div>
            </div>
          </div>
        )}

        {/* Professional Analytics */}
        {professionalAnalytics && (
          <div className="analytics-panel">
            <h2>Professional Analytics</h2>
            <div className="analytics-metrics">
              <div className="metric-card">
                <div className="metric-label">Total Clients</div>
                <div className="metric-value">{professionalAnalytics.total_clients || 0}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Total AUM</div>
                <div className="metric-value">
                  ${(professionalAnalytics.total_aum || 0).toLocaleString()}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Active Portfolios</div>
                <div className="metric-value">{professionalAnalytics.active_portfolios || 0}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">API Calls (30d)</div>
                <div className="metric-value">{professionalAnalytics.api_calls_30d || 0}</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InstitutionalToolsDashboard;
