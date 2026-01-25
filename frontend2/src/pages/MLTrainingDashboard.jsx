/**
 * ==============================================================================
 * FILE: frontend2/src/pages/MLTrainingDashboard.jsx
 * ROLE: ML Training Pipeline Dashboard
 * PURPOSE: Phase 27 - Machine Learning Model Training Pipeline
 *          Displays ML training jobs, model versions, and deployment status.
 * 
 * INTEGRATION POINTS:
 *    - MLTrainingAPI: /api/v1/ml-training endpoints
 * 
 * FEATURES:
 *    - Training job management
 *    - Model versioning
 *    - Deployment monitoring
 *    - Performance metrics
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MLTrainingDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const MLTrainingDashboard = () => {
  const [trainingJobs, setTrainingJobs] = useState([]);
  const [modelVersions, setModelVersions] = useState([]);
  const [deployments, setDeployments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newJob, setNewJob] = useState({ model_type: 'price_prediction', dataset: '' });

  useEffect(() => {
    loadTrainingJobs();
    loadModelVersions();
    loadDeployments();
  }, []);

  const loadTrainingJobs = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/ml-training/jobs`, {
        params: { user_id: userId }
      });
      setTrainingJobs(res.data.data || []);
    } catch (error) {
      console.error('Error loading training jobs:', error);
    }
  };

  const loadModelVersions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/ml-training/models`, {
        params: { user_id: userId }
      });
      setModelVersions(res.data.data || []);
    } catch (error) {
      console.error('Error loading model versions:', error);
    }
  };

  const loadDeployments = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/ml-training/deployments`, {
        params: { user_id: userId }
      });
      setDeployments(res.data.data || []);
    } catch (error) {
      console.error('Error loading deployments:', error);
    }
  };

  const startTrainingJob = async () => {
    if (!newJob.model_type || !newJob.dataset) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/ml-training/job/start`, {
        user_id: userId,
        model_type: newJob.model_type,
        dataset: newJob.dataset
      });
      setNewJob({ model_type: 'price_prediction', dataset: '' });
      loadTrainingJobs();
    } catch (error) {
      console.error('Error starting training job:', error);
    } finally {
      setLoading(false);
    }
  };

  const deployModel = async (modelId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/ml-training/deploy`, {
        model_id: modelId
      });
      loadDeployments();
      loadModelVersions();
    } catch (error) {
      console.error('Error deploying model:', error);
    } finally {
      setLoading(false);
    }
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
            <button onClick={startTrainingJob} disabled={loading} className="start-button">
              Start Training
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
                      onClick={() => deployModel(model.model_id)}
                      disabled={loading}
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
