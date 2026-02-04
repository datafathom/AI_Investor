import React from 'react';
import { Server, Database, Cpu, Activity, AlertTriangle, CheckCircle } from 'lucide-react';
import './SystemHealth.css';

/**
 * System Health Telemetry 
 * 
 * Kafka, Database, and Agent health monitoring dashboard.
 */
const SystemHealth = () => {
    const services = [
        { name: 'Kafka Cluster', status: 'healthy', latency: 12, icon: Activity },
        { name: 'PostgreSQL', status: 'healthy', latency: 5, icon: Database },
        { name: 'Neo4j Graph', status: 'warning', latency: 45, icon: Database },
        { name: 'Redis Cache', status: 'healthy', latency: 2, icon: Server },
    ];

    const agents = [
        { name: 'Bull Agent', load: 45, status: 'active' },
        { name: 'Bear Agent', load: 32, status: 'active' },
        { name: 'Risk Officer', load: 78, status: 'busy' },
        { name: 'Executor', load: 15, status: 'idle' },
    ];

    const kafkaTopics = [
        { name: 'market-data', lag: 0, throughput: '12.5K/s' },
        { name: 'agent-events', lag: 52, throughput: '2.1K/s' },
        { name: 'trade-signals', lag: 0, throughput: '450/s' },
    ];

    return (
        <div className="system-health">
            <div className="widget-header">
                <Server size={16} />
                <h3>System Telemetry</h3>
                <span className="overall-status healthy">All Systems Operational</span>
            </div>

            <div className="services-grid">
                {services.map((service, i) => (
                    <div key={i} className={`service-card ${service.status}`}>
                        <div className="service-icon">
                            <service.icon size={18} />
                        </div>
                        <div className="service-info">
                            <span className="service-name">{service.name}</span>
                            <span className="service-latency">{service.latency}ms</span>
                        </div>
                        {service.status === 'healthy' ? (
                            <CheckCircle size={14} className="status-icon" />
                        ) : (
                            <AlertTriangle size={14} className="status-icon" />
                        )}
                    </div>
                ))}
            </div>

            <div className="section-header">
                <Cpu size={12} />
                <span>Agent Brain Load</span>
            </div>
            <div className="agents-list">
                {agents.map((agent, i) => (
                    <div key={i} className="agent-row">
                        <span className="agent-name">{agent.name}</span>
                        <div className="load-bar">
                            <div 
                                className={`load-fill ${agent.load > 70 ? 'high' : agent.load > 40 ? 'medium' : 'low'}`}
                                style={{ width: `${agent.load}%` }}
                            ></div>
                        </div>
                        <span className="load-value">{agent.load}%</span>
                    </div>
                ))}
            </div>

            <div className="section-header">
                <Activity size={12} />
                <span>Kafka Topics</span>
            </div>
            <div className="topics-list">
                {kafkaTopics.map((topic, i) => (
                    <div key={i} className="topic-row">
                        <span className="topic-name">{topic.name}</span>
                        <span className={`topic-lag ${topic.lag > 0 ? 'has-lag' : ''}`}>
                            Lag: {topic.lag}
                        </span>
                        <span className="topic-throughput">{topic.throughput}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SystemHealth;
