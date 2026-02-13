import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Radio, Search, Filter, AlertTriangle } from 'lucide-react';

const OptionsFlowScanner = () => {
    const [flow, setFlow] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        const loadData = async () => {
            try {
                const res = await apiClient.get('/options/flow');
                if (res.data.success) setFlow(res.data.data);
            } catch (e) {
                console.error(e);
            }
        };
        loadData();
        const interval = setInterval(loadData, 3000); // Poll for real-time feel
        return () => clearInterval(interval);
    }, []);

    const filteredFlow = flow.filter(f => f.ticker.includes(filter.toUpperCase()));

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Radio className="text-green-500 animate-pulse" /> Options Flow Scanner
                    </h1>
                    <p className="text-slate-500">Institutional Sweep & Block Detection</p>
                </div>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
                    <input 
                        type="text" 
                        placeholder="Filter Ticker..." 
                        value={filter}
                        onChange={e => setFilter(e.target.value)}
                        className="bg-slate-900 border border-slate-700 rounded-full pl-10 pr-4 py-2 text-white focus:border-green-500 outline-none uppercase font-bold w-64"
                    />
                </div>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-sm text-left">
                    <thead className="bg-slate-950 text-slate-500 uppercase text-xs">
                        <tr>
                            <th className="p-4">Time</th>
                            <th className="p-4">Ticker</th>
                            <th className="p-4">Contract</th>
                            <th className="p-4">Type</th>
                            <th className="p-4 text-center">Sentiment</th>
                            <th className="p-4 text-right">Premium</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredFlow.map((f, i) => (
                            <tr key={i} className={`border-t border-slate-800 hover:bg-slate-800/50 ${f.premium > 1000000 ? 'bg-yellow-500/5' : ''}`}>
                                <td className="p-4 font-mono text-slate-500">{f.time}</td>
                                <td className="p-4 font-bold text-white">{f.ticker}</td>
                                <td className="p-4 font-mono text-cyan-300">{f.contract}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        f.type === 'SWEEP' ? 'bg-purple-500/20 text-purple-400' :
                                        f.type === 'BLOCK' ? 'bg-blue-500/20 text-blue-400' :
                                        'bg-slate-800 text-slate-400'
                                    }`}>
                                        {f.type}
                                    </span>
                                </td>
                                <td className="p-4 text-center">
                                    <span className={`font-bold ${f.sentiment === 'BULLISH' ? 'text-green-400' : 'text-red-400'}`}>
                                        {f.sentiment}
                                    </span>
                                </td>
                                <td className="p-4 text-right font-mono font-bold text-white">
                                    ${(f.premium / 1000).toFixed(0)}k
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default OptionsFlowScanner;
