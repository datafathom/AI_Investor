import React from 'react';
import './MonitoringDashboard.css';
import LatencyHeatmapWidget from '../../components/widgets/LatencyHeatmapWidget';
import WebSocketStatusWidget from '../../components/widgets/WebSocketStatusWidget';

const MonitoringDashboard = () => {
    return (
        <div className="monitoring-dashboard-container">
            <header className="page-header">
                <div className="title-group">
                    <h1>SYSTEM_PERFORMANCE_MONITOR</h1>
                    <p className="subtitle">REAL_TIME_LATENCY_AND_STREAM_METRICS</p>
                </div>
            </header>
            
            <div className="dashboard-grid">
                <div className="grid-item latency-item">
                    <LatencyHeatmapWidget />
                </div>
                <div className="grid-item websocket-item">
                    <WebSocketStatusWidget />
                </div>
            </div>
        </div>
    );
};

export default MonitoringDashboard;
