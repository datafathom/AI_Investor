import React, { useEffect } from 'react';
import { Compass, AlertTriangle, ShieldCheck, Activity } from 'lucide-react';
import useInstitutionalStore from '../../stores/institutionalStore';
import './ClientHealthCompass.css';

const ClientHealthCompass = ({ clientId }) => {
    const { riskLevels, fetchRiskLevels, loading } = useInstitutionalStore();

    useEffect(() => {
        if (clientId) fetchRiskLevels(clientId);
    }, [clientId, fetchRiskLevels]);

    const riskData = riskLevels[clientId] || {
        volatility_score: 0,
        drawdown_risk: 0,
        liquidity_score: 0,
        health_status: 'Unknown',
        alerts: []
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'Healthy': return 'text-success';
            case 'Warning': return 'text-warning';
            case 'Critical': return 'text-error';
            default: return 'text-slate-500';
        }
    };

    if (loading && !riskLevels[clientId]) {
        return <div className="client-health-compass-loading glass-premium">Analyzing Risk...</div>;
    }

    return (
        <div className="client-health-compass glass-premium p-6 rounded-3xl border border-white/5">
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-slate-400 text-xs uppercase tracking-widest font-bold flex items-center gap-2">
                        <Compass size={14} className="text-primary" />
                        Client Health Compass
                    </h3>
                    <div className={`text-2xl font-bold mt-1 ${getStatusColor(riskData.health_status)}`}>
                        {riskData.health_status}
                    </div>
                </div>
                <div className="w-12 h-12 rounded-full border-2 border-primary/20 flex items-center justify-center">
                    <Activity size={20} className="text-primary animate-pulse" />
                </div>
            </div>

            <div className="space-y-4 mb-6">
                <div className="risk-metric">
                    <div className="flex justify-between text-[10px] uppercase font-bold mb-1">
                        <span className="text-slate-500">Volatility Score</span>
                        <span className="text-white">{riskData.volatility_score}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-primary transition-all duration-1000" 
                            style={{ width: `${riskData.volatility_score}%` }}
                        />
                    </div>
                </div>

                <div className="risk-metric">
                    <div className="flex justify-between text-[10px] uppercase font-bold mb-1">
                        <span className="text-slate-500">Drawdown Risk</span>
                        <span className="text-white">{riskData.drawdown_risk}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-warning transition-all duration-1000" 
                            style={{ width: `${riskData.drawdown_risk}%` }}
                        />
                    </div>
                </div>

                <div className="risk-metric">
                    <div className="flex justify-between text-[10px] uppercase font-bold mb-1">
                        <span className="text-slate-500">Liquidity Score</span>
                        <span className="text-white">{riskData.liquidity_score}%</span>
                    </div>
                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                        <div 
                            className="h-full bg-success transition-all duration-1000" 
                            style={{ width: `${riskData.liquidity_score}%` }}
                        />
                    </div>
                </div>
            </div>

            <div className="space-y-2">
                {riskData.alerts.map((alert, idx) => (
                    <div key={idx} className="flex items-center gap-2 p-2 rounded-lg bg-white/5 border border-white/5 text-[10px]">
                        <AlertTriangle size={12} className="text-warning" />
                        <span className="text-slate-300">{alert}</span>
                    </div>
                ))}
                {riskData.alerts.length === 0 && (
                    <div className="flex items-center gap-2 p-2 rounded-lg bg-success/5 border border-success/10 text-[10px]">
                        <ShieldCheck size={12} className="text-success" />
                        <span className="text-success/80">All safety parameters within limits.</span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ClientHealthCompass;
