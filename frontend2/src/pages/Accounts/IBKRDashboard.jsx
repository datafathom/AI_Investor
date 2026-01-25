/**
 * ==============================================================================
 * FILE: frontend2/src/pages/Accounts/IBKRDashboard.jsx
 * ROLE: Interactive Brokers Account Dashboard
 * PURPOSE: Displays IBKR account status, positions with P&L, margin requirements,
 *          and currency exposure for professional users.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/ibkr/account-summary: Account summary endpoint
 *     - /api/v1/ibkr/positions: Positions endpoint
 *     - /api/v1/ibkr/margin: Margin requirements endpoint
 *     - /api/v1/ibkr/currency-exposure: Currency exposure endpoint
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import './IBKRDashboard.css';

const API_BASE = '/api/v1/ibkr';

const IBKRDashboard = () => {
    const [accountSummary, setAccountSummary] = useState(null);
    const [positions, setPositions] = useState([]);
    const [margin, setMargin] = useState(null);
    const [currencyExposure, setCurrencyExposure] = useState([]);
    const [loading, setLoading] = useState(false);
    const [gatewayStatus, setGatewayStatus] = useState(null);

    useEffect(() => {
        loadAllData();
        // Refresh every 30 seconds
        const interval = setInterval(loadAllData, 30000);
        return () => clearInterval(interval);
    }, []);

    const loadAllData = async () => {
        setLoading(true);
        try {
            await Promise.all([
                loadAccountSummary(),
                loadPositions(),
                loadMargin(),
                loadCurrencyExposure(),
                loadGatewayStatus()
            ]);
        } finally {
            setLoading(false);
        }
    };

    const loadAccountSummary = async () => {
        try {
            const response = await fetch(`${API_BASE}/account-summary`);
            if (response.ok) {
                const data = await response.json();
                setAccountSummary(data);
            }
        } catch (err) {
            console.error('Failed to load account summary:', err);
        }
    };

    const loadPositions = async () => {
        try {
            const response = await fetch(`${API_BASE}/positions`);
            if (response.ok) {
                const data = await response.json();
                setPositions(data.positions || []);
            }
        } catch (err) {
            console.error('Failed to load positions:', err);
        }
    };

    const loadMargin = async () => {
        try {
            const response = await fetch(`${API_BASE}/margin`);
            if (response.ok) {
                const data = await response.json();
                setMargin(data);
            }
        } catch (err) {
            console.error('Failed to load margin:', err);
        }
    };

    const loadCurrencyExposure = async () => {
        try {
            const response = await fetch(`${API_BASE}/currency-exposure`);
            if (response.ok) {
                const data = await response.json();
                setCurrencyExposure(data.currency_exposure || []);
            }
        } catch (err) {
            console.error('Failed to load currency exposure:', err);
        }
    };

    const loadGatewayStatus = async () => {
        try {
            const response = await fetch(`${API_BASE}/gateway/status`);
            if (response.ok) {
                const data = await response.json();
                setGatewayStatus(data);
            }
        } catch (err) {
            console.error('Failed to load gateway status:', err);
        }
    };

    const formatCurrency = (value) => {
        if (typeof value === 'string') {
            value = parseFloat(value);
        }
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(value);
    };

    const formatPercent = (value) => {
        return `${parseFloat(value).toFixed(2)}%`;
    };

    const getPnlColor = (pnl) => {
        const pnlValue = parseFloat(pnl);
        if (pnlValue > 0) return '#34a853';
        if (pnlValue < 0) return '#ea4335';
        return '#9aa0a6';
    };

    if (loading && !accountSummary) {
        return (
            <div className="ibkr-dashboard">
                <div className="ibkr-dashboard__loading">Loading IBKR account data...</div>
            </div>
        );
    }

    return (
        <div className="ibkr-dashboard">
            <div className="ibkr-dashboard__header">
                <h2>🏦 Interactive Brokers Account</h2>
                {gatewayStatus && (
                    <div className={`gateway-status gateway-status--${gatewayStatus.status?.toLowerCase()}`}>
                        Gateway: {gatewayStatus.status}
                    </div>
                )}
            </div>

            {/* Account Summary */}
            {accountSummary && (
                <div className="ibkr-dashboard__summary">
                    <div className="summary-grid">
                        <div className="summary-card">
                            <div className="summary-label">Net Liquidation</div>
                            <div className="summary-value">
                                {formatCurrency(accountSummary.NetLiquidation)}
                            </div>
                        </div>
                        <div className="summary-card">
                            <div className="summary-label">Buying Power</div>
                            <div className="summary-value">
                                {formatCurrency(accountSummary.BuyingPower)}
                            </div>
                        </div>
                        <div className="summary-card">
                            <div className="summary-label">Available Funds</div>
                            <div className="summary-value">
                                {formatCurrency(accountSummary.AvailableFunds)}
                            </div>
                        </div>
                        <div className="summary-card">
                            <div className="summary-label">Excess Liquidity</div>
                            <div className="summary-value">
                                {formatCurrency(accountSummary.ExcessLiquidity)}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Margin Requirements */}
            {margin && (
                <div className="ibkr-dashboard__margin">
                    <h3>Margin Requirements</h3>
                    <div className="margin-info">
                        <div className="margin-item">
                            <span className="margin-label">Initial Margin:</span>
                            <span className="margin-value">{formatCurrency(margin.init_margin_req)}</span>
                        </div>
                        <div className="margin-item">
                            <span className="margin-label">Maintenance Margin:</span>
                            <span className="margin-value">{formatCurrency(margin.maint_margin_req)}</span>
                        </div>
                        <div className="margin-item">
                            <span className="margin-label">Utilization:</span>
                            <span className="margin-value">{margin.utilization_pct.toFixed(1)}%</span>
                        </div>
                        <div className="margin-item">
                            <span className="margin-label">Cushion:</span>
                            <span className="margin-value">{formatPercent(margin.cushion * 100)}</span>
                        </div>
                    </div>
                    <div className="margin-bar">
                        <div
                            className="margin-bar__fill"
                            style={{
                                width: `${Math.min(margin.utilization_pct, 100)}%`,
                                backgroundColor: margin.utilization_pct > 80 ? '#ea4335' : margin.utilization_pct > 60 ? '#fbbc04' : '#34a853'
                            }}
                        />
                    </div>
                </div>
            )}

            {/* Currency Exposure */}
            {currencyExposure.length > 0 && (
                <div className="ibkr-dashboard__currency">
                    <h3>Currency Exposure</h3>
                    <div className="currency-list">
                        {currencyExposure.map((exp, idx) => (
                            <div key={idx} className="currency-item">
                                <div className="currency-code">{exp.currency}</div>
                                <div className="currency-exposure">
                                    {formatCurrency(exp.exposure)}
                                </div>
                                <div className="currency-percentage">
                                    {exp.percentage.toFixed(2)}%
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Positions */}
            <div className="ibkr-dashboard__positions">
                <h3>Positions ({positions.length})</h3>
                {positions.length === 0 ? (
                    <div className="no-positions">No open positions</div>
                ) : (
                    <div className="positions-table">
                        <div className="positions-header">
                            <div>Symbol</div>
                            <div>Type</div>
                            <div>Position</div>
                            <div>Avg Cost</div>
                            <div>Market Price</div>
                            <div>Market Value</div>
                            <div>Unrealized P&L</div>
                        </div>
                        {positions.map((pos, idx) => (
                            <div key={idx} className="position-row">
                                <div className="position-symbol">{pos.symbol}</div>
                                <div className="position-type">{pos.sec_type}</div>
                                <div className="position-qty">{pos.position}</div>
                                <div className="position-cost">{formatCurrency(pos.avg_cost)}</div>
                                <div className="position-price">{formatCurrency(pos.market_price)}</div>
                                <div className="position-value">{formatCurrency(pos.market_value)}</div>
                                <div
                                    className="position-pnl"
                                    style={{ color: getPnlColor(pos.unrealized_pnl) }}
                                >
                                    {formatCurrency(pos.unrealized_pnl)}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default IBKRDashboard;
