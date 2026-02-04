/**
 * ==============================================================================
 * FILE: frontend2/src/pages/DeveloperPlatformDashboard.jsx
 * ROLE: Developer Platform Dashboard
 * PURPOSE: Phase 29 - Public API & Developer Platform
 * 
 * INTEGRATION POINTS:
 *    - PublicApiStore: Uses apiClient for all API calls (User Rule 6)
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-30
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import usePublicApiStore from '../stores/publicApiStore';
import './DeveloperPlatformDashboard.css';

const DeveloperPlatformDashboard = () => {
  const userId = 'user_1'; // TODO: Get from authStore
  
  const {
    apiKeys,
    usage,
    loading,
    fetchApiKeys,
    fetchUsage,
    createApiKey,
    revokeApiKey
  } = usePublicApiStore();

  const [newKeyName, setNewKeyName] = useState('');

  useEffect(() => {
    fetchApiKeys(userId);
    fetchUsage(userId);
  }, [fetchApiKeys, fetchUsage]);

  const handleCreateKey = async () => {
    if (!newKeyName) return;
    const success = await createApiKey({ user_id: userId, key_name: newKeyName });
    if (success) {
      setNewKeyName('');
    }
  };

  const handleRevokeKey = async (keyId) => {
    await revokeApiKey(keyId, userId);
  };

  return (
    <div className="developer-platform-dashboard">
      <div className="dashboard-header">
        <h1>Developer Platform</h1>
        <p className="subtitle">Phase 29: Public API & Developer Platform</p>
      </div>

      <div className="dashboard-content">
        {/* Usage Statistics */}
        {usage && (
          <div className="stats-panel">
            <h2>API Usage Statistics</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label">Total Requests (30d)</div>
                <div className="stat-value">{usage.total_requests_30d || 0}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Active Keys</div>
                <div className="stat-value">{apiKeys.filter(k => k.status === 'active').length}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Rate Limit</div>
                <div className="stat-value">{usage.rate_limit || 'N/A'}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Remaining Quota</div>
                <div className="stat-value">{usage.remaining_quota || 'Unlimited'}</div>
              </div>
            </div>
          </div>
        )}

        {/* Create API Key */}
        <div className="create-key-panel">
          <h2>Create API Key</h2>
          <div className="key-form">
            <input
              type="text"
              placeholder="Key Name"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              className="form-input"
            />
            <button onClick={handleCreateKey} disabled={loading || !newKeyName} className="create-button">
              Create Key
            </button>
          </div>
        </div>

        {/* API Keys */}
        <div className="keys-panel">
          <h2>Your API Keys</h2>
          {apiKeys.length > 0 ? (
            <div className="keys-list">
              {apiKeys.map((key) => (
                <div key={key.api_key_id} className="key-card">
                  <div className="key-header">
                    <h3>{key.key_name}</h3>
                    <span className={`key-status ${key.status}`}>{key.status}</span>
                  </div>
                  <div className="key-details">
                    <div className="key-value">
                      <span className="label">API Key:</span>
                      <code className="key-code">{key.api_key?.substring(0, 20)}...</code>
                      <button className="copy-button">Copy</button>
                    </div>
                    <div className="key-meta">
                      <span>Created: {new Date(key.created_date).toLocaleDateString()}</span>
                      <span>Last Used: {key.last_used ? new Date(key.last_used).toLocaleDateString() : 'Never'}</span>
                      <span>Requests: {key.request_count || 0}</span>
                    </div>
                  </div>
                  {key.status === 'active' && (
                    <button
                      onClick={() => handleRevokeKey(key.api_key_id)}
                      disabled={loading}
                      className="revoke-button"
                    >
                      Revoke Key
                    </button>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No API keys created yet</div>
          )}
        </div>

        {/* Developer Resources */}
        <div className="resources-panel">
          <h2>Developer Resources</h2>
          <div className="resources-grid">
            <div className="resource-card">
              <h3>API Documentation</h3>
              <p>Complete API reference with examples</p>
              <button className="resource-button">View Docs</button>
            </div>
            <div className="resource-card">
              <h3>SDKs & Libraries</h3>
              <p>Official SDKs for popular languages</p>
              <button className="resource-button">Download SDKs</button>
            </div>
            <div className="resource-card">
              <h3>Sandbox Environment</h3>
              <p>Test your integration safely</p>
              <button className="resource-button">Access Sandbox</button>
            </div>
            <div className="resource-card">
              <h3>Support & Community</h3>
              <p>Get help from our developer community</p>
              <button className="resource-button">Join Community</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeveloperPlatformDashboard;
