import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Percent, ArrowRight, TrendingUp } from 'lucide-react';

const YieldOptimizer = () => {
    const [options, setOptions] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/treasury/yield/opportunities');
            if (res.data.success) setOptions(res.data.data);
        };
        load();
    }, []);

    const allocate = async (id, name) => {
        const amount = prompt(`Enter amount to allocate to ${name}:`);
        if (!amount) return;
        await apiClient.post('/treasury/allocations', null, { params: { amount, option_id: id } });
        alert("Allocation request submitting.");
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <TrendingUp className="text-purple-500" /> Yield Optimizer
                </h1>
                <p className="text-slate-500">Idle Cash Management & APY Maximization</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Instrument</th>
                            <th className="p-4">APY</th>
                            <th className="p-4">Risk Profile</th>
                            <th className="p-4">Liquidity</th>
                            <th className="p-4">Min. Invest</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {options.map(opt => (
                            <tr key={opt.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{opt.name}</td>
                                <td className="p-4 text-emerald-400 font-bold text-lg">{opt.apy}%</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        opt.risk === 'RISK_FREE' ? 'bg-emerald-500/20 text-emerald-400' : 
                                        opt.risk === 'FDIC' ? 'bg-blue-500/20 text-blue-400' : 
                                        'bg-yellow-500/20 text-yellow-400'
                                    }`}>
                                        {opt.risk.replace('_', ' ')}
                                    </span>
                                </td>
                                <td className="p-4 text-slate-300">{opt.liquidity}</td>
                                <td className="p-4 font-mono text-slate-400">${opt.min_investment.toLocaleString()}</td>
                                <td className="p-4">
                                    <button 
                                        onClick={() => allocate(opt.id, opt.name)}
                                        className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded text-xs font-bold flex items-center gap-1"
                                    >
                                        ALLOCATE <ArrowRight size={12} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6 flex gap-4 items-center">
                <Percent className="text-blue-500" size={32} />
                <div>
                    <h3 className="font-bold text-white">Benchmark Comparison</h3>
                    <p className="text-sm text-slate-400">
                        Current average portfolio yield is <strong>4.2%</strong>. Moving idle cash to T-Bills could increase net yield by <strong>120bps</strong>.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default YieldOptimizer;
