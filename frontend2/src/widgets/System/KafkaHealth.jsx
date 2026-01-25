import React from 'react';
import { Server, Activity, AlertTriangle, RefreshCw } from 'lucide-react';
import './KafkaHealth.css';

const KafkaHealth = () => {
    return (
        <div className="kafka-health-widget">
            <div className="widget-header">
                <h3><Server size={18} className="text-orange-500" /> Kafka Cluster Health</h3>
                <div className="cluster-status">
                    <span className="dot online"></span>
                    <span className="status-text">HEALTHY</span>
                </div>
            </div>

            <div className="metrics-grid">
                <div className="metric-box">
                    <span className="label">Total Brokers</span>
                    <span className="val">3</span>
                </div>
                <div className="metric-box">
                    <span className="label">Msg/Sec In</span>
                    <span className="val">4,281</span>
                </div>
                <div className="metric-box">
                    <span className="label">Under-Replicated</span>
                    <span className="val good">0</span>
                </div>
            </div>

            <div className="topic-throughput">
                <h4>Topic Throughput (Msg/Sec)</h4>
                <div className="topic-row">
                    <span className="topic-name">market-data.ticks</span>
                    <div className="bar-container">
                        <div className="bar-fill" style={{ width: '85%' }}></div>
                    </div>
                    <span className="throughput">2,400</span>
                </div>
                <div className="topic-row">
                    <span className="topic-name">agent.signals</span>
                    <div className="bar-container">
                        <div className="bar-fill" style={{ width: '45%' }}></div>
                    </div>
                    <span className="throughput">850</span>
                </div>
                <div className="topic-row">
                    <span className="topic-name">system.logs</span>
                    <div className="bar-container">
                        <div className="bar-fill" style={{ width: '60%' }}></div>
                    </div>
                    <span className="throughput">1,031</span>
                </div>
            </div>

            <div className="consumer-lag-alert">
                <div className="alert-header">
                    <AlertTriangle size={14} className="text-red-500" />
                    <span>Consumer Group Lag Alert</span>
                </div>
                <div className="lag-details">
                    <span className="group-name">analytics-engine-pro-1</span>
                    <span className="lag-count">Lag: 4,200 msgs</span>
                </div>
                <button className="restart-btn">
                    <RefreshCw size={12} /> Restart Consumer
                </button>
            </div>
        </div>
    );
};

export default KafkaHealth;
