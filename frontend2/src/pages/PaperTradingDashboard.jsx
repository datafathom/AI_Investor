/**
 * ==============================================================================
 * FILE: frontend2/src/pages/PaperTradingDashboard.jsx
 * ROLE: Paper Trading & Simulation Dashboard
 * PURPOSE: Phase 14 - Paper Trading & Simulation
 *          Displays virtual portfolios, paper trades, and backtesting results.
 * 
 * INTEGRATION POINTS:
 *    - PaperTradingAPI: /api/v1/paper-trading endpoints
 * 
 * FEATURES:
 *    - Virtual portfolio management
 *    - Paper trade execution
 *    - Backtesting
 *    - Performance tracking
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PaperTradingDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const PaperTradingDashboard = () => {
  const [virtualPortfolio, setVirtualPortfolio] = useState(null);
  const [paperTrades, setPaperTrades] = useState([]);
  const [backtestResults, setBacktestResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newTrade, setNewTrade] = useState({ symbol: '', quantity: '', order_type: 'market' });

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'trade', x: 0, y: 0, w: 12, h: 2 },
      { i: 'portfolio', x: 0, y: 2, w: 7, h: 8 },
      { i: 'trades', x: 7, y: 2, w: 5, h: 8 },
      { i: 'backtest', x: 0, y: 10, w: 12, h: 4 }
    ]
  };
  const STORAGE_KEY = 'layout_paper_trading';

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
    loadVirtualPortfolio();
    loadPaperTrades();
  }, []);

  const loadVirtualPortfolio = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/paper-trading/portfolio`, {
        params: { user_id: userId }
      });
      setVirtualPortfolio(res.data.data);
    } catch (error) {
      console.error('Error loading virtual portfolio:', error);
    }
  };

  const loadPaperTrades = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/paper-trading/trades`, {
        params: { user_id: userId, limit: 20 }
      });
      setPaperTrades(res.data.data || []);
    } catch (error) {
      console.error('Error loading paper trades:', error);
    }
  };

  const placePaperTrade = async () => {
    if (!newTrade.symbol || !newTrade.quantity) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/paper-trading/trade`, {
        user_id: userId,
        symbol: newTrade.symbol.toUpperCase(),
        quantity: parseInt(newTrade.quantity),
        order_type: newTrade.order_type
      });
      setNewTrade({ symbol: '', quantity: '', order_type: 'market' });
      loadVirtualPortfolio();
      loadPaperTrades();
    } catch (error) {
      console.error('Error placing paper trade:', error);
    } finally {
      setLoading(false);
    }
  };

  const runBacktest = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/v1/paper-trading/backtest`, {
        user_id: userId,
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        initial_capital: 100000
      });
      setBacktestResults(res.data.data);
    } catch (error) {
      console.error('Error running backtest:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page paper-trading-dashboard">
      <div className="dashboard-header">
        <h1>Paper Trading & Simulation</h1>
        <p className="subtitle">Phase 14: Paper Trading & Simulation</p>
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
          {/* Place Trade */}
          <div key="trade" className="trade-panel">
            <h2>Place Paper Trade</h2>
            <div className="trade-form">
              <div className="form-group">
                <span className="form-label">Symbol</span>
                <input
                  type="text"
                  placeholder="e.g. AAPL"
                  value={newTrade.symbol}
                  onChange={(e) => setNewTrade({ ...newTrade, symbol: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Quantity</span>
                <input
                  type="number"
                  placeholder="0"
                  value={newTrade.quantity}
                  onChange={(e) => setNewTrade({ ...newTrade, quantity: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Order Type</span>
                <select
                  value={newTrade.order_type}
                  onChange={(e) => setNewTrade({ ...newTrade, order_type: e.target.value })}
                  className="form-input"
                >
                  <option value="market">Market</option>
                  <option value="limit">Limit</option>
                  <option value="stop">Stop</option>
                </select>
              </div>
              <div className="form-group" style={{ flex: '0 0 auto', justifyContent: 'flex-end' }}>
                <button onClick={placePaperTrade} disabled={loading} className="trade-button">
                  Place Trade
                </button>
              </div>
            </div>
          </div>

          {/* Virtual Portfolio */}
          <div key="portfolio" className="portfolio-panel h-full">
            <h2>Virtual Portfolio</h2>
            {virtualPortfolio ? (
              <>
                <div className="portfolio-metrics">
                  <div className="metric-card">
                    <div className="metric-label">Total Value</div>
                    <div className="metric-value">${virtualPortfolio.total_value?.toFixed(2)}</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-label">Cash Balance</div>
                    <div className="metric-value">${virtualPortfolio.cash_balance?.toFixed(2)}</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-label">Total P&L</div>
                    <div className="metric-value" style={{ color: virtualPortfolio.total_pnl >= 0 ? '#00ff88' : '#ff4444' }}>
                      ${virtualPortfolio.total_pnl?.toFixed(2)}
                    </div>
                  </div>
                </div>
                {virtualPortfolio.holdings && virtualPortfolio.holdings.length > 0 && (
                  <div className="holdings-list">
                    <h3>Holdings</h3>
                    {virtualPortfolio.holdings.map((holding, idx) => (
                      <div key={idx} className="holding-item">
                        <span className="symbol">{holding.symbol}</span>
                        <span className="quantity">{holding.quantity}</span>
                        <span className={`pnl ${holding.pnl >= 0 ? 'positive' : 'negative'}`}>
                          ${holding.pnl?.toFixed(2)}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
                <div className="no-data">Loading portfolio...</div>
            )}
          </div>

          {/* Recent Trades */}
          <div key="trades" className="trades-panel h-full">
            <h2>Recent Paper Trades</h2>
            {paperTrades.length > 0 ? (
              <div className="trades-list">
                {paperTrades.map((trade) => (
                  <div key={trade.trade_id} className="trade-item">
                    <div className="trade-info">
                      <span className="trade-symbol">{trade.symbol}</span>
                      <span className="trade-action">{trade.action}</span>
                      <span className="trade-quantity">{trade.quantity}</span>
                    </div>
                    <div className="trade-details">
                      <span className={trade.pnl >= 0 ? 'positive' : 'negative'}>
                        ${trade.pnl?.toFixed(2)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No trades yet</div>
            )}
          </div>

          {/* Backtesting */}
          <div key="backtest" className="backtest-panel h-full">
            <h2>Backtesting</h2>
            <button onClick={runBacktest} disabled={loading} className="backtest-button">
              {loading ? 'Running...' : 'Run Backtest'}
            </button>
            {backtestResults && (
              <div className="backtest-results">
                <div className="result-metric">
                  <span className="label">Total Return:</span>
                  <span className="value" style={{ color: backtestResults.total_return >= 0 ? '#00ff88' : '#ff4444' }}>
                    {(backtestResults.total_return * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="result-metric">
                  <span className="label">Sharpe Ratio:</span>
                  <span className="value">{backtestResults.sharpe_ratio?.toFixed(2)}</span>
                </div>
                <div className="result-metric">
                  <span className="label">Win Rate:</span>
                  <span className="value">{(backtestResults.win_rate * 100).toFixed(1)}%</span>
                </div>
              </div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default PaperTradingDashboard;
