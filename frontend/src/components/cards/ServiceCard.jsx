import React, { useState, useEffect } from 'react';
import './ServiceCard.css';
import UptimeSparkline from '../charts/UptimeSparkline';

const ServiceCard = ({ service }) => {
    const [expanded, setExpanded] = useState(false);
    const [history, setHistory] = useState([]);
    const [historyLoading, setHistoryLoading] = useState(false);

    const toggleExpand = async () => {
        const nextState = !expanded;
        setExpanded(nextState);
        
        if (nextState && history.length === 0) {
            setHistoryLoading(true);
            try {
                const response = await fetch(`/api/v1/admin/health/services/${service.id}/history`);
                const data = await response.json();
                setHistory(data);
            } catch (error) {
                console.error("Error fetching uptime history:", error);
            } finally {
                setHistoryLoading(false);
            }
        }
    };

    const handleManualCheck = async (e) => {
        e.stopPropagation();
        try {
            await fetch(`/api/v1/admin/health/services/${service.id}/check`, { method: 'POST' });
            // In a real app, this would trigger a global refresh or local update
        } catch (error) {
            console.error("Error triggering manual check:", error);
        }
    };

    return (
        <div className={`service-card ${service.status.toLowerCase()} ${expanded ? 'expanded' : ''}`} onClick={toggleExpand}>
            <div className="card-top">
                <div className="service-info">
                    <span className="service-name">{service.name}</span>
                    <span className="service-target">{service.target}</span>
                </div>
                <div className="service-status-badge">
                    {service.status}
                </div>
            </div>

            <div className="card-main">
                <div className="main-stat">
                    <label>LATENCY</label>
                    <span className="latency-val">{service.latency_ms}ms</span>
                </div>
                <button className="recheck-btn" onClick={handleManualCheck}>RESCAN</button>
            </div>

            {expanded && (
                <div className="card-expanded">
                    <label>30_DAY_UPTIME_HISTORY</label>
                    {historyLoading ? (
                        <div className="history-loading">LOADING_TIMELINE...</div>
                    ) : (
                        <UptimeSparkline data={history} />
                    )}
                </div>
            )}
        </div>
    );
};

export default ServiceCard;
