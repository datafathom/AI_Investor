import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Search, Filter } from 'lucide-react';

export const ScannerBuilder = ({ metrics, onRun }) => {
    const [criteria, setCriteria] = useState([
        { metric: 'pe_ratio', operator: '<', value: 25 }
    ]);

    const addCriterion = () => {
        setCriteria([...criteria, { metric: metrics[0]?.id || '', operator: '<', value: 0 }]);
    };

    const removeCriterion = (idx) => {
        const newCriteria = [...criteria];
        newCriteria.splice(idx, 1);
        setCriteria(newCriteria);
    };

    const updateCriterion = (idx, field, val) => {
        const newCriteria = [...criteria];
        newCriteria[idx][field] = val;
        setCriteria(newCriteria);
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider flex items-center gap-2">
                    <Filter size={16} /> Scan Criteria
                </h3>
            </div>
            
            <div className="space-y-3 mb-6">
                {criteria.map((c, idx) => (
                    <div key={idx} className="flex gap-3 items-center">
                        <select 
                            value={c.metric} 
                            onChange={(e) => updateCriterion(idx, 'metric', e.target.value)}
                            className="bg-slate-800 border border-slate-700 text-white rounded p-2 text-sm flex-1 outline-none focus:border-cyan-500"
                        >
                            {metrics.map(m => (
                                <option key={m.id} value={m.id}>{m.name}</option>
                            ))}
                        </select>
                        <select 
                            value={c.operator}
                            onChange={(e) => updateCriterion(idx, 'operator', e.target.value)}
                            className="bg-slate-800 border border-slate-700 text-white rounded p-2 text-sm w-20 outline-none focus:border-cyan-500"
                        >
                            <option value="<">&lt;</option>
                            <option value=">">&gt;</option>
                            <option value="=">=</option>
                            <option value=">=">&ge;</option>
                            <option value="<=">&le;</option>
                        </select>
                        <input 
                            type="number" 
                            step="0.01"
                            value={c.value}
                            onChange={(e) => updateCriterion(idx, 'value', e.target.value)}
                            className="bg-slate-800 border border-slate-700 text-white rounded p-2 text-sm w-32 outline-none focus:border-cyan-500"
                        />
                        <button onClick={() => removeCriterion(idx)} className="text-slate-500 hover:text-red-400 p-2">
                            <Trash2 size={16} />
                        </button>
                    </div>
                ))}
            </div>

            <div className="flex gap-3">
                <button onClick={addCriterion} className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded text-sm text-slate-300 font-bold flex items-center gap-2 transition-colors">
                    <Plus size={16} /> Add Filter
                </button>
                <button onClick={() => onRun(criteria)} className="px-6 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-900 rounded text-sm font-bold flex items-center gap-2 transition-colors ml-auto shadow-lg shadow-cyan-500/20">
                    <Search size={16} /> Run Scan
                </button>
            </div>
        </div>
    );
};

export const ScanResultsTable = ({ results, metrics }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-slate-400">
                    <thead className="bg-slate-950 text-slate-200 uppercase font-bold text-xs">
                        <tr>
                            <th className="p-4">Ticker</th>
                            <th className="p-4">Company</th>
                            <th className="p-4">Sector</th>
                            {metrics.slice(0, 5).map(m => (
                                <th key={m.id} className="p-4 text-right">{m.name}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {results.length === 0 ? (
                            <tr>
                                <td colSpan={3 + Math.min(metrics.length, 5)} className="p-8 text-center text-slate-500">
                                    No matches found.
                                </td>
                            </tr>
                        ) : (
                            results.map(r => (
                                <tr key={r.ticker} className="hover:bg-slate-800/50 transition-colors">
                                    <td className="p-4 font-bold text-white">{r.ticker}</td>
                                    <td className="p-4">{r.name}</td>
                                    <td className="p-4">
                                        <span className="px-2 py-1 bg-slate-800 rounded text-xs">{r.sector}</span>
                                    </td>
                                    {metrics.slice(0, 5).map(m => (
                                        <td key={m.id} className="p-4 text-right font-mono text-slate-300">
                                            {m.format === 'percent' ? `${(r.metrics[m.id] * 100).toFixed(2)}%` : r.metrics[m.id]}
                                        </td>
                                    ))}
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
            <div className="bg-slate-950 p-2 text-xs text-slate-600 text-center border-t border-slate-800">
                Showing top 5 metrics columns for brevity
            </div>
        </div>
    );
};
