/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AIPredictionsDashboard.jsx
 * ROLE: AI Predictions Dashboard
 * PURPOSE: Phase 25 - Advanced AI Predictions & Forecasting
 *          Displays price predictions, trend analysis, and market regime detection.
 * 
 * INTEGRATION POINTS:
 *    - AIPredictionsAPI: /api/ai-predictions endpoints
 * 
 * FEATURES:
 *    - Price forecasting
 *    - Trend prediction
 *    - Market regime detection
 *    - Confidence intervals
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AIPredictionsDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const AIPredictionsDashboard = () => {
  const [prediction, setPrediction] = useState(null);
  const [trend, setTrend] = useState(null);
  const [regime, setRegime] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPredictions();
    loadRegime();
  }, [selectedSymbol]);

  const loadPredictions = async () => {
    setLoading(true);
    try {
      // Load price prediction
      const predRes = await axios.post(`${API_BASE}/api/ai-predictions/price`, {
        symbol: selectedSymbol,
        time_horizon: '1m'
      });
      setPrediction(predRes.data.data);

      // Load trend prediction
      const trendRes = await axios.post(`${API_BASE}/api/ai-predictions/trend`, {
        symbol: selectedSymbol,
        time_horizon: '1m'
      });
      setTrend(trendRes.data.data);
    } catch (error) {
      console.error('Error loading predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRegime = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/ai-predictions/regime`, {
        params: { market_index: 'SPY' }
      });
      setRegime(res.data.data);
    } catch (error) {
      console.error('Error loading regime:', error);
    }
  };

  const getTrendColor = (direction) => {
    if (direction === 'bullish') return '#00ff88';
    if (direction === 'bearish') return '#ff4444';
    return '#888888';
  };

  const getRegimeColor = (type) => {
    if (type === 'bull') return '#00ff88';
    if (type === 'bear') return '#ff4444';
    if (type === 'volatile') return '#ff8844';
    return '#888888';
  };

  return (
    <div className="ai-predictions-dashboard">
      <div className="dashboard-header">
        <h1>AI Predictions & Forecasting</h1>
        <p className="subtitle">Phase 25: Advanced AI Predictions & Market Forecasting</p>
      </div>

      <div className="symbol-selector-section">
        <input
          type="text"
          value={selectedSymbol}
          onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
          placeholder="Enter symbol"
          className="symbol-input-large"
        />
        <button onClick={loadPredictions} disabled={loading} className="predict-button">
          {loading ? 'Predicting...' : 'Get Predictions'}
        </button>
      </div>

      <div className="predictions-grid">
        {/* Price Prediction */}
        {prediction && (
          <div className="prediction-card">
            <h2>Price Prediction</h2>
            <div className="prediction-main">
              <div className="predicted-price">
                ${prediction.predicted_price?.toFixed(2)}
              </div>
              <div className="confidence-badge" style={{
                backgroundColor: prediction.confidence > 0.7 ? 'rgba(0, 255, 136, 0.2)' : 
                                 prediction.confidence > 0.5 ? 'rgba(255, 136, 68, 0.2)' : 
                                 'rgba(255, 68, 68, 0.2)',
                color: prediction.confidence > 0.7 ? '#00ff88' : 
                       prediction.confidence > 0.5 ? '#ff8844' : '#ff4444'
              }}>
                Confidence: {(prediction.confidence * 100).toFixed(0)}%
              </div>
            </div>
            {prediction.confidence_interval && (
              <div className="confidence-interval">
                <div className="interval-label">Confidence Interval (95%)</div>
                <div className="interval-range">
                  ${prediction.confidence_interval.lower?.toFixed(2)} - ${prediction.confidence_interval.upper?.toFixed(2)}
                </div>
              </div>
            )}
            <div className="prediction-meta">
              <span>Time Horizon: {prediction.time_horizon}</span>
              <span>Model: {prediction.model_version}</span>
            </div>
          </div>
        )}

        {/* Trend Prediction */}
        {trend && (
          <div className="prediction-card">
            <h2>Trend Prediction</h2>
            <div className="trend-main">
              <div className="trend-direction" style={{ color: getTrendColor(trend.trend_direction) }}>
                {trend.trend_direction?.toUpperCase()}
              </div>
              <div className="trend-strength">
                Strength: {(trend.trend_strength * 100).toFixed(0)}%
              </div>
              <div className="predicted-change" style={{
                color: trend.predicted_change > 0 ? '#00ff88' : '#ff4444'
              }}>
                {trend.predicted_change > 0 ? '+' : ''}{trend.predicted_change.toFixed(2)}%
              </div>
            </div>
            <div className="trend-meta">
              <span>Confidence: {(trend.confidence * 100).toFixed(0)}%</span>
              <span>Horizon: {trend.time_horizon}</span>
            </div>
          </div>
        )}

        {/* Market Regime */}
        {regime && (
          <div className="prediction-card regime-card">
            <h2>Market Regime</h2>
            <div className="regime-main">
              <div className="regime-type" style={{ color: getRegimeColor(regime.regime_type) }}>
                {regime.regime_type?.toUpperCase()}
              </div>
              <div className="regime-confidence">
                Confidence: {(regime.confidence * 100).toFixed(0)}%
              </div>
              {regime.expected_duration && (
                <div className="regime-duration">
                  Expected Duration: {regime.expected_duration}
                </div>
              )}
            </div>
            <div className="regime-meta">
              <span>Detected: {new Date(regime.detected_date).toLocaleDateString()}</span>
            </div>
          </div>
        )}
      </div>

      {!prediction && !trend && !loading && (
        <div className="no-predictions">
          <p>Enter a symbol and click "Get Predictions" to see AI-powered forecasts</p>
        </div>
      )}
    </div>
  );
};

export default AIPredictionsDashboard;
