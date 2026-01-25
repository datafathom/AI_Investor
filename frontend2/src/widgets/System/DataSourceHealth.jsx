/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/System/DataSourceHealth.jsx
 * ROLE: External API Monitoring Widget
 * PURPOSE: Visualizes health, latency, and quota usage of market data providers.
 *          
 * INTEGRATION POINTS:
 *     - systemApi: GET /api/v1/system/health
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import './DataSourceHealth.css';

const DataSourceHealth = () => {
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchHealth = async () => {
        try {
            const response = await fetch('/api/v1/system/health');
            if (!response.ok) throw new Error('Failed to fetch system health');
            const data = await response.json();
            
            if (data.data_sources) {
                setSources(data.data_sources);
            }
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHealth();
        const interval = setInterval(fetchHealth, 30000); // 30s refresh
        return () => clearInterval(interval);
    }, []);

    const getStatusClass = (status) => {
        switch (status) {
            case 'online': return 'status--online';
            case 'degraded': return 'status--warning';
            case 'rate_limited': return 'status--error';
            default: return 'status--offline';
        }
    };

    if (loading && sources.length === 0) return <div className="ds-health ds-health--loading">Loading Data Sources...</div>;
    if (error) return <div className="ds-health ds-health--error">Error: {error}</div>;

    return (
        <div className="ds-health">
            <div className="ds-health__header">
                <h3 className="ds-health__title">Market Data Sources</h3>
                <span className="ds-health__refresh-dot" title="Live Auto-Refresh"></span>
            </div>

            <div className="ds-health__grid">
                {sources.map(source => (
                    <div key={source.provider} className="ds-card">
                        <div className="ds-card__header">
                            <span className="ds-card__name">{source.provider.replace('_', ' ')}</span>
                            <span className={`ds-card__status ${getStatusClass(source.status)}`}>
                                {source.status.toUpperCase()}
                            </span>
                        </div>
                        
                        <div className="ds-card__metrics">
                            <div className="ds-metric">
                                <span className="ds-metric__label">Latency</span>
                                <span className="ds-metric__value">{Math.round(source.latency_ms)}ms</span>
                            </div>
                            
                            <div className="ds-metric">
                                <span className="ds-metric__label">Quota Usage</span>
                                <div className="ds-quota">
                                    <div className="ds-quota__bar">
                                        <div 
                                            className="ds-quota__fill" 
                                            style={{ 
                                                width: `${source.usage_pct}%`,
                                                backgroundColor: source.usage_pct > 80 ? '#ff4757' : (source.usage_pct > 50 ? '#ffa502' : '#00d4aa')
                                            }}
                                        ></div>
                                    </div>
                                    <span className="ds-quota__text">{source.usage_pct}%</span>
                                </div>
                            </div>
                        </div>
                        
                        <div className="ds-card__footer">
                            <span className="ds-card__time">Last check: {new Date(source.last_check).toLocaleTimeString()}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DataSourceHealth;
