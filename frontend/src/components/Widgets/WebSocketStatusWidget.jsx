import React, { useState, useEffect } from 'react';
import './WebSocketStatusWidget.css';
import ConnectionPoolMeter from '../charts/ConnectionPoolMeter';

const WebSocketStatusWidget = () => {
    const [stats, setStats] = useState(null);
    const [connections, setConnections] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
        fetchConnections();
        const interval = setInterval(() => {
            fetchStats();
            fetchConnections();
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    const fetchStats = async () => {
        try {
            const response = await fetch('/api/v1/admin/websocket/stats');
            const data = await response.json();
            setStats(data);
        } catch (error) {
            console.error("Error fetching WS stats:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchConnections = async () => {
        try {
            const response = await fetch('/api/v1/admin/websocket/connections');
            const data = await response.json();
            setConnections(data);
        } catch (error) {
            console.error("Error fetching WS connections:", error);
        }
    };

    const handleDisconnect = async (connId) => {
        if (!window.confirm(`FORCE_DISCONNECT_CLIENT ${connId}?`)) return;
        try {
            await fetch(`/api/v1/admin/websocket/connections/${connId}/disconnect`, { method: 'POST' });
            fetchConnections();
        } catch (error) {
            console.error("Error disconnecting client:", error);
        }
    };

    if (loading && !stats) return <div className="ws-loading">ESTABLISHING_TELEMETRY_STREAM...</div>;

    return (
        <div className="websocket-status-widget">
            <header className="widget-header">
                <h3>WS_CORE_STATUS</h3>
                <div className="live-indicator">LIVE</div>
            </header>

            <div className="stats-hero">
                <ConnectionPoolMeter active={stats?.active} max={stats?.max} />
                <div className="throughput-stats">
                    <div className="stat-item">
                        <label>SENT</label>
                        <span className="val">{stats?.msg_out}</span>
                    </div>
                    <div className="stat-item">
                        <label>RECV</label>
                        <span className="val">{stats?.msg_in}</span>
                    </div>
                </div>
            </div>

            <div className="connections-panel">
                <h4>ACTIVE_CLIENTS ({connections.length})</h4>
                <div className="connections-list">
                    {connections.map((conn, i) => (
                        <div key={i} className="connection-row">
                            <span className="conn-id">{conn.id.substring(0, 8)}...</span>
                            <span className="conn-dept">DEPT_{conn.dept_id}</span>
                            <button className="kill-btn" onClick={() => handleDisconnect(conn.id)}>KILL</button>
                        </div>
                    ))}
                    {connections.length === 0 && <div className="no-conns">ZERO_ACTIVE_SESSIONS</div>}
                </div>
            </div>
        </div>
    );
};

export default WebSocketStatusWidget;
