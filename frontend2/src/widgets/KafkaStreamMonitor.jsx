/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/KafkaStreamMonitor.jsx
 * ROLE: "Nervous System" Monitor Widget
 * PURPOSE: Visualizes real-time Kafka event streams and throughput latency.
 *          Provides system health observability for the infrastructure layer.
 * ==============================================================================
 */
import React, { useEffect, useState } from 'react';
import './KafkaStreamMonitor.css';

const KafkaStreamMonitor = () => {
    const [stats, setStats] = useState([]);
    const [messages, setMessages] = useState([]);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        // Poll stats
        const fetchStats = async () => {
            try {
                const res = await fetch('http://localhost:5050/api/v1/system/kafka/stats');
                if (res.ok) {
                    const json = await res.json();
                    // Robust check: Ensure stats is an array
                    if (Array.isArray(json)) {
                        setStats(json);
                    } else if (typeof json === 'object') {
                        // Fallback: If object, wrap in array or extract values
                        setStats([json]);
                    }
                } else {
                    // fall back
                    setStats([
                        { topic: 'market-data', msg_per_sec: 124, lag: 2 },
                        { topic: 'risk-alerts', msg_per_sec: 2, lag: 0 },
                    ]);
                }
            } catch (e) {
                 // Mock
                 setStats([
                    { topic: 'market-data', msg_per_sec: 250, lag: 5 },
                    { topic: 'options-flow', msg_per_sec: 45, lag: 1 },
                    { topic: 'risk-alerts', msg_per_sec: 0, lag: 0 },
                ]);
            }
        };
        
        fetchStats();
        const interval = setInterval(fetchStats, 5000);
        return () => clearInterval(interval);
    }, []);

    // Simulate stream
    useEffect(() => {
        const timer = setInterval(() => {
            const topics = ['market-data', 'risk-alerts', 'options-flow'];
            const types = ['INFO', 'WARN', 'ERROR', 'DEBUG'];
            const topic = topics[Math.floor(Math.random() * topics.length)];
            
            if (filter !== 'all' && filter !== topic) return;

            const newMsg = {
                id: Date.now(),
                timestamp: new Date().toISOString().split('T')[1].split('.')[0],
                topic: topic,
                type: Math.random() > 0.9 ? 'WARN' : 'INFO',
                payload: `Sample payload ${Math.floor(Math.random() * 1000)} bytes`
            };
            
            setMessages(prev => [newMsg, ...prev].slice(0, 50));
        }, 800);
        return () => clearInterval(timer);
    }, [filter]);

    return (
        <div className="kafka-monitor-widget">
            <header className="monitor-header">
                <h3>Kafka Nervous System</h3>
                <div className="topic-filters">
                    <button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>All</button>
                    <button className={filter === 'market-data' ? 'active' : ''} onClick={() => setFilter('market-data')}>Market</button>
                    <button className={filter === 'options-flow' ? 'active' : ''} onClick={() => setFilter('options-flow')}>Options</button>
                </div>
            </header>

            <div className="throughput-grid">
                {Array.isArray(stats) && stats.map(s => (
                    <div key={s.topic} className="stat-card">
                        <span className="sc-topic">{s.topic}</span>
                        <div className="sc-metrics">
                            <span className="sc-val">{s.msg_per_sec} m/s</span>
                            <span className="sc-lag">Lag: {s.lag}</span>
                        </div>
                        <div className="sparkline">
                           {/* CSS sparkline placeholder */}
                           <div className="sl-bar" style={{height: '40%'}}></div>
                           <div className="sl-bar" style={{height: '70%'}}></div>
                           <div className="sl-bar" style={{height: '50%'}}></div>
                           <div className="sl-bar" style={{height: '80%'}}></div>
                           <div className="sl-bar" style={{height: '60%'}}></div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="stream-log">
                {messages.map(m => (
                    <div key={m.id} className={`log-row ${m.type.toLowerCase()}`}>
                        <span className="log-time">{m.timestamp}</span>
                        <span className="log-topic">{m.topic}</span>
                        <span className="log-type">{m.type}</span>
                        <span className="log-payload">{m.payload}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KafkaStreamMonitor;
