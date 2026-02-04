/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Merchant/SquareDashboard.jsx
 * ROLE: Admin Widget
 * PURPOSE: Displays daily sales and merchant status from Square.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import useMerchantStore from '../../stores/merchantStore';
import './SquareDashboard.css';

const SquareDashboard = ({ mock = true }) => {
    const { stats, catalog, fetchStats, fetchCatalog, loading, error } = useMerchantStore();

    useEffect(() => {
        fetchStats(mock);
        fetchCatalog(mock);
        
        // Polling for live dashboard feel
        const interval = setInterval(() => {
            fetchStats(mock);
        }, 30000); // 30s refresh

        return () => clearInterval(interval);
    }, [mock, fetchStats, fetchCatalog]);

    if (error) return <div className="square-dash error">Error: {error}</div>;

    return (
        <div className="square-dash">
            <header className="dash-header">
                <div className="title-row">
                    <h3>Square Merchant Dashboard</h3>
                    <span className={`status-badge ${stats?.terminal_status === 'ONLINE' ? 'online' : 'offline'}`}>
                        {stats?.terminal_status || 'UNKNOWN'}
                    </span>
                </div>
                <p className="subtitle">Merchant ID: {stats?.merchant_id || '---'}</p>
            </header>

            {loading && !stats ? (
                <div className="loading-state">Loading Merchant Data...</div>
            ) : (
                <>
                    <div className="kpi-grid">
                        <div className="kpi-card sales">
                            <h4>Gross Sales (Today)</h4>
                            <div className="value">
                                ${(stats?.gross_sales_money?.amount / 100 || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                            </div>
                            <div className="subtext">{stats?.gross_sales_money?.currency || 'USD'}</div>
                        </div>

                        <div className="kpi-card txns">
                            <h4>Transactions</h4>
                            <div className="value">{stats?.transaction_count || 0}</div>
                            <div className="subtext">Completed</div>
                        </div>

                        <div className="kpi-card locations">
                            <h4>Active Locations</h4>
                            <div className="value">{stats?.active_locations || 0}</div>
                            <div className="subtext">Retail & Kiosks</div>
                        </div>
                    </div>

                    <div className="catalog-section">
                        <h4>Product Catalog Sync</h4>
                        <div className="catalog-list">
                            {catalog.map(item => (
                                <div key={item.id} className="catalog-item">
                                    <span className="item-name">{item.name}</span>
                                    <span className="item-price">${(item.price / 100).toFixed(2)}</span>
                                </div>
                            ))}
                            {catalog.length === 0 && <div className="empty">No items in catalog</div>}
                        </div>
                    </div>
                </>
            )}
            
            <div className="footer">
                <span className="source-label">Powered by Square</span>
                {mock && <span className="mock-label">(MOCK DATA)</span>}
            </div>
        </div>
    );
};

export default SquareDashboard;
