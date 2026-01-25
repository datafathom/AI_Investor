/**
 * ==============================================================================
 * FILE: frontend2/src/pages/OptionsStrategyDashboard.jsx
 * ROLE: Options Strategy Builder & Analyzer Dashboard
 * PURPOSE: Phase 6 - Options Strategy Builder & Analyzer
 *          Displays options strategies, Greeks analysis, and P&L visualization.
 * 
 * INTEGRATION POINTS:
 *    - OptionsAPI: /api/v1/options endpoints
 * 
 * FEATURES:
 *    - Options strategy builder
 *    - Greeks analysis (Delta, Gamma, Theta, Vega, Rho)
 *    - P&L visualization
 *    - Options chain data
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './OptionsStrategyDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const OptionsStrategyDashboard = () => {
  const [strategy, setStrategy] = useState(null);
  const [greeks, setGreeks] = useState(null);
  const [optionsChain, setOptionsChain] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [strategyType, setStrategyType] = useState('covered_call');

  useEffect(() => {
    loadOptionsChain();
  }, [selectedSymbol]);

  const loadOptionsChain = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/options/chain`, {
        params: { symbol: selectedSymbol }
      });
      setOptionsChain(res.data.data || []);
    } catch (error) {
      console.error('Error loading options chain:', error);
    }
  };

  const buildStrategy = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/options/strategy/build`, {
        symbol: selectedSymbol,
        strategy_type: strategyType,
        legs: []
      });
      setStrategy(res.data.data);
      
      // Load Greeks for the strategy
      if (res.data.data.strategy_id) {
        const greeksRes = await axios.post(`${API_BASE}/api/v1/options/strategy/analyze`, {
          strategy_id: res.data.data.strategy_id
        });
        setGreeks(greeksRes.data.data);
      }
    } catch (error) {
      console.error('Error building strategy:', error);
    } finally {
      setLoading(false);
    }
  };

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const OptionsStrategyDashboard = () => {
  const [strategy, setStrategy] = useState(null);
  const [greeks, setGreeks] = useState(null);
  const [optionsChain, setOptionsChain] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [strategyType, setStrategyType] = useState('covered_call');

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'controls', x: 0, y: 0, w: 12, h: 2 },
      { i: 'details', x: 0, y: 2, w: 6, h: 6 },
      { i: 'greeks', x: 6, y: 2, w: 6, h: 6 },
      { i: 'chain', x: 0, y: 8, w: 12, h: 10 }
    ]
  };
  const STORAGE_KEY = 'layout_options_strategy';

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
    localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
  };

  useEffect(() => {
    loadOptionsChain();
  }, [selectedSymbol]);

  const loadOptionsChain = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/options/chain`, {
        params: { symbol: selectedSymbol }
      });
      setOptionsChain(res.data.data || []);
    } catch (error) {
      console.error('Error loading options chain:', error);
    }
  };

  const buildStrategy = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/options/strategy/build`, {
        symbol: selectedSymbol,
        strategy_type: strategyType,
        legs: []
      });
      setStrategy(res.data.data);
      
      if (res.data.data.strategy_id) {
        const greeksRes = await axios.post(`${API_BASE}/api/v1/options/strategy/analyze`, {
          strategy_id: res.data.data.strategy_id
        });
        setGreeks(greeksRes.data.data);
      }
    } catch (error) {
      console.error('Error building strategy:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page options-strategy-dashboard">
      <div className="dashboard-header">
        <h1>Options Strategy Builder</h1>
        <p className="subtitle">Phase 6: Options Strategy Builder & Analyzer</p>
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
          {/* Controls */}
          <div key="controls" className="strategy-controls-panel">
            <div className="strategy-controls">
              <div className="form-group">
                <span className="form-label">Symbol</span>
                <input
                  type="text"
                  value={selectedSymbol}
                  onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
                  placeholder="e.g. TSLA"
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Strategy Type</span>
                <select
                  value={strategyType}
                  onChange={(e) => setStrategyType(e.target.value)}
                  className="form-input"
                >
                  <option value="covered_call">Covered Call</option>
                  <option value="protective_put">Protective Put</option>
                  <option value="straddle">Straddle</option>
                  <option value="strangle">Strangle</option>
                  <option value="iron_condor">Iron Condor</option>
                  <option value="butterfly">Butterfly</option>
                </select>
              </div>
              <div className="form-group" style={{ flex: '0 0 auto', justifyContent: 'flex-end' }}>
                <button onClick={buildStrategy} disabled={loading} className="build-button">
                  {loading ? 'Building...' : 'Build Strategy'}
                </button>
              </div>
            </div>
          </div>

          {/* Strategy Details */}
          <div key="details" className="strategy-panel h-full">
            <h2>Strategy Details</h2>
            {strategy ? (
              <div className="strategy-info">
                <div className="info-item">
                  <span className="label">Strategy Type:</span>
                  <span className="value">{strategy.strategy_type}</span>
                </div>
                <div className="info-item">
                  <span className="label">Net Cost:</span>
                  <span className="value">${strategy.net_cost?.toFixed(2)}</span>
                </div>
                <div className="info-item">
                  <span className="label">Max Profit:</span>
                  <span className="value" style={{ color: '#00ff88' }}>
                    ${strategy.max_profit?.toFixed(2)}
                  </span>
                </div>
                <div className="info-item">
                  <span className="label">Max Loss:</span>
                  <span className="value" style={{ color: '#ff4444' }}>
                    ${strategy.max_loss?.toFixed(2)}
                  </span>
                </div>
                <div className="info-item">
                  <span className="label">Breakeven:</span>
                  <span className="value">${strategy.breakeven?.toFixed(2)}</span>
                </div>
              </div>
            ) : (
                <div className="no-data">Build a strategy to see details</div>
            )}
          </div>

          {/* Greeks Analysis */}
          <div key="greeks" className="greeks-panel h-full">
            <h2>Greeks Analysis</h2>
            {greeks ? (
              <div className="greeks-grid">
                <div className="greek-card">
                  <div className="greek-label">Delta</div>
                  <div className="greek-value">{greeks.delta?.toFixed(4)}</div>
                </div>
                <div className="greek-card">
                  <div className="greek-label">Gamma</div>
                  <div className="greek-value">{greeks.gamma?.toFixed(4)}</div>
                </div>
                <div className="greek-card">
                  <div className="greek-label">Theta</div>
                  <div className="greek-value" style={{ color: '#ff4444' }}>
                    {greeks.theta?.toFixed(4)}
                  </div>
                </div>
                <div className="greek-card">
                  <div className="greek-label">Vega</div>
                  <div className="greek-value">{greeks.vega?.toFixed(4)}</div>
                </div>
                <div className="greek-card">
                  <div className="greek-label">Rho</div>
                  <div className="greek-value">{greeks.rho?.toFixed(4)}</div>
                </div>
              </div>
            ) : (
                <div className="no-data">Analyze a strategy to see Greeks</div>
            )}
          </div>

          {/* Options Chain */}
          <div key="chain" className="options-chain-panel h-full">
            <h2>Options Chain - {selectedSymbol}</h2>
            {optionsChain.length > 0 ? (
              <div className="chain-table">
                <div className="chain-header">
                  <span>Strike</span>
                  <span>Call Bid</span>
                  <span>Call Ask</span>
                  <span>Put Bid</span>
                  <span>Put Ask</span>
                </div>
                {optionsChain.slice(0, 20).map((option, idx) => (
                  <div key={idx} className="chain-row">
                    <span className="strike">${option.strike}</span>
                    <span>${option.call_bid?.toFixed(2)}</span>
                    <span>${option.call_ask?.toFixed(2)}</span>
                    <span>${option.put_bid?.toFixed(2)}</span>
                    <span>${option.put_ask?.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No data available</div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default OptionsStrategyDashboard;
