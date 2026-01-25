import React, { useState, useEffect } from 'react';
import { ShieldAlert, Activity, PauseCircle, PlayCircle, Filter, Loader2 } from 'lucide-react';
import useComplianceStore from '../../stores/complianceStore';
import './AbuseMonitor.css';

const AbuseMonitor = () => {
    const { sarAlerts, isMonitoring, isLoading, fetchSarAlerts, pauseAgent } = useComplianceStore();
    const [pausedAgents, setPausedAgents] = useState({});

    useEffect(() => {
        fetchSarAlerts();
        const interval = setInterval(fetchSarAlerts, 10000); // Poll for live abuse
        return () => clearInterval(interval);
    }, [fetchSarAlerts]);
    
    // Filter for abuse-related types
    const abuseAlerts = sarAlerts.filter(a => ['spoofing', 'layering', 'wash_trading'].includes(a.type));

    const toggleAgentPause = (agentId) => {
        if (!pausedAgents[agentId]) {
            pauseAgent(agentId);
        }
        setPausedAgents(prev => ({
            ...prev,
            [agentId]: !prev[agentId]
        }));
    };

    return (
        <div className="abuse-monitor-widget">
            <div className="widget-header">
                <h3><ShieldAlert size={18} className="text-red-500" /> Real-time 'Anti-Market Abuse' Monitoring</h3>
                <div className="header-actions">
                    <button className="icon-btn"><Filter size={14}/></button>
                    <span className={`status-badge ${isMonitoring ? 'live' : 'off'}`}>
                        {isMonitoring ? 'LIVE' : 'IDLE'}
                    </span>
                </div>
            </div>

            <div className="monitor-stats">
                <div className="stat-item">
                    <div className="label">Abuse Flags</div>
                    <div className="value text-red-500">{abuseAlerts.length}</div>
                </div>
                <div className="stat-item">
                    <div className="label">System Health</div>
                    <div className="value text-slate-400">99.8%</div>
                </div>
                <div className="stat-item">
                    <div className="label">Agents Paused</div>
                    <div className="value text-amber-500">
                        {Object.values(pausedAgents).filter(Boolean).length}
                    </div>
                </div>
            </div>

            <div className="alerts-feed">
                {isLoading && abuseAlerts.length === 0 ? (
                    <div className="p-8 flex justify-center"><Loader2 className="animate-spin" /></div>
                ) : abuseAlerts.length === 0 ? (
                    <div className="p-8 text-center text-slate-500">No abuse patterns detected.</div>
                ) : (
                    abuseAlerts.map(alert => (
                        <div key={alert.id} className={`alert-card risk-${alert.severity.toLowerCase()}`}>
                            <div className="alert-header">
                                <span className="alert-type">{alert.type.toUpperCase()}</span>
                                <span className="alert-time">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                            </div>
                            <div className="alert-body">
                                <div className="agent-info">
                                    <span className="agent-name">{alert.agent_id || 'Global Scanner'}</span>
                                    {alert.agent_id && (
                                        <button 
                                            className={`pause-btn ${pausedAgents[alert.agent_id] ? 'resume' : 'pause'}`}
                                            onClick={() => toggleAgentPause(alert.agent_id)}
                                        >
                                            {pausedAgents[alert.agent_id] ? <PlayCircle size={14}/> : <PauseCircle size={14}/>}
                                            {pausedAgents[alert.agent_id] ? 'RESUME' : 'PAUSE'}
                                        </button>
                                    )}
                                </div>
                                <p className="alert-details">{alert.description}</p>
                                <div className="evidence-score">
                                    Confidence: {(alert.evidence_score * 100).toFixed(1)}%
                                </div>
                            </div>
                            <div className="alert-footer">
                                <button className="action-btn">Analyze</button>
                                <button className="action-btn">Dismiss</button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default AbuseMonitor;
