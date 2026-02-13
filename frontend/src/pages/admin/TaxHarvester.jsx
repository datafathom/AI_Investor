import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { DollarSign, RefreshCw, Scissors } from 'lucide-react';

const TaxHarvester = () => {
    const [opps, setOpps] = useState([]);

    useEffect(() => {
        loadOpps();
    }, []);

    const loadOpps = async () => {
        const res = await apiClient.get('/portfolio/tax/opportunities');
        if (res.data.success) setOpps(res.data.data);
    };

    const harvest = async (symbol) => {
        if (!confirm(`Harvest losses for ${symbol}? This will sell the position and buy the replacement.`)) return;
        await apiClient.post('/portfolio/tax/harvest', null, { params: { symbol } });
        alert("Harvest Executed");
        loadOpps();
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Scissors className="text-red-500" /> Tax Loss Harvester
                </h1>
                <p className="text-slate-500">Unrealized Loss Realization & Wash Sale Avoidance</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Symbol</th>
                            <th className="p-4">Current Price</th>
                            <th className="p-4">Unrealized Loss</th>
                            <th className="p-4">Replacement</th>
                            <th className="p-4">Est. Tax Savings</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {opps.map(op => (
                            <tr key={op.symbol} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{op.symbol}</td>
                                <td className="p-4 font-mono text-slate-300">${op.current_price.toFixed(2)}</td>
                                <td className="p-4 font-mono font-bold text-red-500">${op.unrealized_loss.toLocaleString()}</td>
                                <td className="p-4">
                                    <span className="flex items-center gap-1 text-blue-400">
                                        <RefreshCw size={12} /> {op.replacement}
                                    </span>
                                </td>
                                <td className="p-4 font-mono font-bold text-emerald-400">+${op.estimated_savings.toLocaleString()}</td>
                                <td className="p-4">
                                    <button 
                                        onClick={() => harvest(op.symbol)}
                                        className="bg-red-900/40 hover:bg-red-900/60 text-red-400 border border-red-900/60 px-3 py-1 rounded text-xs"
                                    >
                                        HARVEST
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 flex gap-4 items-center">
                <DollarSign className="text-emerald-500" size={32} />
                <div>
                    <h3 className="font-bold text-white">Tax Efficiency Impact</h3>
                    <p className="text-sm text-slate-400">
                        Harvesting all opportunities could offset <strong>$12,500</strong> in capital gains this year.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default TaxHarvester;
