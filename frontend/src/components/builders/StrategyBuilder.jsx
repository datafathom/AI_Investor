import React, { useState } from 'react';
import { Plus, Play, Trash2, Settings } from 'lucide-react';

export const StrategyBuilder = ({ onRun }) => {
    const [strategy, setStrategy] = useState({
        ticker: 'AAPL',
        initial_capital: 100000,
        rules: [
            { type: 'entry', indicator: 'RSI', operator: '<', value: 30, action: 'BUY' },
            { type: 'exit', indicator: 'RSI', operator: '>', value: 70, action: 'SELL' }
        ]
    });

    const updateRule = (idx, field, val) => {
        const newRules = [...strategy.rules];
        newRules[idx][field] = val;
        setStrategy({ ...strategy, rules: newRules });
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider mb-4 flex items-center gap-2">
                <Settings size={16} /> Strategy Config
            </h3>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <label className="text-xs text-slate-500 mb-1 block">Ticker</label>
                    <input 
                        value={strategy.ticker}
                        onChange={(e) => setStrategy({...strategy, ticker: e.target.value})}
                        className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-sm"
                    />
                </div>
                <div>
                    <label className="text-xs text-slate-500 mb-1 block">Capital</label>
                     <input 
                        type="number"
                        value={strategy.initial_capital}
                        onChange={(e) => setStrategy({...strategy, initial_capital: parseFloat(e.target.value)})}
                        className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-sm"
                    />
                </div>
            </div>

            <div className="space-y-3 mb-6">
                <label className="text-xs text-slate-500 block">Trade Rules</label>
                {strategy.rules.map((rule, idx) => (
                    <div key={idx} className="flex gap-2 items-center bg-slate-800/50 p-2 rounded border border-slate-800">
                        <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded ${rule.type === 'entry' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                            {rule.type}
                        </span>
                        <select 
                            value={rule.indicator}
                            onChange={(e) => updateRule(idx, 'indicator', e.target.value)}
                            className="bg-slate-900 border border-slate-700 text-white rounded p-1 text-xs"
                        >
                            <option value="RSI">RSI</option>
                            <option value="SMA">SMA</option>
                            <option value="EMA">EMA</option>
                        </select>
                        <select 
                            value={rule.operator}
                            onChange={(e) => updateRule(idx, 'operator', e.target.value)}
                            className="bg-slate-900 border border-slate-700 text-white rounded p-1 text-xs w-12"
                        >
                            <option value="<">&lt;</option>
                            <option value=">">&gt;</option>
                        </select>
                        <input 
                            type="number"
                            value={rule.value}
                            onChange={(e) => updateRule(idx, 'value', e.target.value)}
                            className="bg-slate-900 border border-slate-700 text-white rounded p-1 text-xs w-16"
                        />
                    </div>
                ))}
            </div>

            <button 
                onClick={() => onRun(strategy)} 
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded font-bold flex items-center justify-center gap-2 transition-colors"
            >
                <Play size={16} fill="currentColor" /> Run Backtest
            </button>
        </div>
    );
};
