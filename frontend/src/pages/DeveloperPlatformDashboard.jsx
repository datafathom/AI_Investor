import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import usePublicApiStore from '../stores/publicApiStore';
import AgentLogicEditor from '../components/Development/AgentLogicEditor';
import HistoryReplay from '../components/Development/HistoryReplay';
import { Grid, Box } from '@mui/material';
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
      <div className="dashboard-header" style={{ marginBottom: '24px' }}>
        <h1 style={{ color: '#eee', margin: 0 }}>Sovereign Developer Forge</h1>
        <p className="subtitle" style={{ color: '#586e75' }}>: Phase 7 Meta-Logic & Autonomous Hot-Swap</p>
      </div>

      <Box sx={{ mb: 4 }}>
        <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 8 }}>
                <AgentLogicEditor />
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
                <HistoryReplay />
            </Grid>
        </Grid>
      </Box>

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

        {/* Create API Key & Keys List (Simplified for space) */}
        <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
                <div className="create-key-panel" style={{ height: '100%' }}>
                  <h2>Generate Sovereign Access Key</h2>
                  <div className="key-form" style={{ marginTop: '16px' }}>
                    <input
                      type="text"
                      placeholder="Access Key Label..."
                      value={newKeyName}
                      onChange={(e) => setNewKeyName(e.target.value)}
                      className="form-input"
                      style={{ background: '#073642', border: '1px solid #586e75', color: '#eee' }}
                    />
                    <button 
                        onClick={handleCreateKey} 
                        disabled={loading || !newKeyName} 
                        className="create-button"
                        style={{ background: '#268bd2' }}
                    >
                      Issue Key
                    </button>
                  </div>
                </div>
            </Grid>
        </Grid>
      </div>
    </div>
  );
};

export default DeveloperPlatformDashboard;
