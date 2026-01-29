import React from 'react';
import { Database, Link, RefreshCw, Activity } from 'lucide-react';
import useAPIStore from '../../stores/apiStore';
import './DataConnectors.css';

const DataConnectors = () => {
    const { connectors, testConnector } = useAPIStore();

    return (
        <div className="data-connectors-widget">
            <div className="widget-header">
                <h3><Link size={18} className="text-blue-400" /> Third-party Data Connectors</h3>
                <div className="status-indicator">
                    <span className={`dot ${connectors.every(c => c.status === 'active' || c.status === 'healthy') ? 'healthy' : 'degraded'}`}></span>
                    <span>{connectors.every(c => c.status === 'active' || c.status === 'healthy') ? 'All Systems Operational' : 'Degraded Performance'}</span>
                </div>
            </div>

            <div className="connector-list">
                {connectors.map((connector) => (
                    <div key={connector.id} className={`connector-card ${connector.status === 'active' ? 'active' : 'inactive'}`}>
                        <div className="card-top">
                            <div className="provider-info">
                                <span className={`icon ${connector.id}`}>{connector.name.charAt(0)}</span>
                                <span className="name">{connector.name}</span>
                            </div>
                            <div className="ping-status">
                                <Activity size={12} className={connector.ping < 100 ? "text-green-400" : "text-yellow-400"} />
                                <span>{connector.ping}ms</span>
                            </div>
                        </div>
                        {connector.usage !== undefined && (
                            <div className="usage-meter">
                                <div className="meter-label">
                                    <span>Usage</span>
                                    <span>{connector.usage} / {connector.limit}</span>
                                </div>
                                <div className="meter-bg">
                                    <div className="meter-fill" style={{ width: `${(connector.usage / connector.limit) * 100}%` }}></div>
                                </div>
                            </div>
                        )}
                        {!connector.status === 'active' && (
                            <button className="connect-btn" onClick={() => testConnector(connector.id)}>Connect</button>
                        )}
                    </div>
                ))}
            </div>
            
            <div className="failover-control">
                <div className="failover-label">
                    <RefreshCw size={14} /> Auto-Failover: <strong>ENABLED</strong>
                </div>
                <div className="failover-path">Primary: Polygon → Backup: Alpha Vantage</div>
            </div>
        </div>
    );
};

export default DataConnectors;
