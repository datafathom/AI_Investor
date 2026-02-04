import React, { useState, useEffect } from 'react';
import { Cpu, Zap } from 'lucide-react';
import { telemetryService } from '../../services/telemetryService';
import './Widgets.css';

const SystemLoadRibbon = () => {
    const [load, setLoad] = useState(telemetryService.getSystemLoad());

    useEffect(() => {
        const unsubscribe = telemetryService.subscribe((metrics) => {
            setLoad(metrics.systemLoad);
        });
        return () => unsubscribe();
    }, []);

    const maxLoad = Math.max(...load, 100);
    const avgLoad = load.length > 0 ? Math.round(load.reduce((a, b) => a + b, 0) / load.length) : 0;

    return (
        <div className="widget system-load animate-fade-in">
            <div className="widget__header">
                <Cpu size={16} className="widget__icon" />
                <span className="widget__title">System Load Ribbon</span>
                <span className={`load-badge ${avgLoad > 70 ? 'critical' : avgLoad > 40 ? 'warning' : 'nominal'}`}>
                    {avgLoad}%
                </span>
            </div>

            <div className="system-load__ribbon">
                <div className="ribbon-container">
                    {load.map((val, idx) => (
                        <div 
                            key={idx} 
                            className="ribbon-bar"
                            style={{ 
                                height: `${(val / maxLoad) * 100}%`,
                                backgroundColor: val > 75 ? '#ef4444' : val > 50 ? '#f59e0b' : '#6366f1'
                            }}
                        />
                    ))}
                </div>
            </div>

            <div className="widget__footer">
                <div className="load-details">
                    <Zap size={12} className="text-amber" />
                    <span>Kafka Ingest: Nominal</span>
                </div>
                <span>24-core cluster</span>
            </div>
        </div>
    );
};

export default SystemLoadRibbon;
