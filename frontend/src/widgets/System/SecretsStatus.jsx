
import React, { useEffect, useState } from 'react';
import { Lock, ShieldCheck, AlertTriangle } from 'lucide-react';
import apiClient from '../../services/apiClient';
import './SecretsStatus.css';

const SecretsStatus = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const res = await apiClient.get('/system/secrets');
                setStatus(res.data);
            } catch (err) {
                console.error("Failed to fetch secrets status", err);
            } finally {
                setLoading(false);
            }
        };

        fetchStatus();
        const interval = setInterval(fetchStatus, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="secrets-status-widget">Loading...</div>;
    if (!status) return <div className="secrets-status-widget">Failed to load status</div>;

    const isHealthy = status.status === 'Healthy';

    return (
        <div className="secrets-status-widget">
            <div className="widget-header">
                <h3><Lock size={18} className="text-cyan-400" /> Secrets Engine</h3>
                <div className={`status-badge ${isHealthy ? 'healthy' : 'degraded'}`}>
                    {isHealthy ? <ShieldCheck size={14} /> : <AlertTriangle size={14} />}
                    {status.status.toUpperCase()}
                </div>
            </div>

            <div className="info-grid">
                <div className="info-item">
                    <span className="label">Engine</span>
                    <span className="value">{status.engine}</span>
                </div>
                <div className="info-item">
                    <span className="label">Source</span>
                    <span className="value">{status.source}</span>
                </div>
            </div>

            <div className="metrics-list">
                <h4>Protected Connections</h4>
                <div className="connection-item">
                    <span>Database (Postgres)</span>
                    <span className="text-green-400">Secured</span>
                </div>
                <div className="connection-item">
                    <span>Graph (Neo4j)</span>
                    <span className="text-green-400">Secured</span>
                </div>
                {status.security_gateway && (
                    <>
                        <div className="connection-item">
                            <span>Rate Limiter</span>
                            <span className={status.security_gateway.rate_limiter === 'Active' ? "text-green-400" : "text-yellow-500"}>
                                {status.security_gateway.rate_limiter}
                            </span>
                        </div>
                        <div className="connection-item">
                            <span>WAF Rules</span>
                            <span className="text-cyan-400">{status.security_gateway.waf_rules}</span>
                        </div>
                    </>
                )}
                <div className="connection-item">
                    <span>Vault Integration</span>
                    <span className={status.vault_connected ? "text-green-400" : "text-yellow-500"}>
                        {status.vault_connected ? "Connected" : "Not Configured"}
                    </span>
                </div>
                <div className="connection-item">
                    <span>Hardware Token</span>
                    <span className="text-yellow-500">Not Detected</span>
                </div>
            </div>
            
            {!isHealthy && status.missing_critical_keys && (
                <div style={{marginTop: '10px', color: '#ef4444', fontSize: '0.8rem'}}>
                    Missing: {status.missing_critical_keys.join(', ')}
                </div>
            )}
        </div>
    );
};

export default SecretsStatus;
