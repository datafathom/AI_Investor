import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Eye, Fuel, Activity } from 'lucide-react';

const OnChainTerminal = () => {
    const [whales, setWhales] = useState([]);
    const [gas, setGas] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [wRes, gRes] = await Promise.all([
                apiClient.get('/crypto/on-chain/activity'),
                apiClient.get('/crypto/gas')
            ]);
            if (wRes.data.success) setWhales(wRes.data.data);
            if (gRes.data.success) setGas(gRes.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Eye className="text-purple-500" /> On-Chain Intelligence
                </h1>
                <p className="text-slate-500">Whale Monitoring & Gas Oracle</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                {gas.map(g => (
                    <div key={g.chain} className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Fuel size={20} className="text-orange-500" />
                            <h3 className="font-bold text-white">{g.chain} Gas</h3>
                        </div>
                        <div className="flex justify-between text-center">
                            <div>
                                <div className="text-2xl font-bold text-emerald-400">{g.slow}</div>
                                <div className="text-xs text-slate-500">Slow</div>
                            </div>
                            <div>
                                <div className="text-2xl font-bold text-blue-400">{g.std}</div>
                                <div className="text-xs text-slate-500">Standard</div>
                            </div>
                            <div>
                                <div className="text-2xl font-bold text-red-400">{g.fast}</div>
                                <div className="text-xs text-slate-500">Fast</div>
                            </div>
                        </div>
                        <div className="text-center mt-2 text-xs text-slate-600 uppercase font-bold">{g.unit}</div>
                    </div>
                ))}
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <div className="p-4 bg-slate-950 border-b border-slate-800 font-bold text-white flex items-center gap-2">
                    <Activity size={18} className="text-blue-500" /> Whale Alert Feed
                </div>
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Time</th>
                            <th className="p-4">Chain</th>
                            <th className="p-4">Token</th>
                            <th className="p-4">Value (USD)</th>
                            <th className="p-4">From</th>
                            <th className="p-4">To</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {whales.map((w, i) => (
                            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 text-slate-400">{w.time}</td>
                                <td className="p-4 text-white font-bold">{w.chain}</td>
                                <td className="p-4 text-slate-300">{w.token}</td>
                                <td className="p-4 font-mono font-bold text-white">${w.value_usd.toLocaleString()}</td>
                                <td className="p-4 text-slate-400 text-xs">{w.from}</td>
                                <td className="p-4 text-slate-400 text-xs">{w.to}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default OnChainTerminal;
