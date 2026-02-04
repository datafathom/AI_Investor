/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Crypto/CoinbaseTrade.jsx
 * ROLE: Coinbase Trading Widget
 * PURPOSE: Displays available trading pairs and order form for Coinbase
 *          institutional crypto trading.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/coinbase/trading-pairs: Available pairs
 *     - /api/v1/coinbase/orders: Order placement and history
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './CoinbaseTrade.css';

const API_BASE = '/coinbase';

const CoinbaseTrade = () => {
    const [tradingPairs, setTradingPairs] = useState([]);
    const [selectedPair, setSelectedPair] = useState('');
    const [orderType, setOrderType] = useState('market');
    const [side, setSide] = useState('buy');
    const [amount, setAmount] = useState('');
    const [price, setPrice] = useState('');
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadTradingPairs();
        loadOrders();
    }, []);

    const loadTradingPairs = async () => {
        try {
        try {
            const response = await apiClient.get(`${API_BASE}/trading-pairs`);
            const data = response.data;
            setTradingPairs(data.trading_pairs || []);
            if (data.trading_pairs?.length > 0) {
                setSelectedPair(data.trading_pairs[0]);
            }
        } catch (err) {
            console.error('Failed to load trading pairs:', err);
        }
    };

    const loadOrders = async () => {
        try {
            const response = await apiClient.get(`${API_BASE}/orders`, { params: { limit: 10 } });
            const data = response.data;
            setOrders(data.orders || []);
        } catch (err) {
            console.error('Failed to load orders:', err);
        }
    };

    const handleSubmitOrder = async (e) => {
        e.preventDefault();
        
        if (!selectedPair || !amount) {
            setError('Please select a trading pair and enter amount');
            return;
        }

        if (orderType === 'limit' && !price) {
            setError('Please enter limit price');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const orderConfig = orderType === 'market' 
                ? { market_market_ioc: { quote_size: amount } }
                : { limit_limit_gtc: { base_size: amount, limit_price: price } };

            const response = await apiClient.post(`${API_BASE}/orders`, {
                product_id: selectedPair,
                side: side,
                order_configuration: orderConfig
            });

            const data = response.data;
            
            // Reload orders
            await loadOrders();
            
            // Reset form
            setAmount('');
            setPrice('');

        } catch (err) {
            console.error('Order submission failed:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="coinbase-trade">
            <div className="coinbase-trade__header">
                <h3>🏦 Coinbase Institutional Trading</h3>
            </div>

            {/* Trading Pairs */}
            {tradingPairs.length > 0 && (
                <div className="coinbase-trade__pairs">
                    <label>Trading Pair</label>
                    <select
                        value={selectedPair}
                        onChange={(e) => setSelectedPair(e.target.value)}
                        className="coinbase-trade__select"
                    >
                        {tradingPairs.map((pair) => (
                            <option key={pair} value={pair}>
                                {pair}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {/* Order Form */}
            <form onSubmit={handleSubmitOrder} className="coinbase-trade__form">
                <div className="coinbase-trade__row">
                    <div className="coinbase-trade__field">
                        <label>Side</label>
                        <select
                            value={side}
                            onChange={(e) => setSide(e.target.value)}
                            className="coinbase-trade__select"
                        >
                            <option value="buy">Buy</option>
                            <option value="sell">Sell</option>
                        </select>
                    </div>

                    <div className="coinbase-trade__field">
                        <label>Order Type</label>
                        <select
                            value={orderType}
                            onChange={(e) => setOrderType(e.target.value)}
                            className="coinbase-trade__select"
                        >
                            <option value="market">Market</option>
                            <option value="limit">Limit</option>
                        </select>
                    </div>
                </div>

                <div className="coinbase-trade__field">
                    <label>Amount</label>
                    <input
                        type="number"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        placeholder={orderType === 'market' ? 'Quote size' : 'Base size'}
                        className="coinbase-trade__input"
                        required
                    />
                </div>

                {orderType === 'limit' && (
                    <div className="coinbase-trade__field">
                        <label>Limit Price</label>
                        <input
                            type="number"
                            value={price}
                            onChange={(e) => setPrice(e.target.value)}
                            placeholder="Enter limit price"
                            className="coinbase-trade__input"
                            required
                        />
                    </div>
                )}

                {error && (
                    <div className="coinbase-trade__error">
                        ⚠️ {error}
                    </div>
                )}

                <button
                    type="submit"
                    className="coinbase-trade__submit"
                    disabled={loading}
                >
                    {loading ? 'Placing Order...' : 'Place Order'}
                </button>
            </form>

            {/* Recent Orders */}
            {orders.length > 0 && (
                <div className="coinbase-trade__orders">
                    <h4>Recent Orders</h4>
                    <div className="orders-list">
                        {orders.map((order, idx) => (
                            <div key={idx} className="order-item">
                                <div className="order-item__info">
                                    <div className="order-item__pair">{order.product_id}</div>
                                    <div className={`order-item__side order-item__side--${order.side}`}>
                                        {order.side.toUpperCase()}
                                    </div>
                                    <div className="order-item__type">{order.order_type}</div>
                                </div>
                                <div className={`order-item__status order-item__status--${order.status}`}>
                                    {order.status}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CoinbaseTrade;
