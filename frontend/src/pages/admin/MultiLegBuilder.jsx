import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { GitMerge, Plus, Trash2 } from 'lucide-react';

const MultiLegBuilder = () => {
    const [templates, setTemplates] = useState([]);
    const [legs, setLegs] = useState([{ side: 'BUY', symbol: '', qty: 1 }]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/orders/multileg/templates');
            if (res.data.success) setTemplates(res.data.data);
        };
        load();
    }, []);

    const addLeg = () => setLegs([...legs, { side: 'BUY', symbol: '', qty: 1 }]);
    const removeLeg = (idx) => setLegs(legs.filter((_, i) => i !== idx));
    const updateLeg = (idx, field, val) => {
        const newLegs = [...legs];
        newLegs[idx][field] = val;
        setLegs(newLegs);
    };

    const submit = async () => {
        await apiClient.post('/orders/multileg', legs);
        alert("Strategy Submitted");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <GitMerge className="text-purple-500" /> Multi-Leg Strategy Builder
                    </h1>
                    <p className="text-slate-500">Complex Option Spreads & Combinations</p>
                </div>
                <div className="flex gap-2">
                    {templates.map(t => (
                        <button key={t.name} className="bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded text-xs text-slate-300">
                            {t.name}
                        </button>
                    ))}
                </div>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
                <div className="space-y-4">
                    {legs.map((leg, i) => (
                        <div key={i} className="flex gap-4 items-end bg-slate-950 p-4 rounded border border-slate-800">
                            <div>
                                <label className="block text-xs uppercase text-slate-500 mb-1">Side</label>
                                <select 
                                    className={`bg-slate-900 border rounded p-2 text-white outline-none w-24 ${leg.side === 'BUY' ? 'border-emerald-500 text-emerald-400' : 'border-red-500 text-red-400'}`}
                                    value={leg.side}
                                    onChange={e => updateLeg(i, 'side', e.target.value)}
                                >
                                    <option value="BUY">BUY</option>
                                    <option value="SELL">SELL</option>
                                </select>
                            </div>
                            <div className="flex-1">
                                <label className="block text-xs uppercase text-slate-500 mb-1">Symbol / Contract</label>
                                <input 
                                    className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white outline-none"
                                    value={leg.symbol}
                                    onChange={e => updateLeg(i, 'symbol', e.target.value)}
                                    placeholder="e.g., SPY 240621C00500000"
                                />
                            </div>
                            <div>
                                <label className="block text-xs uppercase text-slate-500 mb-1">Ratio</label>
                                <input 
                                    type="number"
                                    className="w-20 bg-slate-900 border border-slate-700 rounded p-2 text-white outline-none"
                                    value={leg.qty}
                                    onChange={e => updateLeg(i, 'qty', e.target.value)}
                                />
                            </div>
                            <button onClick={() => removeLeg(i)} className="p-2 text-slate-500 hover:text-red-400">
                                <Trash2 size={18} />
                            </button>
                        </div>
                    ))}
                </div>
                
                <div className="mt-6 flex justify-between">
                    <button onClick={addLeg} className="text-blue-400 hover:text-blue-300 flex items-center gap-1 text-sm font-bold">
                        <Plus size={16} /> ADD LEG
                    </button>
                    <button onClick={submit} className="bg-purple-600 hover:bg-purple-500 text-white font-bold px-6 py-2 rounded">
                        SUBMIT STRATEGY
                    </button>
                </div>
            </div>
        </div>
    );
};

export default MultiLegBuilder;
