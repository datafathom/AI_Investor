/**
 * ==============================================================================
 * FILE: frontend2/src/pages/MLTrainingDashboard.jsx
 * ROLE: ML Training Pipeline Dashboard
 * PURPOSE: Phase 27 - Machine Learning Model Training Pipeline
 *          Displays ML training jobs, model versions, and deployment status.
 * 
 * INTEGRATION POINTS:
 *    - MLStore: Centralized state management
 *    - MLTrainingAPI: /api/v1/ml-training endpoints (via Service)
 * 
 * FEATURES:
 *    - Training job management
 *    - Model versioning
 *    - Deployment monitoring
 *    - Performance metrics
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-28
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import useMLStore from '../stores/mlStore';
import './MLTrainingDashboard.css';

const MLTrainingDashboard = () => {
  // Store State
  const { 
    trainingJobs, 
    modelVersions, 
    deployments, 
    isLoading, 
    fetchTrainingJobs, 
    fetchModelVersions, 
    fetchDeployments,
    startTrainingJob: startJobAction,
    deployModel: deployModelAction
  } = useMLStore();

  const [userId] = useState('user_1');
  const [newJob, setNewJob] = useState({ model_type: 'price_prediction', dataset: '' });

  // Load Data on Mount
  useEffect(() => {
    fetchTrainingJobs(userId);
    fetchModelVersions(userId);
    fetchDeployments(userId);
  }, [userId, fetchTrainingJobs, fetchModelVersions, fetchDeployments]);

  const handleStartTrainingJob = async () => {
    if (!newJob.model_type || !newJob.dataset) return;
    
    const success = await startJobAction(userId, newJob.model_type, newJob.dataset);
    if (success) {
      setNewJob({ model_type: 'price_prediction', dataset: '' });
    }
  };

  const handleDeployModel = async (modelId) => {
    await deployModelAction(userId, modelId);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#00ff88';
      case 'running': return '#00d4ff';
      case 'failed': return '#ff4444';
      case 'pending': return '#ff8844';
      default: return '#888';
    }
  };

  return (
    <div className="ml-training-dashboard">
      <div className="dashboard-header">
        <h1>ML Training Pipeline</h1>
        <p className="subtitle">Phase 27: Machine Learning Model Training Pipeline</p>
      </div>

      <div className="dashboard-content">
        {/* Start Training Job */}
        <div className="start-job-panel">
          <h2>Start Training Job</h2>
          <div className="job-form">
            <select
              value={newJob.model_type}
              onChange={(e) => setNewJob({ ...newJob, model_type: e.target.value })}
              className="form-input"
            >
              <option value="price_prediction">Price Prediction</option>
              <option value="sentiment_analysis">Sentiment Analysis</option>
              <option value="volatility_forecast">Volatility Forecast</option>
              <option value="trend_detection">Trend Detection</option>
            </select>
            <input
              type="text"
              placeholder="Dataset ID"
              value={newJob.dataset}
              onChange={(e) => setNewJob({ ...newJob, dataset: e.target.value })}
              className="form-input"
            />
            <button onClick={handleStartTrainingJob} disabled={isLoading} className="start-button">
              {isLoading ? 'Starting...' : 'Start Training'}
            </button>
          </div>
        </div>

        {/* Training Jobs */}
        <div className="jobs-panel">
          <h2>Training Jobs</h2>
          {trainingJobs.length > 0 ? (
            <div className="jobs-list">
              {trainingJobs.map((job) => (
                <div key={job.job_id} className="job-card">
                  <div className="job-header">
                    <h3>{job.model_type}</h3>
                    <span className="job-status" style={{ color: getStatusColor(job.status) }}>
                      {job.status}
                    </span>
                  </div>
                  <div className="job-details">
                    <span>Progress: {job.progress_percent || 0}%</span>
                    <span>Epochs: {job.current_epoch || 0}/{job.total_epochs || 0}</span>
                    <span>Started: {new Date(job.started_date).toLocaleDateString()}</span>
                  </div>
                  {job.status === 'running' && (
                    <div className="progress-bar-container">
                      <div className="progress-bar" style={{ width: `${job.progress_percent || 0}%` }}></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No training jobs</div>
          )}
        </div>

        {/* Model Versions */}
        <div className="models-panel">
          <h2>Model Versions</h2>
          {modelVersions.length > 0 ? (
            <div className="models-list">
              {modelVersions.map((model) => (
                <div key={model.model_id} className="model-card">
                  <div className="model-header">
                    <h3>v{model.version}</h3>
                    <span className="model-status">{model.status}</span>
                  </div>
                  <div className="model-metrics">
                    <div className="metric">
                      <span className="label">Accuracy:</span>
                      <span className="value">{(model.accuracy * 100 || 0).toFixed(2)}%</span>
                    </div>
                    <div className="metric">
                      <span className="label">Loss:</span>
                      <span className="value">{model.loss?.toFixed(4) || 'N/A'}</span>
                    </div>
                    <div className="metric">
                      <span className="label">Trained:</span>
                      <span className="value">{new Date(model.trained_date).toLocaleDateString()}</span>
                    </div>
                  </div>
                  {model.status === 'ready' && (
                    <button
                      onClick={() => handleDeployModel(model.model_id)}
                      disabled={isLoading}
                      className="deploy-button"
                    >
                      Deploy Model
                    </button>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No model versions</div>
          )}
        </div>

        {/* Deployments */}
        <div className="deployments-panel">
          <h2>Active Deployments</h2>
          {deployments.length > 0 ? (
            <div className="deployments-list">
              {deployments.map((deployment) => (
                <div key={deployment.deployment_id} className="deployment-card">
                  <div className="deployment-header">
                    <h3>Model v{deployment.model_version}</h3>
                    <span className={`deployment-status ${deployment.status}`}>
                      {deployment.status}
                    </span>
                  </div>
                  <div className="deployment-details">
                    <span>Type: {deployment.deployment_type}</span>
                    <span>Traffic: {deployment.traffic_percent || 0}%</span>
                    <span>Requests: {deployment.request_count || 0}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No active deployments</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MLTrainingDashboard;

