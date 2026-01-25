import React from 'react';
import { Database, HardDrive, List } from 'lucide-react';
import './DatabaseGauges.css';

const DatabaseGauges = () => {
    return (
        <div className="database-gauges-widget">
            <div className="widget-header">
                <h3><Database size={18} className="text-blue-400" /> Database I/O & Memory Pressure</h3>
            </div>

            <div className="gauge-row">
                <div className="gauge-item">
                    <div className="gauge-circle">
                        <svg viewBox="0 0 36 36">
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#333" strokeWidth="3" />
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#3b82f6" strokeWidth="3" strokeDasharray="65, 100" />
                        </svg>
                        <div className="gauge-val">65%</div>
                    </div>
                    <span className="gauge-label">Postgres WAL</span>
                </div>
                <div className="gauge-item">
                    <div className="gauge-circle">
                        <svg viewBox="0 0 36 36">
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#333" strokeWidth="3" />
                            <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#22c55e" strokeWidth="3" strokeDasharray="92, 100" />
                        </svg>
                        <div className="gauge-val">92%</div>
                    </div>
                    <span className="gauge-label">Neo4j Cache Hit</span>
                </div>
            </div>

            <div className="slow-query-log">
                <h4><List size={14} /> Slow Query Log (>100ms)</h4>
                <div className="query-list">
                    <div className="query-item">
                        <div className="query-meta">
                            <span className="db-badge pg">PG</span>
                            <span className="duration text-amber-500">245ms</span>
                        </div>
                        <code className="query-text">SELECT * FROM market_ticks WHERE symbol = 'AAPL' ORDER...</code>
                    </div>
                    <div className="query-item">
                        <div className="query-meta">
                            <span className="db-badge neo">NEO</span>
                            <span className="duration text-red-500">1.2s</span>
                        </div>
                        <code className="query-text">MATCH (a:Asset)-[:CORRELATED]->(b:Asset) WHERE...</code>
                    </div>
                </div>
            </div>

            <div className="disk-alert">
                <HardDrive size={14} />
                <span>Disk Usage: <strong>82%</strong> (Warning Threshold: 85%)</span>
            </div>
        </div>
    );
};

export default DatabaseGauges;
