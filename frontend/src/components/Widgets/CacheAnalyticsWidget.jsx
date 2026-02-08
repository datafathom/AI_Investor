import React, { useState, useEffect } from 'react';
import './CacheAnalyticsWidget.css';

const CacheAnalyticsWidget = () => {
    const [cacheData, setCacheData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [invalidating, setInvalidating] = useState(false);

    useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 10000);
        return () => clearInterval(interval);
    }, []);

    const fetchStats = async () => {
        try {
            const response = await fetch('/api/v1/admin/cache/stats');
            const data = await response.json();
            setCacheData(data);
        } catch (error) {
            console.error("Error fetching cache stats:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleInvalidate = async (cacheName) => {
        if (!window.confirm(`Are you sure you want to invalidate ${cacheName}?`)) return;
        
        setInvalidating(true);
        try {
            await fetch(`/api/v1/admin/cache/${cacheName}/invalidate?pattern=*`, { method: 'POST' });
            fetchStats();
        } catch (error) {
            console.error("Error invalidating cache:", error);
        } finally {
            setInvalidating(false);
        }
    };

    if (loading && !cacheData) return <div className="cache-widget-loading">LOADING_CACHE_METRICS...</div>;

    return (
        <div className="cache-analytics-widget">
            <header className="widget-header">
                <h3>CACHE_ANALYTICS</h3>
                <button className="refresh-btn" onClick={fetchStats}></button>
            </header>

            <div className="cache-grid">
                {Object.entries(cacheData || {}).map(([name, stats]) => (
                    <div key={name} className="cache-card">
                        <div className="cache-title">
                            <h4>{name.replace('_', ' ').toUpperCase()}</h4>
                            <span className="cache-type">{stats.type}</span>
                        </div>
                        
                        <div className="metric-row">
                            <div className="metric">
                                <label>KEYS</label>
                                <value>{stats.key_count}</value>
                            </div>
                            <div className="metric">
                                <label>MEMORY</label>
                                <value>{stats.memory_used_mb.toFixed(2)} MB</value>
                            </div>
                        </div>

                        <div className="progress-container">
                            <label>MEMORY_UTILIZATION</label>
                            <div className="progress-bar">
                                <div 
                                    className="progress-fill" 
                                    style={{ width: `${Math.min(100, (stats.memory_used_mb / stats.memory_max_mb) * 100)}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="hit-rate-container">
                            <div className="hit-rate-labels">
                                <span>HIT_RATE: {(stats.hit_rate * 100).toFixed(1)}%</span>
                                <span>MISS: {(stats.miss_rate * 100).toFixed(1)}%</span>
                            </div>
                            <div className="hit-rate-bar">
                                <div className="hit-fill" style={{ width: `${stats.hit_rate * 100}%` }}></div>
                                <div className="miss-fill" style={{ width: `${stats.miss_rate * 100}%` }}></div>
                            </div>
                        </div>

                        <button 
                            className="invalidate-btn" 
                            disabled={invalidating}
                            onClick={() => handleInvalidate(name)}
                        >
                            {invalidating ? 'INVALIDATING...' : 'INVALIDATE_CACHE'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CacheAnalyticsWidget;
