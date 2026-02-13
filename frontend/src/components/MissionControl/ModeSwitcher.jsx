import React, { useState, useEffect } from 'react';
import apiClient from '../../../services/apiClient';
import { Shield, Zap, Eye, Leaf, Check } from 'lucide-react';

const MODES = {
    DEFENSE: { icon: Shield, color: 'text-blue-400', bg: 'bg-blue-500/20' },
    ATTACK: { icon: Zap, color: 'text-red-400', bg: 'bg-red-500/20' },
    STEALTH: { icon: Eye, color: 'text-slate-400', bg: 'bg-slate-500/20' },
    ZEN: { icon: Leaf, color: 'text-green-400', bg: 'bg-green-500/20' }
};

const ModeSwitcher = () => {
    const [currentMode, setCurrentMode] = useState('ZEN');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadMode();
    }, []);

    const loadMode = async () => {
        try {
            const res = await apiClient.get('/modes/current');
            if (res.data.success) {
                setCurrentMode(res.data.data.mode);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const handleSwitch = async (mode) => {
        setLoading(true);
        try {
            await apiClient.post('/modes/switch', { mode });
            setCurrentMode(mode);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-3 px-1">System Operation Mode</h3>
            <div className="grid grid-cols-2 gap-2">
                {Object.keys(MODES).map(key => {
                    const mode = MODES[key];
                    const Icon = mode.icon;
                    const isActive = currentMode === key;

                    return (
                        <button
                            key={key}
                            onClick={() => handleSwitch(key)}
                            disabled={loading}
                            className={`flex flex-col items-center justify-center p-3 rounded-lg border transition-all ${
                                isActive 
                                ? `${mode.bg} border-current ${mode.color} shadow-lg` 
                                : 'bg-slate-950 border-slate-800 text-slate-500 hover:bg-slate-800'
                            }`}
                        >
                            <Icon size={20} className="mb-2" />
                            <span className="text-[10px] font-bold">{key}</span>
                            {isActive && <Check size={10} className="mt-1" />}
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default ModeSwitcher;
