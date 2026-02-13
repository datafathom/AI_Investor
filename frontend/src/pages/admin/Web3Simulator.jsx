import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { PlayCircle, ShieldCheck, ShieldAlert } from 'lucide-react';

const Web3Simulator = () => {
    const [params, setParams] = useState({ to: '', value: '', data: '' });
    const [result, setResult] = useState(null);

    const simulate = async () => {
        const res = await apiClient.post('/crypto/simulate', params);
        if (res.data.success) setResult(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <PlayCircle className="text-pink-500" /> Web3 Transaction Simulator
                </h1>
                <p className="text-slate-500">Pre-Execution Safety Checks & Outcome Preview</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6">Transaction Params</h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">To Address</label>
                            <input 
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white font-mono text-sm outline-none"
                                value={params.to}
                                onChange={e => setParams({...params, to: e.target.value})}
                                placeholder="0x..."
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Value (ETH)</label>
                            <input 
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white font-mono text-sm outline-none"
                                value={params.value}
                                onChange={e => setParams({...params, value: e.target.value})}
                                placeholder="0.0"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Data (Hex)</label>
                            <textarea 
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white font-mono text-sm outline-none h-32"
                                value={params.data}
                                onChange={e => setParams({...params, data: e.target.value})}
                                placeholder="0x..."
                            />
                        </div>
                        <button 
                            onClick={simulate}
                            className="w-full bg-pink-600 hover:bg-pink-500 text-white font-bold py-3 rounded"
                        >
                            SIMULATE TRANSACTION
                        </button>
                    </div>
                </div>

                {result && (
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                            {result.risk_flags.length === 0 ? <ShieldCheck className="text-emerald-500" /> : <ShieldAlert className="text-red-500" />}
                            Simulation Result
                        </h3>
                        
                        <div className="space-y-6">
                            <div className="p-4 bg-slate-950 rounded border border-slate-800">
                                <div className="text-xs uppercase text-slate-500 font-bold mb-2">Balance Changes</div>
                                {result.balance_changes.map((c, i) => (
                                    <div key={i} className="flex justify-between text-sm py-1 border-b border-slate-800 last:border-0">
                                        <span className="text-slate-300">{c.asset}</span>
                                        <span className={`font-bold ${c.change > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                            {c.change > 0 ? '+' : ''}{c.change}
                                        </span>
                                    </div>
                                ))}
                            </div>

                            <div className="p-4 bg-slate-950 rounded border border-slate-800">
                                <div className="text-xs uppercase text-slate-500 font-bold mb-2">Outcome</div>
                                <div className="text-white">{result.simulation_result}</div>
                            </div>
                            
                            <div className="p-4 bg-slate-950 rounded border border-slate-800">
                                <div className="text-xs uppercase text-slate-500 font-bold mb-2">Gas Used</div>
                                <div className="text-slate-300 font-mono">{result.gas_used.toLocaleString()} units</div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Web3Simulator;
