import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Calculator, ArrowRight } from 'lucide-react';

const PositionSizer = () => {
    const [inputs, setInputs] = useState({ capital: 100000, risk_per_trade_pct: 1.0, stop_loss_pct: 5.0 });
    const [result, setResult] = useState(null);

    const calculate = async () => {
        try {
            const res = await apiClient.post('/risk/sizing/calculate', null, { params: inputs });
            if (res.data.success) setResult(res.data.data);
        } catch (e) { console.error(e); }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Calculator className="text-cyan-500" /> Position Sizing Calculator
                </h1>
                <p className="text-slate-500">Determine Optimal Trade Size / Risk Parameters</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-8">
                    <div className="space-y-6">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-2">Account Capital ($)</label>
                            <input 
                                type="number" 
                                value={inputs.capital}
                                onChange={e => setInputs({...inputs, capital: parseFloat(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white text-lg font-mono"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-2">Risk Per Trade (%)</label>
                            <input 
                                type="number" 
                                value={inputs.risk_per_trade_pct}
                                onChange={e => setInputs({...inputs, risk_per_trade_pct: parseFloat(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white text-lg font-mono"
                            />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-2">Stop Loss Distance (%)</label>
                            <input 
                                type="number" 
                                value={inputs.stop_loss_pct}
                                onChange={e => setInputs({...inputs, stop_loss_pct: parseFloat(e.target.value)})}
                                className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-white text-lg font-mono"
                            />
                        </div>
                        <button 
                            onClick={calculate}
                            className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-4 rounded-xl text-lg shadow-lg shadow-cyan-900/20"
                        >
                            CALCULATE POSITION SIZE
                        </button>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col justify-center">
                    {result ? (
                        <div className="space-y-8">
                            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800">
                                <h3 className="text-xs uppercase text-slate-500 mb-2">Fixed Fractional Model</h3>
                                <div className="text-4xl font-bold text-white font-mono">${result.fixed_fractional.size.toLocaleString()}</div>
                                <div className="text-cyan-400 font-mono mt-1">{result.fixed_fractional.shares} Shares (@ $100 est)</div>
                            </div>

                            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 opacity-75">
                                <h3 className="text-xs uppercase text-slate-500 mb-2">Kelly Criterion (Aggressive)</h3>
                                <div className="text-2xl font-bold text-slate-300 font-mono">${result.kelly_criterion.size.toLocaleString()}</div>
                                <div className="text-slate-500 font-mono mt-1">{(result.kelly_criterion.optimal_f * 100).toFixed(1)}% of Capital</div>
                            </div>

                            <div className="flex items-start gap-4 p-4 bg-blue-900/20 rounded border border-blue-900/40">
                                <div className="bg-blue-500 w-12 h-12 rounded-full flex items-center justify-center shrink-0 font-bold text-white">AI</div>
                                <div>
                                    <div className="font-bold text-blue-300 mb-1">Recommendation</div>
                                    <p className="text-sm text-blue-200">{result.recommendation}</p>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-slate-500">
                            Enter parameters to see sizing recommendations.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PositionSizer;
