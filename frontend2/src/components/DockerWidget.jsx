import React, { useState, useEffect, useCallback } from 'react';
import './DockerWidget.css';

const STATE_COLORS = {
    running: '#22c55e',
    exited: '#ef4444',
    paused: '#f59e0b',
    created: '#3b82f6',
    restarting: '#8b5cf6',
};

const DockerWidget = ({ onToast }) => {
    const [containers, setContainers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [actionLoading, setActionLoading] = useState({});

    const fetchContainers = useCallback(async () => {
        try {
            const response = await fetch('/api/docker/containers');
            if (!response.ok) throw new Error('Failed to fetch containers');
            const data = await response.json();
            setContainers(data);
            setError(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchContainers();
        const interval = setInterval(fetchContainers, 10000); // Refresh every 10s
        return () => clearInterval(interval);
    }, [fetchContainers]);

    const handleAction = async (containerId, action) => {
        setActionLoading(prev => ({ ...prev, [containerId]: action }));
        try {
            const method = action === 'remove' ? 'DELETE' : 'POST';
            const url = action === 'remove'
                ? `/api/docker/containers/${containerId}?force=true`
                : `/api/docker/containers/${containerId}/${action}`;

            const response = await fetch(url, { method });
            const result = await response.json();

            if (!response.ok) throw new Error(result.error);

            if (onToast) onToast({ type: 'success', message: result.message });
            fetchContainers();
        } catch (err) {
            if (onToast) onToast({ type: 'error', message: err.message });
        } finally {
            setActionLoading(prev => ({ ...prev, [containerId]: null }));
        }
    };

    if (loading) {
        return (
            <div className="docker-widget-content">
                <div className="docker-loading">
                    <div className="spinner"></div>
                    <span>Connecting to Docker...</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="docker-widget-content">
                <div className="docker-error">
                    <span className="error-icon"></span>
                    <span>{error}</span>
                    <button onClick={fetchContainers} className="retry-btn">Retry</button>
                </div>
            </div>
        );
    }

    return (
        <div className="docker-widget-content">
            <div className="docker-header">
                <span className="container-count">{containers.length} container{containers.length !== 1 ? 's' : ''}</span>
                <button onClick={fetchContainers} className="refresh-btn" title="Refresh"></button>
            </div>

            {containers.length === 0 ? (
                <div className="docker-empty">No containers found</div>
            ) : (
                <div className="container-list">
                    {containers.map(container => (
                        <div key={container.id} className={`container-card ${container.state}`}>
                            <div className="container-info">
                                <div className="container-name">
                                    <span
                                        className="status-dot"
                                        style={{ background: STATE_COLORS[container.state] || '#6b7280' }}
                                    />
                                    {container.name}
                                </div>
                                <div className="container-meta">
                                    <span className="container-image">{container.image}</span>
                                    <span className="container-status">{container.status}</span>
                                </div>
                            </div>
                            <div className="container-actions">
                                {container.state === 'running' ? (
                                    <>
                                        <button
                                            onClick={() => handleAction(container.id, 'stop')}
                                            disabled={!!actionLoading[container.id]}
                                            className="action-btn stop"
                                            title="Stop"
                                        >
                                            {actionLoading[container.id] === 'stop' ? '...' : ''}
                                        </button>
                                        <button
                                            onClick={() => handleAction(container.id, 'restart')}
                                            disabled={!!actionLoading[container.id]}
                                            className="action-btn restart"
                                            title="Restart"
                                        >
                                            {actionLoading[container.id] === 'restart' ? '...' : ''}
                                        </button>
                                    </>
                                ) : (
                                    <button
                                        onClick={() => handleAction(container.id, 'start')}
                                        disabled={!!actionLoading[container.id]}
                                        className="action-btn start"
                                        title="Start"
                                    >
                                        {actionLoading[container.id] === 'start' ? '...' : ''}
                                    </button>
                                )}
                                <button
                                    onClick={() => handleAction(container.id, 'remove')}
                                    disabled={!!actionLoading[container.id]}
                                    className="action-btn remove"
                                    title="Remove"
                                >
                                    {actionLoading[container.id] === 'remove' ? '...' : ''}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default DockerWidget;
