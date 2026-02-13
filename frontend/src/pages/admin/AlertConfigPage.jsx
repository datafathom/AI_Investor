import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './AlertConfigPage.css';

const AlertConfigPage = () => {
    const [rules, setRules] = useState([]);
    const [loading, setLoading] = useState(true);
    const [editingRule, setEditingRule] = useState(null);

    useEffect(() => {
        fetchRules();
    }, []);

    const fetchRules = async () => {
        try {
            const data = await apiClient.get('/admin/alerts/rules');
            setRules(data);
        } catch (error) {
            console.error("Error fetching rules:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (id, enabled) => {
        try {
            await apiClient.put(`/admin/alerts/rules/${id}`, { enabled });
            setRules(rules.map(r => r.id === id ? { ...r, enabled } : r));
        } catch (error) {
            console.error("Error toggling rule:", error);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("DELETE_ALERT_RULE?")) return;
        try {
            await apiClient.delete(`/admin/alerts/rules/${id}`);
            setRules(rules.filter(r => r.id !== id));
        } catch (error) {
            console.error("Error deleting rule:", error);
        }
    };

    if (loading) return <div className="alerts-loading">DECODING_THRESHOLD_MATRIX...</div>;

    return (
        <div className="alert-config-container">
            <header className="page-header">
                <div className="title-group">
                    <h1>ALERT_CRITERIA_MANAGEMENT</h1>
                    <p className="subtitle">THRESHOLD_DEFINITION_AND_NOTIFICATION_ROUTING</p>
                </div>
                <button className="add-rule-btn" onClick={() => setEditingRule({})}>NEW_RULE</button>
            </header>

            <div className="rules-grid">
                {rules.map(rule => (
                    <div key={rule.id} className={`rule-card ${rule.severity} ${rule.enabled ? '' : 'disabled'}`}>
                        <div className="rule-header">
                            <span className="severity-badge">{rule.severity.toUpperCase()}</span>
                            <h3>{rule.name}</h3>
                            <button className="delete-rule-btn" onClick={() => handleDelete(rule.id)}>×</button>
                        </div>
                        <div className="rule-body">
                            <div className="condition">
                                <label>CONDITION</label>
                                <span>{rule.metric.toUpperCase()} {rule.comparison} {rule.threshold} (FOR {rule.duration}S)</span>
                            </div>
                            <div className="channels">
                                <label>CHANNELS</label>
                                <div className="channel-list">
                                    {rule.channels.map(c => <span key={c} className="channel-tag">{c}</span>)}
                                </div>
                            </div>
                        </div>
                        <div className="rule-footer">
                            <label className="switch">
                                <input 
                                    type="checkbox" 
                                    checked={rule.enabled} 
                                    onChange={(e) => handleToggle(rule.id, e.target.checked)}
                                />
                                <span className="slider"></span>
                            </label>
                            <span className="status-text">{rule.enabled ? 'MONITORING' : 'PAUSED'}</span>
                        </div>
                    </div>
                ))}
            </div>
            
            {/* Rule Editor Modal would be rendered here when editingRule is not null */}
        </div>
    );
};

export default AlertConfigPage;
