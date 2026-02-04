/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Ops/IncidentDashboard.jsx
 * ROLE: Ops Dashboard
 * PURPOSE: Monitor and manage system incidents.
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import useIncidentStore from '../../stores/incidentStore';
import './IncidentDashboard.css';

const IncidentDashboard = ({ mock = true }) => {
    const { incidents, fetchIncidents, triggerIncident, loading, triggering, error } = useIncidentStore();
    const [title, setTitle] = useState('');
    
    useEffect(() => {
        fetchIncidents(mock);
        // Poll for updates every 10s
        const interval = setInterval(() => fetchIncidents(mock), 10000);
        return () => clearInterval(interval);
    }, [mock, fetchIncidents]);

    const handleTrigger = async () => {
        if (!title) return;
        await triggerIncident(title, "high", mock);
        setTitle('');
    };

    const getStatusColor = (status) => {
        switch(status) {
            case 'triggered': return '#dc2626'; // Red
            case 'acknowledged': return '#d97706'; // Orange
            case 'resolved': return '#059669'; // Green
            default: return '#6b7280';
        }
    };

    return (
        <div className="incident-dashboard">
            <header className="dash-header">
                <h3>Ops Incidents</h3>
                <span className="pd-logo">PagerDuty</span>
            </header>

            <div className="trigger-section">
                <input 
                    type="text" 
                    placeholder="Describe incident..."
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <button 
                    className="trigger-btn" 
                    onClick={handleTrigger}
                    disabled={triggering || !title}
                >
                    {triggering ? 'Triggering...' : 'Trigger Incident'}
                </button>
            </div>

            <div className="incident-list">
                {loading && incidents.length === 0 && <div className="loading">Loading...</div>}
                {error && <div className="error-msg">{error}</div>}
                
                {incidents.map((inc) => (
                    <div key={inc.id} className="incident-card" style={{ borderLeftColor: getStatusColor(inc.status) }}>
                        <div className="inc-header">
                            <span className="inc-id">{inc.id}</span>
                            <span className={`inc-urgency ${inc.urgency}`}>{inc.urgency.toUpperCase()}</span>
                        </div>
                        <div className="inc-title">{inc.title}</div>
                        <div className="inc-meta">
                            <span className="inc-status" style={{ color: getStatusColor(inc.status) }}>
                                {inc.status.toUpperCase()}
                            </span>
                            <span className="inc-time">{new Date(inc.created_at).toLocaleTimeString()}</span>
                        </div>
                    </div>
                ))}
                
                {!loading && incidents.length === 0 && (
                    <div className="empty-state">All systems operational.</div>
                )}
            </div>

            <div className="footer">
                <span> {mock && '(Mock)'}</span>
            </div>
        </div>
    );
};

export default IncidentDashboard;
