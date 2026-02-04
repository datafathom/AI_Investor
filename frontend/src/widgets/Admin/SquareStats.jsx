/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Admin/SquareStats.jsx
 * ROLE: Square Statistics Dashboard Widget
 * PURPOSE: Displays Square merchant transaction statistics including daily/weekly/monthly
 *          volume, refund rates, and top customers by lifetime value.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/square/stats: Merchant statistics endpoint
 *     - /api/v1/square/transactions: Transaction history endpoint
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './SquareStats.css';

const API_BASE = '/square';

const SquareStats = () => {
    const [stats, setStats] = useState(null);
    const [transactions, setTransactions] = useState([]);
    const [refunds, setRefunds] = useState([]);
    const [loading, setLoading] = useState(false);
    const [timeRange, setTimeRange] = useState('daily'); // daily, weekly, monthly

    useEffect(() => {
        loadStats();
        loadTransactions();
        loadRefunds();
    }, [timeRange]);

    const loadStats = async () => {
        setLoading(true);
        try {
        try {
            const response = await apiClient.get(`${API_BASE}/stats`, { params: { range: timeRange } });
            setStats(response.data);
        } catch (err) {
            console.error('Failed to load stats:', err);
        } finally {
            setLoading(false);
        }
    };

    const loadTransactions = async () => {
        try {
        try {
            const response = await apiClient.get(`${API_BASE}/transactions`);
            const data = response.data;
            setTransactions(data.transactions || []);
        } catch (err) {
            console.error('Failed to load transactions:', err);
        }
    };

    const loadRefunds = async () => {
        try {
        try {
            const response = await apiClient.get(`${API_BASE}/refunds`);
            const data = response.data;
            setRefunds(data.refunds || []);
        } catch (err) {
            console.error('Failed to load refunds:', err);
        }
    };

    const formatCurrency = (amount) => {
        if (typeof amount === 'object' && amount.amount) {
            return `$${(amount.amount / 100).toFixed(2)}`;
        }
        return `$${amount.toFixed(2)}`;
    };

    const calculateRefundRate = () => {
        if (!stats || !refunds.length) return 0;
        const totalRefunded = refunds.reduce((sum, refund) => {
            const amount = typeof refund.amount_money === 'object' 
                ? refund.amount_money.amount / 100 
                : refund.amount_money || 0;
            return sum + amount;
        }, 0);
        const totalSales = typeof stats.gross_sales_money === 'object'
            ? stats.gross_sales_money.amount / 100
            : stats.gross_sales_money || 1;
        return ((totalRefunded / totalSales) * 100).toFixed(2);
    };

    if (loading && !stats) {
        return (
            <div className="square-stats">
                <div className="square-stats__loading">Loading statistics...</div>
            </div>
        );
    }

    return (
        <div className="square-stats">
            <div className="square-stats__header">
                <h3>💳 Square Merchant Stats</h3>
                <div className="square-stats__controls">
                    <select
                        className="time-range-select"
                        value={timeRange}
                        onChange={(e) => setTimeRange(e.target.value)}
                    >
                        <option value="daily">Daily</option>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>
            </div>

            {stats && (
                <>
                    {/* Key Metrics */}
                    <div className="square-stats__metrics">
                        <div className="metric-card">
                            <div className="metric-label">Gross Sales</div>
                            <div className="metric-value">
                                {formatCurrency(stats.gross_sales_money)}
                            </div>
                        </div>
                        <div className="metric-card">
                            <div className="metric-label">Transactions</div>
                            <div className="metric-value">
                                {stats.transaction_count || 0}
                            </div>
                        </div>
                        <div className="metric-card">
                            <div className="metric-label">Refund Rate</div>
                            <div className="metric-value">
                                {calculateRefundRate()}%
                            </div>
                        </div>
                        <div className="metric-card">
                            <div className="metric-label">Active Locations</div>
                            <div className="metric-value">
                                {stats.active_locations || 0}
                            </div>
                        </div>
                    </div>

                    {/* Terminal Status */}
                    <div className="square-stats__status">
                        <div className="status-item">
                            <span className="status-label">Terminal Status:</span>
                            <span className={`status-badge status-badge--${stats.terminal_status?.toLowerCase() || 'unknown'}`}>
                                {stats.terminal_status || 'UNKNOWN'}
                            </span>
                        </div>
                    </div>

                    {/* Recent Transactions */}
                    {transactions.length > 0 && (
                        <div className="square-stats__transactions">
                            <h4>Recent Transactions</h4>
                            <div className="transactions-list">
                                {transactions.slice(0, 10).map((txn) => (
                                    <div key={txn.id} className="transaction-item">
                                        <div className="transaction-id">{txn.id}</div>
                                        <div className="transaction-amount">
                                            {formatCurrency(txn.amount_money)}
                                        </div>
                                        <div className="transaction-status">
                                            <span className={`status-badge status-badge--${txn.status?.toLowerCase() || 'unknown'}`}>
                                                {txn.status}
                                            </span>
                                        </div>
                                        <div className="transaction-date">
                                            {new Date(txn.created_at).toLocaleDateString()}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default SquareStats;
