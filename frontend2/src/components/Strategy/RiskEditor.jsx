import React, { useState } from 'react';
import { Sliders } from 'lucide-react';

const RiskEditor = () => {
    const [params, setParams] = useState({
        maxDrawdown: 15,
        leverage: 2.5,
        concentration: 20
    });

    const handleChange = (key, val) => {
        setParams(p => ({ ...p, [key]: val }));
    };

    return (
        <div className="bg-slate-900/50 p-4 rounded border border-slate-700">
            <h3 className="text-sm font-bold text-slate-300 mb-4 flex items-center gap-2">
                <Sliders size={14} className="text-cyan-400" /> Risk Constraints
            </h3>

            <div className="space-y-4">
                <div className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-400">
                        <span>Max Drawdown</span>
                        <span className="font-mono text-cyan-400">{params.maxDrawdown}%</span>
                    </div>
                    <input
                        type="range" min="5" max="30" step="1"
                        value={params.maxDrawdown}
                        onChange={(e) => handleChange('maxDrawdown', e.target.value)}
                        className="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                    />
                </div>

                <div className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-400">
                        <span>Max Leverage</span>
                        <span className="font-mono text-purple-400">{params.leverage}x</span>
                    </div>
                    <input
                        type="range" min="1" max="5" step="0.1"
                        value={params.leverage}
                        onChange={(e) => handleChange('leverage', e.target.value)}
                        className="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                    />
                </div>

                <div className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-400">
                        <span>Concentration Limit</span>
                        <span className="font-mono text-orange-400">{params.concentration}%</span>
                    </div>
                    <input
                        type="range" min="5" max="50" step="5"
                        value={params.concentration}
                        onChange={(e) => handleChange('concentration', e.target.value)}
                        className="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-orange-500"
                    />
                </div>
            </div>
        </div>
    );
};

export default RiskEditor;
