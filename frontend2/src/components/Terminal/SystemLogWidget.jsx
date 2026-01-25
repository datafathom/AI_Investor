import React from 'react';
import { Terminal, ShieldAlert, Zap, RefreshCw, Radio } from 'lucide-react';
import './SystemLogWidget.css';

/**
 * SystemLogWidget - Institutional-grade event monitoring
 * Mirrors high-end desktop OS console output.
 */
const SystemLogWidget = () => {
    const logs = [
        {
            id: '1',
            type: 'critical',
            title: 'Connection Severed',
            timestamp: '10:42:05',
            description: 'Market data feed lost for 200ms.',
            icon: Radio
        },
        {
            id: '2',
            type: 'warning',
            title: 'High Volatility',
            timestamp: '10:38:12',
            description: 'VIX spike detected (>25). Risk subsystem engaged.',
            icon: ShieldAlert
        },
        {
            id: '3',
            type: 'success',
            title: 'Order Filled',
            timestamp: '10:15:00',
            description: 'Bought 100 SPY @ 450.20',
            icon: Zap
        },
        {
            id: '4',
            type: 'info',
            title: 'System Update',
            timestamp: '09:00:00',
            description: 'Kernel patch v4.2.0 deployed successfully.',
            icon: RefreshCw
        }
    ];

    return (
        <div className="system-log-widget custom-scrollbar">
            <div className="log-entries">
                {logs.map((log) => {
                    const Icon = log.icon;
                    return (
                        <div key={log.id} className={`log-entry ${log.type}`}>
                            <div className="log-icon-wrapper">
                                <Icon size={14} className="log-icon" />
                            </div>
                            <div className="log-content">
                                <div className="log-header">
                                    <span className="log-title">{log.title}</span>
                                    <span className="log-timestamp">{log.timestamp}</span>
                                </div>
                                {log.description && <p className="log-description">{log.description}</p>}
                            </div>
                        </div>
                    );
                })}
            </div>
            <div className="log-footer">
                <div className="status-indicator">
                    <div className="status-dot pulse" />
                    <span>SYSTEM ANALYTICS LIVE</span>
                </div>
            </div>
        </div>
    );
};

export default SystemLogWidget;
