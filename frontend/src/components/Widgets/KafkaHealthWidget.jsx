import React, { useState, useEffect } from 'react';
import './KafkaHealthWidget.css';

const KafkaHealthWidget = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchMetrics();
        const interval = setInterval(fetchMetrics, 15000);
        return () => clearInterval(interval);
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await fetch('/api/v1/admin/kafka/metrics');
            const data = await response.json();
            setMetrics(data);
        } catch (error) {
            console.error("Error fetching Kafka metrics:", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading && !metrics) return <div className="kafka-widget-loading">SYNCING_KAFKA_OFFSETS...</div>;

    return (
        <div className="kafka-health-widget">
            <header className="widget-header">
                <h3>KAFKA_CONSUMER_HEALTH</h3>
                <span className={`broker-status ${metrics?.broker_status === 'Connected' ? 'online' : 'offline'}`}>
                    {metrics?.broker_status.toUpperCase()}
                </span>
            </header>

            <div className="metrics-summary">
                <div className="summary-item">
                    <label>TOTAL_LAG</label>
                    <value className={metrics?.total_lag > 1000 ? 'warning' : 'healthy'}>
                        {metrics?.total_lag}
                    </value>
                </div>
                <div className="summary-item">
                    <label>ACTIVE_GROUPS</label>
                    <value>{metrics?.groups.length}</value>
                </div>
            </div>

            <div className="groups-list">
                {metrics?.groups.map(group => (
                    <div key={group.group_id} className="group-card">
                        <div className="group-info">
                            <span className="group-id">{group.group_id}</span>
                            <span className="group-status">{group.status}</span>
                        </div>
                        <div className="group-stats">
                            <div className="stat">
                                <label>LAG</label>
                                <span className={group.total_lag > 100 ? 'crit' : ''}>{group.total_lag}</span>
                            </div>
                            <div className="stat">
                                <label>MEMBERS</label>
                                <span>{group.members}</span>
                            </div>
                            <div className="stat">
                                <label>PARTS</label>
                                <span>{group.partition_count}</span>
                            </div>
                        </div>
                        <div className="lag-bar">
                            <div 
                                className="lag-fill" 
                                style={{ 
                                    width: `${Math.min(100, (group.total_lag / 500) * 100)}%`,
                                    background: group.total_lag > 100 ? '#ff4757' : '#00f2ff'
                                }}
                            ></div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KafkaHealthWidget;
