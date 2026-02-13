import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Bracket, Target, ShieldAlert } from 'lucide-react';

const BracketManager = () => {
    const [formData, setFormData] = useState({ symbol: '', qty: '', limit: '', takeProfit: '', stopLoss: '' });

    const submit = async (e) => {
        e.preventDefault();
        await apiClient.post('/orders/bracket', null, { 
            params: { 
                symbol: formData.symbol, 
                qty: formData.qty, 
                limit: formData.limit, 
                stop: formData.stopLoss, 
                take_profit: formData.takeProfit 
            } 
        });
        alert("Bracket Order Submitted");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Target className="text-emerald-500" /> Bracket Order Manager
                </h1>
                <p className="text-slate-500">Entry + Take Profit + Stop Loss Automation</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1 space-y-4">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <h3 className="font-bold text-white mb-4">Entry Order</h3>
                        <div className="text-xs uppercase text-slate-500 mb-1">Symbol</div>
                        <input 
                            className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white mb-3"
                            value={formData.symbol}
                            onChange={e => setFormData({...formData, symbol: e.target.value.toUpperCase()})}
                        />
                        <div className="text-xs uppercase text-slate-500 mb-1">Quantity</div>
                        <input 
                            className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white mb-3"
                            type="number"
                            value={formData.qty}
                            onChange={e => setFormData({...formData, qty: e.target.value})}
                        />
                        <div className="text-xs uppercase text-slate-500 mb-1">Limit Price</div>
                        <input 
                            className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white"
                            type="number"
                            value={formData.limit}
                            onChange={e => setFormData({...formData, limit: e.target.value})}
                        />
                    </div>

                    <div className="bg-emerald-900/20 border border-emerald-900/50 rounded-xl p-6">
                        <h3 className="font-bold text-emerald-400 mb-4 flex items-center gap-2">
                            <Target size={16} /> Take Profit
                        </h3>
                        <div className="text-xs uppercase text-emerald-400/70 mb-1">Exit Price</div>
                        <input 
                            className="w-full bg-slate-950 border border-emerald-900/50 rounded p-2 text-white"
                            type="number"
                            value={formData.takeProfit}
                            onChange={e => setFormData({...formData, takeProfit: e.target.value})}
                        />
                    </div>

                    <div className="bg-red-900/20 border border-red-900/50 rounded-xl p-6">
                        <h3 className="font-bold text-red-400 mb-4 flex items-center gap-2">
                            <ShieldAlert size={16} /> Stop Loss
                        </h3>
                        <div className="text-xs uppercase text-red-400/70 mb-1">Stop Price</div>
                        <input 
                            className="w-full bg-slate-950 border border-red-900/50 rounded p-2 text-white"
                            type="number"
                            value={formData.stopLoss}
                            onChange={e => setFormData({...formData, stopLoss: e.target.value})}
                        />
                    </div>

                    <button onClick={submit} className="w-full bg-slate-100 hover:bg-white text-slate-900 font-bold py-3 rounded">
                        SUBMIT BRACKET
                    </button>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-center items-center text-slate-500">
                     <div className="text-6xl mb-4 opacity-20">📈</div>
                     <p>Payoff Diagram Placeholder</p>
                     <p className="text-xs mt-2">Visualizing Risk/Reward Ratio: 1:{formData.limit && formData.takeProfit && formData.stopLoss ? ((formData.takeProfit - formData.limit) / (formData.limit - formData.stopLoss)).toFixed(2) : 'N/A'}</p>
                </div>
            </div>
        </div>
    );
};

export default BracketManager;
