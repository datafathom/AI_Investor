
import React, { useState, useEffect } from 'react';
import { Shield, RefreshCw, Key, ArrowRight, CheckCircle, XCircle, Info } from 'lucide-react';
import './BrokerageConnectivityWidget.css';

const BrokerageConnectivityWidget = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [connecting, setConnecting] = useState(false);

    const fetchStatus = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/v1/brokerage/status', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            setStatus(data);
        } catch (e) {
            console.error("Failed to fetch brokerage status", e);
        } finally {
            setLoading(false);
        }
    };

    const handleConnect = async () => {
        setConnecting(true);
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('/api/v1/brokerage/connect', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                setTimeout(fetchStatus, 1000); // Wait for simulation to "propagate"
            }
        } catch (e) {
            console.error("Connection failed", e);
        } finally {
            setTimeout(() => setConnecting(false), 2000);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, []);

    const isConnected = status?.status?.includes('CONNECTED');
    const isError = status?.status === 'ERROR';

    return (
        <div className={`broker-conn-widget ${isConnected ? 'active' : ''}`}>
            <div className="broker-header">
                <div className="title-area">
                    <Shield className="icon-shield" />
                    <h3>Brokerage Gate</h3>
                </div>
                {status && (
                    <div className={`status-pill ${isConnected ? 'status-green' : isError ? 'status-red' : 'status-gray'}`}>
                        {isConnected ? <CheckCircle size={14} /> : <XCircle size={14} />}
                        {status.status}
                    </div>
                )}
            </div>

            <div className="broker-content">
                {!isConnected ? (
                    <div className="connect-view">
                        <p>Link your Alpaca or IBKR account to enable live trade execution and real-time portfolio tracking.</p>
                        <div className="input-sim">
                            <Key size={16} />
                            <span>API Keys required for production</span>
                        </div>
                        <button className="connect-btn" onClick={handleConnect} disabled={connecting}>
                            {connecting ? "Handshaking..." : "Establish Connection"}
                            <ArrowRight size={16} />
                        </button>
                    </div>
                ) : (
                    <div className="info-view">
                        <div className="account-summary">
                            <div className="sum-item">
                                <span className="label">Managed Equity</span>
                                <span className="val">${status.equity?.toLocaleString()}</span>
                            </div>
                            <div className="sum-item">
                                <span className="label">Buying Power</span>
                                <span className="val">${status.buying_power?.toLocaleString()}</span>
                            </div>
                        </div>
                        <div className="broker-tags">
                            <span className="tag">{status.broker}</span>
                            <span className="tag">{status.currency}</span>
                            {status.is_paper && <span className="tag highlight">Paper Trading</span>}
                        </div>
                        <div className="disclaimer">
                            <Info size={12} />
                            AI Execution is currently monitored by Guardian Shield.
                        </div>
                    </div>
                )}
            </div>

            <div className="broker-footer">
                <span className="label">Uptime: 99.98%</span>
                <button className="refresh-mini" onClick={fetchStatus} disabled={loading}>
                    <RefreshCw size={12} className={loading ? 'spinning' : ''} />
                </button>
            </div>
        </div>
    );
};

export default BrokerageConnectivityWidget;
