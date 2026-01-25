/**
 * ==============================================================================
 * FILE: frontend2/src/pages/SocialTradingDashboard.jsx
 * ROLE: Social Trading Dashboard
 * PURPOSE: Phase 19 - Social Trading & Copy Trading
 *          Displays trader leaderboard, follow/unfollow, and copy trading settings.
 * 
 * INTEGRATION POINTS:
 *    - SocialTradingAPI: /api/v1/social-trading endpoints
 * 
 * FEATURES:
 *    - Trader discovery
 *    - Performance ranking
 *    - Follow/unfollow
 *    - Copy trading
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SocialTradingDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const SocialTradingDashboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [followedTraders, setFollowedTraders] = useState([]);
  const [copyTrades, setCopyTrades] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');

  useEffect(() => {
    loadLeaderboard();
    loadFollowedTraders();
    loadCopyTrades();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/social-trading/leaderboard`, {
        params: { limit: 20 }
      });
      setLeaderboard(res.data.data || []);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    }
  };

  const loadFollowedTraders = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/social-trading/following`, {
        params: { user_id: userId }
      });
      setFollowedTraders(res.data.data || []);
    } catch (error) {
      console.error('Error loading followed traders:', error);
    }
  };

  const loadCopyTrades = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/social-trading/copy-trades`, {
        params: { user_id: userId }
      });
      setCopyTrades(res.data.data || []);
    } catch (error) {
      console.error('Error loading copy trades:', error);
    }
  };

  const followTrader = async (traderId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/social-trading/follow`, {
        user_id: userId,
        trader_id: traderId
      });
      loadFollowedTraders();
      loadLeaderboard();
    } catch (error) {
      console.error('Error following trader:', error);
    } finally {
      setLoading(false);
    }
  };

  const startCopyTrading = async (traderId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/social-trading/copy-trading/start`, {
        user_id: userId,
        trader_id: traderId,
        allocation_percent: 10
      });
      loadCopyTrades();
    } catch (error) {
      console.error('Error starting copy trading:', error);
    } finally {
      setLoading(false);
    }
  };

  const getReturnColor = (returnPercent) => {
    if (returnPercent > 0) return '#00ff88';
    if (returnPercent < 0) return '#ff4444';
    return '#888';
  };

  return (
    <div className="social-trading-dashboard">
      <div className="dashboard-header">
        <h1>Social Trading</h1>
        <p className="subtitle">Phase 19: Social Trading & Copy Trading</p>
      </div>

      <div className="dashboard-content">
        {/* Leaderboard */}
        <div className="leaderboard-panel">
          <h2>Top Traders</h2>
          {leaderboard.length > 0 ? (
            <div className="leaderboard-list">
              {leaderboard.map((trader, idx) => (
                <div key={trader.trader_id} className="trader-card">
                  <div className="trader-rank">#{idx + 1}</div>
                  <div className="trader-info">
                    <h3>{trader.trader_name || `Trader ${trader.trader_id}`}</h3>
                    <div className="trader-stats">
                      <span className="stat">
                        Return: <span style={{ color: getReturnColor(trader.total_return) }}>
                          {(trader.total_return * 100).toFixed(2)}%
                        </span>
                      </span>
                      <span className="stat">Followers: {trader.follower_count || 0}</span>
                      <span className="stat">Win Rate: {(trader.win_rate * 100 || 0).toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className="trader-actions">
                    <button
                      onClick={() => followTrader(trader.trader_id)}
                      disabled={loading}
                      className="follow-button"
                    >
                      Follow
                    </button>
                    <button
                      onClick={() => startCopyTrading(trader.trader_id)}
                      disabled={loading}
                      className="copy-button"
                    >
                      Copy Trade
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No traders available</div>
          )}
        </div>

        {/* Followed Traders */}
        <div className="following-panel">
          <h2>Following</h2>
          {followedTraders.length > 0 ? (
            <div className="following-list">
              {followedTraders.map((trader) => (
                <div key={trader.trader_id} className="followed-trader-card">
                  <h3>{trader.trader_name || `Trader ${trader.trader_id}`}</h3>
                  <div className="trader-performance">
                    <span>Return: <span style={{ color: getReturnColor(trader.total_return) }}>
                      {(trader.total_return * 100).toFixed(2)}%
                    </span></span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">Not following any traders</div>
          )}
        </div>

        {/* Copy Trading */}
        <div className="copy-trading-panel">
          <h2>Active Copy Trades</h2>
          {copyTrades.length > 0 ? (
            <div className="copy-trades-list">
              {copyTrades.map((copyTrade) => (
                <div key={copyTrade.copy_trade_id} className="copy-trade-card">
                  <div className="copy-header">
                    <h3>{copyTrade.trader_name || `Trader ${copyTrade.trader_id}`}</h3>
                    <span className={`status ${copyTrade.status}`}>{copyTrade.status}</span>
                  </div>
                  <div className="copy-details">
                    <div className="detail-item">
                      <span className="label">Allocation:</span>
                      <span className="value">{copyTrade.allocation_percent}%</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">Copied Trades:</span>
                      <span className="value">{copyTrade.trades_copied || 0}</span>
                    </div>
                    <div className="detail-item">
                      <span className="label">Total P&L:</span>
                      <span className="value" style={{ color: copyTrade.total_pnl >= 0 ? '#00ff88' : '#ff4444' }}>
                        ${copyTrade.total_pnl?.toFixed(2) || 0}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No active copy trades</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SocialTradingDashboard;
