import React, { useState, useEffect } from 'react';
import { Globe, Wifi, WifiOff } from 'lucide-react';
import { telemetryService } from '../../services/telemetryService';
import './Widgets.css';

const LatencyGlobalMap = () => {
    const [latency, setLatency] = useState(telemetryService.getLatency());

    useEffect(() => {
        const unsubscribe = telemetryService.subscribe((metrics) => {
            setLatency(metrics.latency);
        });
        return () => unsubscribe();
    }, []);

    const getStatusColor = (ms) => {
        if (!ms) return 'rgba(255,255,255,0.1)';
        if (ms < 100) return '#10b981'; // Green
        if (ms < 200) return '#f59e0b'; // Amber
        return '#ef4444'; // Red
    };

    const regions = [
        { id: 'us-east', name: 'US East', ms: latency['us-east'] },
        { id: 'us-west', name: 'US West', ms: latency['us-west'] },
        { id: 'eu-central', name: 'EU Central', ms: latency['eu-central'] },
        { id: 'ap-southeast', name: 'Asia Pacific', ms: latency['ap-southeast'] },
    ];

    return (
        <div className="widget latency-map animate-fade-in">
            <div className="widget__header">
                <Globe size={16} className="widget__icon" />
                <span className="widget__title">Global Provider Lag</span>
            </div>

            <div className="latency-map__grid">
                {regions.map(region => (
                    <div key={region.id} className="latency-map__region">
                        <div className="region-name">{region.name}</div>
                        <div className="region-stat">
                            <div 
                                className="status-dot" 
                                style={{ backgroundColor: getStatusColor(region.ms) }}
                            />
                            <span className="ms-value">{region.ms ? `${region.ms}ms` : '---'}</span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="widget__footer">
                <div className="connection-status">
                    <Wifi size={12} className="text-green" />
                    <span>Real-time Sync Active</span>
                </div>
            </div>
        </div>
    );
};

export default LatencyGlobalMap;
