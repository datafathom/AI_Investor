import React, { useState } from 'react';
import { ToggleLeft, ToggleRight, Save, Play, Settings } from 'lucide-react';

const AutopilotConfig = () => {
    const [rules, setRules] = useState([
        { id: 1, if: 'Market Crash > 10%', then: 'Switch to DEFENSE Mode', active: true },
        { id: 2, if: 'Profit > 20%', then: 'Take Profit (50%)', active: true },
        { id: 3, if: 'Rsi < 30', then: 'Buy Signal', active: false }
    ]);

    const toggleRule = (id) => {
        setRules(rules.map(r => r.id === id ? { ...r, active: !r.active } : r));
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Settings className="text-cyan-500" /> Autopilot Configuration
                </h1>
                <p className="text-slate-500">IF-THEN Logic & Automated Responses</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-sm text-left">
                    <thead className="bg-slate-950 text-slate-500 uppercase text-xs">
                        <tr>
                            <th className="p-4">Condition (IF)</th>
                            <th className="p-4">Action (THEN)</th>
                            <th className="p-4 text-center">Status</th>
                            <th className="p-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rules.map(rule => (
                            <tr key={rule.id} className="border-t border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-mono text-cyan-300">{rule.if}</td>
                                <td className="p-4 font-mono text-purple-300">{rule.then}</td>
                                <td className="p-4 text-center">
                                    <button onClick={() => toggleRule(rule.id)} className="transition-colors">
                                        {rule.active ? (
                                            <ToggleRight size={24} className="text-green-500" />
                                        ) : (
                                            <ToggleLeft size={24} className="text-slate-600" />
                                        )}
                                    </button>
                                </td>
                                <td className="p-4 text-right">
                                    <button className="text-slate-400 hover:text-white mr-2">Edit</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="p-4 bg-slate-950 border-t border-slate-800 flex justify-end gap-2">
                    <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded text-xs font-bold flex items-center gap-2">
                        <Play size={14} /> Test Rules
                    </button>
                    <button className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded text-xs font-bold flex items-center gap-2">
                        <Save size={14} /> Save Configuration
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AutopilotConfig;
