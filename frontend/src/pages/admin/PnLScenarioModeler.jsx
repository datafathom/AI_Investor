import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { TrendingUp, Sliders, PlayCircle } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts';

const PnLScenarioModeler = () => {
    const [scenarios, setScenarios] = useState([]);
    const [loading, setLoading] = useState(false);
    const [params, setParams] = useState({ underlying_price: 175.0, days_to_expiration: 30, volatility: 0.20 });

    const runScenario = async () => {
        setLoading(true);
        try {
            const res = await apiClient.post('/options/scenarios', params);
            if (res.data.success) {
                setScenarios(res.data.data);
            }
        } catch (e) { console.error(e); } 
        finally { setLoading(false); }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <TrendingUp className="text-green-500" /> P&L Modeler
                </h1>
                <p className="text-slate-500">What-If Analysis & Outcome Visualization</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Controls */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-6 flex items-center gap-2">
                        <Sliders size={18} /> Scenario Params
                    </h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Underlying Price</label>
                            <input 
                                type="number" 
                                value={params.underlying_price}
                                onChange={e => setParams({...params, underlying_price: parseFloat(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-white font-mono"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">DTE</label>
                            <input 
                                type="number" 
                                value={params.days_to_expiration}
                                onChange={e => setParams({...params, days_to_expiration: parseInt(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-white font-mono"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Volatility (IV)</label>
                            <input 
                                type="number" 
                                step="0.01"
                                value={params.volatility}
                                onChange={e => setParams({...params, volatility: parseFloat(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-800 rounded p-2 text-white font-mono"
                            />
                        </div>

                        <button 
                            onClick={runScenario}
                            disabled={loading}
                            className="w-full bg-green-600 hover:bg-green-500 text-white font-bold py-3 rounded mt-4 flex justify-center items-center gap-2"
                        >
                            {loading ? 'COMPUTING...' : <><PlayCircle size={18} /> RUN SCENARIO</>}
                        </button>
                    </div>
                </div>

                {/* Chart */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    {scenarios.length > 0 ? (
                        <div className="h-[400px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={scenarios}>
                                    <XAxis dataKey="price" stroke="#475569" tickFormatter={val => val.toFixed(0)} />
                                    <YAxis stroke="#475569" />
                                    <Tooltip 
                                        contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }}
                                        labelFormatter={val => `Price: ${Number(val).toFixed(2)}`}
                                    />
                                    <ReferenceLine y={0} stroke="#94a3b8" strokeDasharray="3 3" />
                                    <Line type="monotone" dataKey="pnl" stroke="#22c55e" strokeWidth={3} dot={false} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-500">
                            Run a scenario to visualize P&L curve
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PnLScenarioModeler;
