/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedOrdersDashboard.jsx
 * ROLE: Advanced Orders & Execution Dashboard
 * PURPOSE: Phase 13 - Advanced Order Types & Smart Execution
 *          Displays advanced order types, execution algorithms, and order management.
 * 
 * INTEGRATION POINTS:
 *    - AdvancedOrdersAPI: /api/v1/advanced-orders endpoints
 * 
 * FEATURES:
 *    - Trailing stops
 *    - Bracket orders
 *    - OCO/OTO orders
 *    - Smart execution (TWAP/VWAP)
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdvancedOrdersDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const AdvancedOrdersDashboard = () => {
  const [orders, setOrders] = useState([]);
  const [orderTemplates, setOrderTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [newOrder, setNewOrder] = useState({
    symbol: '',
    quantity: '',
    order_type: 'trailing_stop',
    trailing_percent: '',
    stop_price: '',
    limit_price: ''
  });

  useEffect(() => {
    loadOrders();
    loadOrderTemplates();
  }, []);

  const loadOrders = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/advanced-orders/orders`, {
        params: { user_id: userId }
      });
      setOrders(res.data.data || []);
    } catch (error) {
      console.error('Error loading orders:', error);
    }
  };

  const loadOrderTemplates = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/advanced-orders/templates`);
      setOrderTemplates(res.data.data || []);
    } catch (error) {
      console.error('Error loading templates:', error);
    }
  };

  const placeOrder = async () => {
    if (!newOrder.symbol || !newOrder.quantity) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/advanced-orders/place`, {
        user_id: userId,
        symbol: newOrder.symbol.toUpperCase(),
        quantity: parseInt(newOrder.quantity),
        order_type: newOrder.order_type,
        trailing_percent: newOrder.trailing_percent ? parseFloat(newOrder.trailing_percent) : undefined,
        stop_price: newOrder.stop_price ? parseFloat(newOrder.stop_price) : undefined,
        limit_price: newOrder.limit_price ? parseFloat(newOrder.limit_price) : undefined
      });
      setNewOrder({
        symbol: '',
        quantity: '',
        order_type: 'trailing_stop',
        trailing_percent: '',
        stop_price: '',
        limit_price: ''
      });
      loadOrders();
    } catch (error) {
      console.error('Error placing order:', error);
    } finally {
      setLoading(false);
    }
  };

  const executeTWAP = async () => {
    if (!newOrder.symbol || !newOrder.quantity) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/advanced-orders/execute/twap`, {
        user_id: userId,
        symbol: newOrder.symbol.toUpperCase(),
        quantity: parseInt(newOrder.quantity),
        duration_minutes: 60
      });
      loadOrders();
    } catch (error) {
      console.error('Error executing TWAP:', error);
    } finally {
      setLoading(false);
    }
  };

  const executeVWAP = async () => {
    if (!newOrder.symbol || !newOrder.quantity) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/advanced-orders/execute/vwap`, {
        user_id: userId,
        symbol: newOrder.symbol.toUpperCase(),
        quantity: parseInt(newOrder.quantity)
      });
      loadOrders();
    } catch (error) {
      console.error('Error executing VWAP:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page advanced-orders-dashboard">
      <div className="dashboard-header">
        <h1>Advanced Orders & Execution</h1>
        <p className="subtitle">Phase 13: Advanced Order Types & Smart Execution</p>
      </div>

      <div className="scrollable-content-wrapper">
        <div className="dashboard-content">
          {/* Place Order */}
          <div className="place-order-panel">
            <h2>Place Advanced Order</h2>
            <div className="order-form">
              <div className="form-group">
                <span className="form-label">Symbol</span>
                <input
                  type="text"
                  placeholder="e.g. SPY"
                  value={newOrder.symbol}
                  onChange={(e) => setNewOrder({ ...newOrder, symbol: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Quantity</span>
                <input
                  type="number"
                  placeholder="0"
                  value={newOrder.quantity}
                  onChange={(e) => setNewOrder({ ...newOrder, quantity: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Order Type</span>
                <select
                  value={newOrder.order_type}
                  onChange={(e) => setNewOrder({ ...newOrder, order_type: e.target.value })}
                  className="form-input"
                >
                  <option value="trailing_stop">Trailing Stop</option>
                  <option value="bracket">Bracket Order</option>
                  <option value="oco">OCO (One-Cancels-Other)</option>
                  <option value="oto">OTO (One-Triggers-Other)</option>
                  <option value="conditional">Conditional Order</option>
                </select>
              </div>
              {newOrder.order_type === 'trailing_stop' && (
                <div className="form-group">
                  <span className="form-label">Trailing %</span>
                  <input
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    value={newOrder.trailing_percent}
                    onChange={(e) => setNewOrder({ ...newOrder, trailing_percent: e.target.value })}
                    className="form-input"
                  />
                </div>
              )}
              {(newOrder.order_type === 'bracket' || newOrder.order_type === 'oco') && (
                <>
                  <div className="form-group">
                    <span className="form-label">Stop Price</span>
                    <input
                      type="number"
                      step="0.01"
                      placeholder="0.00"
                      value={newOrder.stop_price}
                      onChange={(e) => setNewOrder({ ...newOrder, stop_price: e.target.value })}
                      className="form-input"
                    />
                  </div>
                  <div className="form-group">
                    <span className="form-label">Limit Price</span>
                    <input
                      type="number"
                      step="0.01"
                      placeholder="0.00"
                      value={newOrder.limit_price}
                      onChange={(e) => setNewOrder({ ...newOrder, limit_price: e.target.value })}
                      className="form-input"
                    />
                  </div>
                </>
              )}
              <div className="form-group flex-end">
                <button onClick={placeOrder} disabled={loading} className="place-button">
                  Place Order
                </button>
              </div>
            </div>
          </div>

          {/* Smart Execution */}
          <div className="smart-execution-panel">
            <h2>Smart Execution</h2>
            <div className="execution-form">
              <div className="form-group">
                <span className="form-label">Symbol</span>
                <input
                  type="text"
                  placeholder="e.g. BTC"
                  value={newOrder.symbol}
                  onChange={(e) => setNewOrder({ ...newOrder, symbol: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Quantity</span>
                <input
                  type="number"
                  placeholder="0"
                  value={newOrder.quantity}
                  onChange={(e) => setNewOrder({ ...newOrder, quantity: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="execution-buttons">
                <button onClick={executeTWAP} disabled={loading} className="twap-button">
                  Execute TWAP
                </button>
                <button onClick={executeVWAP} disabled={loading} className="vwap-button">
                  Execute VWAP
                </button>
              </div>
            </div>
          </div>

          {/* Order Templates */}
          <div className="templates-panel">
            <h2>Order Templates</h2>
            {orderTemplates.length > 0 ? (
              <div className="templates-list">
                {orderTemplates.map((template) => (
                  <div key={template.template_id} className="template-card">
                    <h3>{template.template_name}</h3>
                    <p className="template-description">{template.description}</p>
                    <div className="template-type">{template.order_type}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No templates available</div>
            )}
          </div>

          {/* Active Orders */}
          <div className="orders-panel">
            <h2>Active Orders</h2>
            {orders.length > 0 ? (
              <div className="orders-list">
                {orders.map((order) => (
                  <div key={order.order_id} className="order-card">
                    <div className="order-header">
                      <span className="order-symbol">{order.symbol}</span>
                      <span className={`order-status ${order.status}`}>{order.status}</span>
                    </div>
                    <div className="order-details">
                      <div className="detail-row">
                        <span>Type: {order.order_type}</span>
                        <span>Quantity: {order.quantity}</span>
                      </div>
                      {order.trailing_percent && (
                        <div className="detail-row">
                          <span>Trailing: {order.trailing_percent}%</span>
                        </div>
                      )}
                      {order.stop_price && (
                        <div className="detail-row">
                          <span>Stop: ${order.stop_price}</span>
                        </div>
                      )}
                      {order.limit_price && (
                        <div className="detail-row">
                          <span>Limit: ${order.limit_price}</span>
                        </div>
                      )}
                    </div>
                    <div className="order-actions">
                      <button className="cancel-button">Cancel</button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No active orders</div>
            )}
          </div>
        </div>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default AdvancedOrdersDashboard;
