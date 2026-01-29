import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, CheckCircle } from 'lucide-react';
import { telemetryService } from '../../services/telemetryService';
import './Widgets.css';

const QuotaHealthMeter = () => {
    const [quota, setQuota] = useState(telemetryService.getQuota());

    useEffect(() => {
        const unsubscribe = telemetryService.subscribe((metrics) => {
            setQuota(metrics.quota);
        });
        telemetryService.startPolling();
        return () => {
            unsubscribe();
            // We don't stop polling here because other widgets might need it
        };
    }, []);

    const percentage = quota.percentage || (quota.used / quota.total) * 100;
    const isCritical = percentage > 85;
    const isWarning = percentage > 60;

    const getColor = () => {
        if (isCritical) return '#ef4444'; // Red
        if (isWarning) return '#f59e0b'; // Amber
        return '#10b981'; // Green
    };

    return (
        <div className="widget quota-meter animate-fade-in">
            <div className="widget__header">
                <Activity size={16} className="widget__icon" />
                <span className="widget__title">API Quota Health</span>
                {isCritical ? (
                    <AlertTriangle size={14} className="text-red animate-pulse" />
                ) : (
                    <CheckCircle size={14} className="text-green" />
                )}
            </div>

            <div className="quota-meter__content">
                <svg className="quota-meter__svg" viewBox="0 0 100 100">
                    <circle
                        className="quota-meter__track"
                        cx="50" cy="50" r="45"
                    />
                    <circle
                        className="quota-meter__progress"
                        cx="50" cy="50" r="45"
                        style={{
                            stroke: getColor(),
                            strokeDasharray: `${percentage * 2.82}, 282.7`
                        }}
                    />
                    <text x="50" y="50" className="quota-meter__text">
                        {Math.round(percentage)}%
                    </text>
                </svg>

                <div className="quota-meter__details">
                    <div className="quota-meter__stat">
                        <span className="label">Used</span>
                        <span className="value">{quota.used.toLocaleString()}</span>
                    </div>
                    <div className="quota-meter__stat">
                        <span className="label">Remaining</span>
                        <span className="value">{(quota.total - quota.used).toLocaleString()}</span>
                    </div>
                </div>
            </div>

            <div className="widget__footer">
                <span className="status-text">
                    {isCritical ? 'Critical Load' : isWarning ? 'High Usage' : 'Systems Nominal'}
                </span>
            </div>
        </div>
    );
};

export default QuotaHealthMeter;
