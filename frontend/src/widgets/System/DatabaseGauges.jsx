import React from 'react';
import { Database, HardDrive, List } from 'lucide-react';
import useSystemHealthStore from '../../stores/systemHealthStore';
import './DatabaseGauges.css';

const DatabaseGauges = () => {
    const { postgresHealth, neo4jHealth } = useSystemHealthStore();

    return (
        <div className="database-gauges-widget">
            <div className="widget-header">
                <h3><Database size={18} className="text-blue-400" /> Database I/O & Latency</h3>
            </div>

            <div className="gauge-row">
                <div className="gauge-item">
                    <div className="gauge-circle">
                        <svg viewBox="0 0 36 36">
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#333" strokeWidth="3" />
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#3b82f6" strokeWidth="3" strokeDasharray={`${Math.min(postgresHealth.connections / 2, 100)}, 100`} />
                        </svg>
                        <div className="gauge-val">{postgresHealth.connections}</div>
                    </div>
                    <span className="gauge-label">PG Connections</span>
                </div>
                <div className="gauge-item">
                    <div className="gauge-circle">
                        <svg viewBox="0 0 36 36">
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#333" strokeWidth="3" />
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#22c55e" strokeWidth="3" strokeDasharray={`${Math.min(neo4jHealth.nodes / 1000, 100)}, 100`} />
                        </svg>
                        <div className="gauge-val">{(neo4jHealth.nodes / 1000).toFixed(1)}k</div>
                    </div>
                    <span className="gauge-label">Neo4j Nodes</span>
                </div>
            </div>

            <div className="slow-query-log">
                <h4><List size={14} /> Latency Metrics</h4>
                <div className="query-list">
                    <div className="query-item">
                        <div className="query-meta">
                            <span className="db-badge pg">PG</span>
                            <span className={`duration ${postgresHealth.queryTime > 100 ? 'text-red-500' : 'text-amber-500'}`}>{postgresHealth.queryTime}ms</span>
                        </div>
                        <code className="query-text">Avg Postgres Transaction Latency</code>
                    </div>
                    <div className="query-item">
                        <div className="query-meta">
                            <span className="db-badge neo">NEO</span>
                            <span className={`duration ${neo4jHealth.queryTime > 500 ? 'text-red-500' : 'text-amber-500'}`}>{neo4jHealth.queryTime}ms</span>
                        </div>
                        <code className="query-text">Avg Graph Traversal Latency</code>
                    </div>
                </div>
            </div>

            <div className="disk-alert">
                <HardDrive size={14} />
                <span>Disk Usage: <strong>{(postgresHealth.diskUsage * 100).toFixed(1)}%</strong> (Warning Threshold: 85%)</span>
            </div>
        </div>
    );
};

export default DatabaseGauges;
