/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedChartingDashboard.jsx
 * ROLE: Advanced Charting & Technical Analysis Dashboard
 * PURPOSE:  - Advanced Charting & Technical Analysis
 * 
 * INTEGRATION POINTS:
 *    - ChartingStore: Uses apiClient for all API calls (User Rule 6)
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-30
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import useChartingStore from '../stores/chartingStore';
import './AdvancedChartingDashboard.css';

const AdvancedChartingDashboard = () => {
  const {
    chartData,
    indicators,
    patterns,
    loading,
    fetchChartData,
    fetchIndicators,
    fetchPatterns
  } = useChartingStore();

  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [chartType, setChartType] = useState('candlestick');
  const [timeframe, setTimeframe] = useState('1d');
  const [selectedIndicators] = useState(['sma_20', 'rsi']);

  useEffect(() => {
    loadData();
  }, [selectedSymbol, timeframe]);

  const loadData = () => {
    const params = { symbol: selectedSymbol, timeframe, chart_type: chartType, limit: 100 };
    fetchChartData(params);
    fetchIndicators({ ...params, indicators: selectedIndicators.join(',') });
    fetchPatterns(params);
  };

  // Get first chart data item for display (store returns array now)
  const currentChart = Array.isArray(chartData) ? chartData[0] : chartData;
  const currentIndicators = Array.isArray(indicators) ? indicators[0] : indicators;

  return (
    <div className="advanced-charting-dashboard">
      <div className="dashboard-header">
        <h1>Advanced Charting & Technical Analysis</h1>
        <p className="subtitle">: Advanced Charting & Technical Analysis</p>
      </div>

      <div className="chart-controls">
        <input
          type="text"
          value={selectedSymbol}
          onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
          placeholder="Symbol"
          className="symbol-input"
        />
        <select value={chartType} onChange={(e) => setChartType(e.target.value)} className="control-select">
          <option value="candlestick">Candlestick</option>
          <option value="line">Line</option>
          <option value="area">Area</option>
          <option value="heikin_ashi">Heikin-Ashi</option>
        </select>
        <select value={timeframe} onChange={(e) => setTimeframe(e.target.value)} className="control-select">
          <option value="1m">1 Minute</option>
          <option value="5m">5 Minutes</option>
          <option value="15m">15 Minutes</option>
          <option value="1h">1 Hour</option>
          <option value="1d">1 Day</option>
          <option value="1w">1 Week</option>
        </select>
        <button onClick={loadData} disabled={loading} className="load-button">
          Load Chart
        </button>
      </div>

      <div className="dashboard-content">
        {/* Chart Display */}
        <div className="chart-panel">
          <h2>Price Chart - {selectedSymbol}</h2>
          {loading ? (
            <div className="loading">Loading chart data...</div>
          ) : currentChart ? (
            <div className="chart-container">
              <div className="chart-placeholder">
                <p>Chart visualization would render here</p>
                <p className="chart-info">{currentChart.data_points?.length || 0} data points loaded</p>
                {currentChart.current_price && (
                  <div className="current-price">Current Price: ${currentChart.current_price.toFixed(2)}</div>
                )}
              </div>
            </div>
          ) : (
            <div className="no-data">No chart data available</div>
          )}
        </div>

        {/* Technical Indicators */}
        {currentIndicators && (
          <div className="indicators-panel">
            <h2>Technical Indicators</h2>
            <div className="indicators-grid">
              {currentIndicators.sma_20 && (
                <div className="indicator-card">
                  <div className="indicator-label">SMA 20</div>
                  <div className="indicator-value">${currentIndicators.sma_20.toFixed(2)}</div>
                </div>
              )}
              {currentIndicators.sma_50 && (
                <div className="indicator-card">
                  <div className="indicator-label">SMA 50</div>
                  <div className="indicator-value">${currentIndicators.sma_50.toFixed(2)}</div>
                </div>
              )}
              {currentIndicators.rsi !== null && currentIndicators.rsi !== undefined && (
                <div className="indicator-card">
                  <div className="indicator-label">RSI</div>
                  <div className="indicator-value" style={{
                    color: currentIndicators.rsi > 70 ? '#ff4444' : currentIndicators.rsi < 30 ? '#00ff88' : '#00d4ff'
                  }}>
                    {currentIndicators.rsi.toFixed(2)}
                  </div>
                  <div className="indicator-status">
                    {currentIndicators.rsi > 70 ? 'Overbought' : currentIndicators.rsi < 30 ? 'Oversold' : 'Neutral'}
                  </div>
                </div>
              )}
              {currentIndicators.macd && (
                <div className="indicator-card">
                  <div className="indicator-label">MACD</div>
                  <div className="indicator-value">{currentIndicators.macd.toFixed(4)}</div>
                </div>
              )}
              {currentIndicators.bollinger_bands && (
                <div className="indicator-card">
                  <div className="indicator-label">Bollinger Bands</div>
                  <div className="indicator-value">
                    Upper: ${currentIndicators.bollinger_bands.upper?.toFixed(2)}<br />
                    Lower: ${currentIndicators.bollinger_bands.lower?.toFixed(2)}
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
                    <span className={`pattern-signal ${pattern.signal}`}>{pattern.signal}</span>
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
