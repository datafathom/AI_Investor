import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Cpu, Send, Info } from 'lucide-react';

const AlgoOrderEntry = () => {
    const [strategies, setStrategies] = useState([]);
    const [selectedStrat, setSelectedStrat] = useState('');
    const [formData, setFormData] = useState({ symbol: '', side: 'BUY', qty: '' });

    useEffect(() => {
        loadStrategies();
    }, []);

    const loadStrategies = async () => {
        const res = await apiClient.get('/orders/algo/strategies');
        if (res.data.success) {
            setStrategies(res.data.data);
            if(res.data.data.length > 0) setSelectedStrat(res.data.data[0].id);
        }
    };

    const submitOrder = async (e) => {
        e.preventDefault();
        await apiClient.post('/orders/algo', null, { params: { ...formData, strategy: selectedStrat } });
        alert("Algo Order Submitted");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Cpu className="text-cyan-500" /> Algorithmic Order Entry
                </h1>
                <p className="text-slate-500">Execution Algorithms & Strategy Parameters</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6">Order Parameters</h3>
                    <form onSubmit={submitOrder} className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Strategy</label>
                            <select 
                                className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white outline-none"
                                value={selectedStrat}
                                onChange={e => setSelectedStrat(e.target.value)}
                            >
                                {strategies.map(s => <option key={s.id} value={s.id}>{s.name} - {s.desc}</option>)}
                            </select>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs uppercase text-slate-500 mb-1">Symbol</label>
                                <input 
                                    className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white uppercase outline-none font-bold"
                                    value={formData.symbol}
                                    onChange={e => setFormData({...formData, symbol: e.target.value.toUpperCase()})}
                                />
                            </div>
                            <div>
                                <label className="block text-xs uppercase text-slate-500 mb-1">Side</label>
                                <select 
                                    className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white outline-none"
                                    value={formData.side}
                                    onChange={e => setFormData({...formData, side: e.target.value})}
                                >
                                    <option value="BUY">BUY</option>
                                    <option value="SELL">SELL</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Quantity</label>
                            <input 
                                type="number"
                                className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white outline-none"
                                value={formData.qty}
                                onChange={e => setFormData({...formData, qty: e.target.value})}
                            />
                        </div>

                        <div className="p-4 bg-slate-950 rounded border border-slate-800 text-sm text-slate-400 flex gap-2">
                            <Info size={16} className="mt-0.5" />
                            <p>
                                <strong>TWAP Strategy:</strong> Slices order evenly over specified time duration to minimize market impact.
                            </p>
                        </div>

                        <button className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded flex justify-center items-center gap-2">
                            <Send size={18} /> SUBMIT ALGO
                        </button>
                    </form>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center justify-center text-slate-500">
                    <div className="text-center">
                        <div className="text-6xl mb-4 opacity-20">📊</div>
                        <p>Execution Preview Chart Placeholder</p>
                        <p className="text-xs mt-2">Visualize projected fill vs benchmark profile</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AlgoOrderEntry;
