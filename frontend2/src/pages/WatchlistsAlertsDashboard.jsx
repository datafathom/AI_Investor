/**
 * ==============================================================================
 * FILE: frontend2/src/pages/WatchlistsAlertsDashboard.jsx
 * ROLE: Watchlists & Alerts Dashboard
 * PURPOSE: Phase 17 - Watchlist Management & Price Alerts
 *          Manages watchlists and price alerts with multi-channel notifications.
 * 
 * INTEGRATION POINTS:
 *    - WatchlistAPI: /api/watchlist endpoints
 *    - AlertAPI: /api/alert endpoints
 * 
 * FEATURES:
 *    - Multiple watchlists
 *    - Price alerts (above/below/change)
 *    - Alert history
 *    - Watchlist management
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './WatchlistsAlertsDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const WatchlistsAlertsDashboard = () => {
  const [watchlists, setWatchlists] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [newWatchlistName, setNewWatchlistName] = useState('');
  const [newSymbol, setNewSymbol] = useState('');
  const [selectedWatchlist, setSelectedWatchlist] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');

  useEffect(() => {
    loadWatchlists();
    loadAlerts();
  }, []);

  const loadWatchlists = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/watchlist/user/${userId}`);
      setWatchlists(res.data.data || []);
    } catch (error) {
      console.error('Error loading watchlists:', error);
    }
  };

  const loadAlerts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/alert/user/${userId}`);
      setAlerts(res.data.data || []);
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
  };

  const createWatchlist = async () => {
    if (!newWatchlistName) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/watchlist/create`, {
        user_id: userId,
        watchlist_name: newWatchlistName
      });
      setNewWatchlistName('');
      loadWatchlists();
    } catch (error) {
      console.error('Error creating watchlist:', error);
    } finally {
      setLoading(false);
    }
  };

  const addSymbol = async (watchlistId) => {
    if (!newSymbol) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/watchlist/${watchlistId}/add`, {
        symbol: newSymbol.toUpperCase()
      });
      setNewSymbol('');
      loadWatchlists();
    } catch (error) {
      console.error('Error adding symbol:', error);
    } finally {
      setLoading(false);
    }
  };

  const createAlert = async () => {
    if (!newSymbol) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/alert/create`, {
        user_id: userId,
        symbol: newSymbol.toUpperCase(),
        alert_type: 'price_above',
        threshold: 100,
        notification_methods: ['email']
      });
      setNewSymbol('');
      loadAlerts();
    } catch (error) {
      console.error('Error creating alert:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="watchlists-alerts-dashboard">
      <div className="dashboard-header">
        <h1>Watchlists & Price Alerts</h1>
        <p className="subtitle">Phase 17: Watchlist Management & Alert System</p>
      </div>

      <div className="dashboard-content">
        {/* Watchlists Panel */}
        <div className="watchlists-panel">
          <h2>Watchlists</h2>
          
          <div className="create-watchlist">
            <input
              type="text"
              value={newWatchlistName}
              onChange={(e) => setNewWatchlistName(e.target.value)}
              placeholder="New watchlist name"
              className="input-field"
            />
            <button onClick={createWatchlist} disabled={loading}>
              Create
            </button>
          </div>

          <div className="watchlists-list">
            {watchlists.map((watchlist) => (
              <div
                key={watchlist.watchlist_id}
                className={`watchlist-card ${selectedWatchlist?.watchlist_id === watchlist.watchlist_id ? 'selected' : ''}`}
                onClick={() => setSelectedWatchlist(watchlist)}
              >
                <h3>{watchlist.watchlist_name}</h3>
                <div className="symbol-count">{watchlist.symbols?.length || 0} symbols</div>
                {watchlist.symbols && watchlist.symbols.length > 0 && (
                  <div className="symbols-preview">
                    {watchlist.symbols.slice(0, 5).map((sym, idx) => (
                      <span key={idx} className="symbol-badge">{sym}</span>
                    ))}
                    {watchlist.symbols.length > 5 && (
                      <span className="more-symbols">+{watchlist.symbols.length - 5}</span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          {selectedWatchlist && (
            <div className="watchlist-details">
              <h3>Add Symbol</h3>
              <div className="add-symbol">
                <input
                  type="text"
                  value={newSymbol}
                  onChange={(e) => setNewSymbol(e.target.value)}
                  placeholder="Symbol (e.g., AAPL)"
                  className="input-field"
                />
                <button onClick={() => addSymbol(selectedWatchlist.watchlist_id)} disabled={loading}>
                  Add
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Alerts Panel */}
        <div className="alerts-panel">
          <h2>Price Alerts</h2>
          
          <div className="create-alert">
            <input
              type="text"
              value={newSymbol}
              onChange={(e) => setNewSymbol(e.target.value)}
              placeholder="Symbol for alert"
              className="input-field"
            />
            <button onClick={createAlert} disabled={loading}>
              Create Alert
            </button>
          </div>

          <div className="alerts-list">
            {alerts.map((alert) => (
              <div key={alert.alert_id} className="alert-card">
                <div className="alert-header">
                  <span className="alert-symbol">{alert.symbol}</span>
                  <span className={`alert-status ${alert.status}`}>{alert.status}</span>
                </div>
                <div className="alert-details">
                  <div className="alert-type">{alert.alert_type?.replace('_', ' ')}</div>
                  <div className="alert-threshold">Threshold: ${alert.threshold}</div>
                  {alert.current_price && (
                    <div className="alert-price">Current: ${alert.current_price}</div>
                  )}
                </div>
                <div className="alert-notifications">
                  {alert.notification_methods?.map((method, idx) => (
                    <span key={idx} className="notification-badge">{method}</span>
                  ))}
                </div>
              </div>
            ))}
            {alerts.length === 0 && (
              <div className="no-data">No alerts configured</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WatchlistsAlertsDashboard;
