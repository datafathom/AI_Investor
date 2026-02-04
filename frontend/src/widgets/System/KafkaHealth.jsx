import React from 'react';
import { Server, Activity, AlertTriangle, RefreshCw } from 'lucide-react';
import useSystemHealthStore from '../../stores/systemHealthStore';
import './KafkaHealth.css';

const KafkaHealth = () => {
    const { kafkaHealth, restartConsumer } = useSystemHealthStore();

    return (
        <div className="kafka-health-widget">
            <div className="widget-header">
                <h3><Server size={18} className="text-orange-500" /> Kafka Cluster Health</h3>
                <div className="cluster-status">
                    <span className={`dot ${kafkaHealth.status === 'healthy' ? 'online' : 'offline'}`}></span>
                    <span className="status-text">{kafkaHealth.status.toUpperCase()}</span>
                </div>
            </div>

            <div className="metrics-grid">
                <div className="metric-box">
                    <span className="label">Topics</span>
                    <span className="val">{kafkaHealth.topics?.length || 0}</span>
                </div>
                <div className="metric-box">
                    <span className="label">Msg/Sec</span>
                    <span className="val">{kafkaHealth.messagesPerSecond?.toLocaleString()}</span>
                </div>
                <div className="metric-box">
                    <span className="label">Total Lag</span>
                    <span className="val ${kafkaHealth.lag > 5000 ? 'bad' : 'good'}">{kafkaHealth.lag?.toLocaleString()}</span>
                </div>
            </div>

            <div className="topic-throughput">
                <h4>Topic Throughput (Msg/Sec)</h4>
                {kafkaHealth.topics?.map((topic, idx) => (
                    <div key={idx} className="topic-row">
                        <span className="topic-name">{topic.name}</span>
                        <div className="bar-container">
                            <div className="bar-fill" style={{ width: `${Math.min(topic.throughput / 100, 100)}%` }}></div>
                        </div>
                        <span className="throughput">{topic.throughput}</span>
                    </div>
                ))}
            </div>

            {kafkaHealth.lag > 1000 && (
                <div className="consumer-lag-alert">
                    <div className="alert-header">
                        <AlertTriangle size={14} className="text-red-500" />
                        <span>High Consumer Group Lag</span>
                    </div>
                    <div className="lag-details">
                        <span className="group-name">Main Analytics Consumer</span>
                        <span className="lag-count">Lag: {kafkaHealth.lag.toLocaleString()} msgs</span>
                    </div>
                    <button className="restart-btn" onClick={() => restartConsumer('analytics-1')}>
                        <RefreshCw size={12} /> Restart Consumer
                    </button>
                </div>
            )}
        </div>
    );
};

export default KafkaHealth;
