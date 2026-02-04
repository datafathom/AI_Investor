import React from 'react';
import useMarginStore from '../../stores/marginStore';
import { ShieldAlert, Zap } from 'lucide-react';
import './DangerZone.css';

const DangerZone = () => {
    const { marginBuffer, dangerZone } = useMarginStore();

    // Calculate rotation for the gauge (0% buffer = -90deg, 100% buffer = 90deg)
    const rotation = (marginBuffer / 100) * 180 - 90;

    return (
        <div className={`danger-zone-widget ${dangerZone ? 'active' : ''}`}>
            <div className="widget-header">
                <h3><ShieldAlert size={16} /> Margin Security Gauge</h3>
            </div>

            <div className="gauge-container">
                <div className="gauge-track"></div>
                <div 
                    className="gauge-progress" 
                    style={{ 
                        transform: `rotate(${rotation}deg)`,
                        background: marginBuffer < 20 ? 'var(--urgent-accent)' : 'var(--success-accent)'
                    }}
                ></div>
                <div className="gauge-center">
                    <span className="buffer-percent">{marginBuffer.toFixed(1)}%</span>
                    <span className="buffer-label">BUFFER</span>
                </div>
            </div>

            <div className="risk-metrics">
                <div className="metric">
                    <span className="label">Health Status</span>
                    <span className={`val ${dangerZone ? 'urgent' : 'safe'}`}>
                        {dangerZone ? 'DANGER: COLLATERAL SQUEEZE' : 'OPTIMAL HOMEOTASIS'}
                    </span>
                </div>
                <div className="metric">
                    <span className="label">Pulse Mode</span>
                    <span className="val text-cyan-400">
                        <Zap size={10} className="inline mr-1" /> ACTIVE MONITORING
                    </span>
                </div>
            </div>
        </div>
    );
};

export default DangerZone;
