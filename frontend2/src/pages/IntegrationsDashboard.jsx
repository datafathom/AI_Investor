/**
 * ==============================================================================
 * FILE: frontend2/src/pages/IntegrationsDashboard.jsx
 * ROLE: Third-Party Integrations Dashboard
 * PURPOSE: Phase 28 - Third-Party App Integrations
 *          Displays available integrations, connection status, and sync management.
 * 
 * INTEGRATION POINTS:
 *    - IntegrationAPI: /api/v1/integrations endpoints
 * 
 * FEATURES:
 *    - Integration catalog
 *    - Connection management
 *    - Data synchronization
 *    - Sync history
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './IntegrationsDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const IntegrationsDashboard = () => {
  const [availableIntegrations, setAvailableIntegrations] = useState([]);
  const [connectedIntegrations, setConnectedIntegrations] = useState([]);
  const [syncHistory, setSyncHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');

  useEffect(() => {
    loadAvailableIntegrations();
    loadConnectedIntegrations();
    loadSyncHistory();
  }, []);

  const loadAvailableIntegrations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/integrations/available`);
      setAvailableIntegrations(res.data.data || []);
    } catch (error) {
      console.error('Error loading available integrations:', error);
    }
  };

  const loadConnectedIntegrations = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/integrations/connected`, {
        params: { user_id: userId }
      });
      setConnectedIntegrations(res.data.data || []);
    } catch (error) {
      console.error('Error loading connected integrations:', error);
    }
  };

  const loadSyncHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/integrations/sync-history`, {
        params: { user_id: userId, limit: 20 }
      });
      setSyncHistory(res.data.data || []);
    } catch (error) {
      console.error('Error loading sync history:', error);
    }
  };

  const connectIntegration = async (integrationId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/integrations/connect`, {
        user_id: userId,
        integration_id: integrationId
      });
      loadConnectedIntegrations();
    } catch (error) {
      console.error('Error connecting integration:', error);
    } finally {
      setLoading(false);
    }
  };

  const syncIntegration = async (integrationId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/integrations/sync`, {
        integration_id: integrationId
      });
      loadSyncHistory();
    } catch (error) {
      console.error('Error syncing integration:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="integrations-dashboard">
      <div className="dashboard-header">
        <h1>Third-Party Integrations</h1>
        <p className="subtitle">Phase 28: Third-Party App Integrations</p>
      </div>

      <div className="dashboard-content">
        {/* Available Integrations */}
        <div className="available-panel">
          <h2>Available Integrations</h2>
          {availableIntegrations.length > 0 ? (
            <div className="integrations-grid">
              {availableIntegrations.map((integration) => {
                const isConnected = connectedIntegrations.some(
                  conn => conn.integration_id === integration.integration_id
                );
                return (
                  <div key={integration.integration_id} className="integration-card">
                    <div className="integration-icon">
                      <span className="icon-text">{integration.name?.charAt(0)}</span>
                    </div>
                    <h3>{integration.name}</h3>
                    <p className="integration-description">{integration.description}</p>
                    <div className="integration-category">{integration.category}</div>
                    {isConnected ? (
                      <button className="connected-button" disabled>
                        Connected
                      </button>
                    ) : (
                      <button
                        onClick={() => connectIntegration(integration.integration_id)}
                        disabled={loading}
                        className="connect-button"
                      >
                        Connect
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="no-data">No integrations available</div>
          )}
        </div>

        {/* Connected Integrations */}
        <div className="connected-panel">
          <h2>Connected Integrations</h2>
          {connectedIntegrations.length > 0 ? (
            <div className="connected-list">
              {connectedIntegrations.map((integration) => (
                <div key={integration.connection_id} className="connected-card">
                  <div className="connected-header">
                    <h3>{integration.integration_name}</h3>
                    <span className={`connection-status ${integration.status}`}>
                      {integration.status}
                    </span>
                  </div>
                  <div className="connection-details">
                    <span>Last Sync: {new Date(integration.last_sync || Date.now()).toLocaleDateString()}</span>
                    <span>Records Synced: {integration.records_synced || 0}</span>
                  </div>
                  <div className="connection-actions">
                    <button
                      onClick={() => syncIntegration(integration.integration_id)}
                      disabled={loading}
                      className="sync-button"
                    >
                      Sync Now
                    </button>
                    <button className="disconnect-button">Disconnect</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No connected integrations</div>
          )}
        </div>

        {/* Sync History */}
        <div className="history-panel">
          <h2>Sync History</h2>
          {syncHistory.length > 0 ? (
            <div className="history-list">
              {syncHistory.map((sync) => (
                <div key={sync.sync_id} className="history-item">
                  <div className="history-info">
                    <span className="sync-app">{sync.integration_name}</span>
                    <span className="sync-status">{sync.status}</span>
                  </div>
                  <div className="history-details">
                    <span>{sync.records_synced || 0} records</span>
                    <span>{new Date(sync.sync_date).toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No sync history</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default IntegrationsDashboard;
