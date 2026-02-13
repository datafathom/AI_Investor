import React, { useState, useEffect } from 'react';
import apiClient from '../../../../services/apiClient'; // Fixed import path
import { Bell, ShieldAlert, Ban, EyeOff } from 'lucide-react';

const ModeAwareAlerts = () => {
    const [alerts, setAlerts] = useState([]);
    const [mode, setMode] = useState('ZEN');

    useEffect(() => {
        loadAlerts();
    }, []);

    const loadAlerts = async () => {
        try {
            const modeRes = await apiClient.get('/modes/current');
            if (modeRes.data.success) setMode(modeRes.data.data.mode);

            // Mock alerts for demo
            setAlerts([
                { id: 1, text: 'Portfolio unbalanced > 5%', severity: 'medium', modes: ['ZEN', 'DEFENSE'] },
                { id: 2, text: 'Margin Call Imminent', severity: 'critical', modes: ['ALL'] },
                { id: 3, text: 'Opportunity: AAPL breakout', severity: 'low', modes: ['ATTACK'] },
            ]);
        } catch (e) { console.error(e); }
    };

    const displayedAlerts = alerts.filter(a => a.modes.includes('ALL') || a.modes.includes(mode));

    const getModeIcon = () => {
        switch (mode) {
            case 'DEFENSE': return <ShieldAlert size={16} className="text-blue-400" />;
            case 'ATTACK': return <Bell size={16} className="text-red-400" />;
            case 'STEALTH': return <EyeOff size={16} className="text-slate-400" />;
            default: return <Ban size={16} className="text-green-400" />;
        }
    }

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 h-full overflow-hidden flex flex-col">
            <div className="flex justify-between items-center mb-4 pb-4 border-b border-slate-800">
                <h3 className="font-bold text-white text-sm">Active Alerts</h3>
                <div className="flex items-center gap-2 text-xs text-slate-500 bg-slate-950 px-2 py-1 rounded border border-slate-800">
                    {getModeIcon()}
                    <span>FILTER: {mode}</span>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
                {displayedAlerts.length === 0 ? (
                    <div className="text-center text-slate-600 text-xs py-4">No alerts for current mode.</div>
                ) : (
                    displayedAlerts.map(alert => (
                        <div key={alert.id} className={`p-3 rounded border text-xs flex gap-3 items-start ${
                            alert.severity === 'critical' ? 'bg-red-500/10 border-red-500/30 text-red-200' : 
                            alert.severity === 'medium' ? 'bg-orange-500/10 border-orange-500/30 text-orange-200' :
                            'bg-slate-800 border-slate-700 text-slate-300'
                        }`}>
                            <div className={`w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 ${
                                alert.severity === 'critical' ? 'bg-red-500 animate-pulse' : 
                                alert.severity === 'medium' ? 'bg-orange-500' : 'bg-blue-400'
                            }`} />
                            <span className="leading-relaxed">{alert.text}</span>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default ModeAwareAlerts;
