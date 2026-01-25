/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedChartingDashboard.jsx
 * ROLE: Advanced Charting & Technical Analysis Dashboard
 * PURPOSE: Phase 5 - Advanced Charting & Technical Analysis
 *          Displays advanced charts, technical indicators, and pattern recognition.
 * 
 * INTEGRATION POINTS:
 *    - ChartingAPI: /api/v1/charting endpoints
 * 
 * FEATURES:
 *    - Multiple chart types (candlestick, line, area)
 *    - Technical indicators overlay
 *    - Chart pattern recognition
 *    - Multiple timeframes
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdvancedChartingDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const AdvancedChartingDashboard = () => {
  const [chartData, setChartData] = useState(null);
  const [indicators, setIndicators] = useState(null);
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [chartType, setChartType] = useState('candlestick');
  const [timeframe, setTimeframe] = useState('1d');
  const [selectedIndicators, setSelectedIndicators] = useState(['sma_20', 'rsi']);

  useEffect(() => {
    loadChartData();
    loadIndicators();
    loadPatterns();
  }, [selectedSymbol, timeframe]);

  const loadChartData = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/api/v1/charting/data`, {
        params: {
          symbol: selectedSymbol,
          chart_type: chartType,
          timeframe: timeframe,
          limit: 100
        }
      });
      setChartData(res.data.data);
    } catch (error) {
      console.error('Error loading chart data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadIndicators = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/charting/indicators`, {
        params: {
          symbol: selectedSymbol,
          timeframe: timeframe,
          indicators: selectedIndicators.join(',')
        }
      });
      setIndicators(res.data.data);
    } catch (error) {
      console.error('Error loading indicators:', error);
    }
  };

  const loadPatterns = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/charting/patterns`, {
        params: {
          symbol: selectedSymbol,
          timeframe: timeframe
        }
      });
      setPatterns(res.data.data || []);
    } catch (error) {
      console.error('Error loading patterns:', error);
    }
  };

  return (
    <div className="advanced-charting-dashboard">
      <div className="dashboard-header">
        <h1>Advanced Charting & Technical Analysis</h1>
        <p className="subtitle">Phase 5: Advanced Charting & Technical Analysis</p>
      </div>

      <div className="chart-controls">
        <input
          type="text"
          value={selectedSymbol}
          onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
          placeholder="Symbol"
          className="symbol-input"
        />
        <select
          value={chartType}
          onChange={(e) => setChartType(e.target.value)}
          className="control-select"
        >
          <option value="candlestick">Candlestick</option>
          <option value="line">Line</option>
          <option value="area">Area</option>
          <option value="heikin_ashi">Heikin-Ashi</option>
        </select>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          className="control-select"
        >
          <option value="1m">1 Minute</option>
          <option value="5m">5 Minutes</option>
          <option value="15m">15 Minutes</option>
          <option value="1h">1 Hour</option>
          <option value="1d">1 Day</option>
          <option value="1w">1 Week</option>
        </select>
        <button onClick={loadChartData} disabled={loading} className="load-button">
          Load Chart
        </button>
      </div>

      <div className="dashboard-content">
        {/* Chart Display */}
        <div className="chart-panel">
          <h2>Price Chart - {selectedSymbol}</h2>
          {loading ? (
            <div className="loading">Loading chart data...</div>
          ) : chartData ? (
            <div className="chart-container">
              <div className="chart-placeholder">
                <p>Chart visualization would render here</p>
                <p className="chart-info">
                  {chartData.data_points?.length || 0} data points loaded
                </p>
                {chartData.current_price && (
                  <div className="current-price">
                    Current Price: ${chartData.current_price.toFixed(2)}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="no-data">No chart data available</div>
          )}
        </div>

        {/* Technical Indicators */}
        {indicators && (
          <div className="indicators-panel">
            <h2>Technical Indicators</h2>
            <div className="indicators-grid">
              {indicators.sma_20 && (
                <div className="indicator-card">
                  <div className="indicator-label">SMA 20</div>
                  <div className="indicator-value">${indicators.sma_20.toFixed(2)}</div>
                </div>
              )}
              {indicators.sma_50 && (
                <div className="indicator-card">
                  <div className="indicator-label">SMA 50</div>
                  <div className="indicator-value">${indicators.sma_50.toFixed(2)}</div>
                </div>
              )}
              {indicators.rsi !== null && (
                <div className="indicator-card">
                  <div className="indicator-label">RSI</div>
                  <div className="indicator-value" style={{
                    color: indicators.rsi > 70 ? '#ff4444' : indicators.rsi < 30 ? '#00ff88' : '#00d4ff'
                  }}>
                    {indicators.rsi.toFixed(2)}
                  </div>
                  <div className="indicator-status">
                    {indicators.rsi > 70 ? 'Overbought' : indicators.rsi < 30 ? 'Oversold' : 'Neutral'}
                  </div>
                </div>
              )}
              {indicators.macd && (
                <div className="indicator-card">
                  <div className="indicator-label">MACD</div>
                  <div className="indicator-value">{indicators.macd.toFixed(4)}</div>
                </div>
              )}
              {indicators.bollinger_bands && (
                <div className="indicator-card">
                  <div className="indicator-label">Bollinger Bands</div>
                  <div className="indicator-value">
                    Upper: ${indicators.bollinger_bands.upper?.toFixed(2)}<br />
                    Lower: ${indicators.bollinger_bands.lower?.toFixed(2)}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Chart Patterns */}
        <div className="patterns-panel">
          <h2>Detected Patterns</h2>
          {patterns.length > 0 ? (
            <div className="patterns-list">
              {patterns.map((pattern, idx) => (
                <div key={idx} className="pattern-card">
                  <div className="pattern-header">
                    <h3>{pattern.pattern_name}</h3>
                    <span className={`pattern-signal ${pattern.signal}`}>
                      {pattern.signal}
                    </span>
                  </div>
                  <div className="pattern-details">
                    <span>Confidence: {(pattern.confidence * 100).toFixed(0)}%</span>
                    <span>Detected: {new Date(pattern.detected_date).toLocaleDateString()}</span>
                  </div>
                  {pattern.description && (
                    <p className="pattern-description">{pattern.description}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No patterns detected</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedChartingDashboard;
