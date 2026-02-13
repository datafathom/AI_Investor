import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { FlaskConical, Settings, Save } from 'lucide-react';
import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const ConstructionLab = () => {
    const [frontier, setFrontier] = useState([]);
    const [result, setResult] = useState(null);

    useEffect(() => {
        loadFrontier();
    }, []);

    const loadFrontier = async () => {
        const res = await apiClient.get('/portfolio/frontier');
        if (res.data.success) {
            setFrontier(res.data.data.map(([risk, ret]) => ({ x: risk, y: ret })));
        }
    };

    const runOptimizer = async () => {
        const res = await apiClient.post('/portfolio/optimize', {});
        if (res.data.success) setResult(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <FlaskConical className="text-cyan-500" /> Portfolio Construction Lab
                </h1>
                <p className="text-slate-500">Mean-Variance Optimization & Efficient Frontier</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <Settings size={18} className="text-slate-400" /> Constraints
                    </h3>
                    <div className="space-y-4">
                        <div>
                            <label className="text-xs text-slate-500 uppercase">Risk Aversion</label>
                            <input type="range" className="w-full mt-1" />
                        </div>
                        <div>
                            <label className="text-xs text-slate-500 uppercase">Max Asset Weight</label>
                            <input type="number" className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white" defaultValue="25" />
                        </div>
                        <div className="flex items-center gap-2">
                            <input type="checkbox" defaultChecked />
                            <label className="text-sm text-slate-300">Long Only (No Shorting)</label>
                        </div>
                        <button 
                            onClick={runOptimizer}
                            className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-2 rounded mt-4"
                        >
                            RUN OPTIMIZER
                        </button>
                    </div>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Efficient Frontier</h3>
                    <div className="h-64 mb-6">
                        <ResponsiveContainer width="100%" height="100%">
                            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                <XAxis type="number" dataKey="x" name="Risk" unit="%" stroke="#64748b" />
                                <YAxis type="number" dataKey="y" name="Return" unit="%" stroke="#64748b" />
                                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                <Scatter name="Frontier" data={frontier} fill="#06b6d4" line />
                            </ScatterChart>
                        </ResponsiveContainer>
                    </div>

                    {result && (
                        <div>
                            <h4 className="font-bold text-white mb-2">Optimal Weights</h4>
                            <div className="grid grid-cols-2 gap-4">
                                {Object.entries(result.optimal_weights).map(([sym, w]) => (
                                    <div key={sym} className="flex justify-between bg-slate-950 p-2 rounded border border-slate-800">
                                        <span className="text-slate-300">{sym}</span>
                                        <span className="text-cyan-400 font-bold">{(w * 100).toFixed(1)}%</span>
                                    </div>
                                ))}
                            </div>
                            <button className="mt-4 flex items-center gap-2 text-sm text-slate-400 hover:text-white">
                                <Save size={16} /> SAVE AS TARGET
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ConstructionLab;
