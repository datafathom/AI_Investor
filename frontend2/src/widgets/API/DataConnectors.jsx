import React from 'react';
import { Database, Link, RefreshCw, Activity } from 'lucide-react';
import './DataConnectors.css';

const DataConnectors = () => {
    return (
        <div className="data-connectors-widget">
            <div className="widget-header">
                <h3><Link size={18} className="text-blue-400" /> Third-party Data Connectors</h3>
                <div className="status-indicator">
                    <span className="dot healthy"></span>
                    <span>All Systems Operational</span>
                </div>
            </div>

            <div className="connector-list">
                <div className="connector-card active">
                    <div className="card-top">
                        <div className="provider-info">
                            <span className="icon av">AV</span>
                            <span className="name">Alpha Vantage</span>
                        </div>
                        <div className="ping-status">
                            <Activity size={12} className="text-green-400" />
                            <span>124ms</span>
                        </div>
                    </div>
                    <div className="usage-meter">
                        <div className="meter-label">
                            <span>Daily API Calls</span>
                            <span>421 / 500</span>
                        </div>
                        <div className="meter-bg">
                            <div className="meter-fill warning" style={{ width: '84%' }}></div>
                        </div>
                    </div>
                </div>

                <div className="connector-card active">
                    <div className="card-top">
                        <div className="provider-info">
                            <span className="icon poly">P</span>
                            <span className="name">Polygon.io</span>
                        </div>
                        <div className="ping-status">
                            <Activity size={12} className="text-green-400" />
                            <span>45ms</span>
                        </div>
                    </div>
                     <div className="usage-meter">
                        <div className="meter-label">
                            <span>Monthly Bandwidth</span>
                            <span>12.5GB / 1TB</span>
                        </div>
                        <div className="meter-bg">
                            <div className="meter-fill" style={{ width: '1.2%' }}></div>
                        </div>
                    </div>
                </div>

                <div className="connector-card inactive">
                    <div className="card-top">
                        <div className="provider-info">
                             <span className="icon fred">F</span>
                            <span className="name">FRED Economic</span>
                        </div>
                        <button className="connect-btn">Connect</button>
                    </div>
                </div>
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
