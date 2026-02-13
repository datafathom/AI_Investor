import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Filter, Play, Save } from 'lucide-react';

const ScreenerBuilder = () => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    const runScreen = async () => {
        setLoading(true);
        try {
            const res = await apiClient.post('/screener/run');
            if (res.data.success) setResults(res.data.data);
        } catch (e) { console.error(e); }
        finally { setLoading(false); }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Filter className="text-purple-500" /> Screener Builder
                </h1>
                <p className="text-slate-500">Find Assets Matching Custom Criteria</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Criteria Panel */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Screening Criteria</h3>
                    <div className="space-y-4 mb-6">
                        <div>
                            <label className="text-xs uppercase text-slate-500">Market Cap</label>
                            <select className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white mt-1">
                                <option>Any</option>
                                <option>Mega {'>'} 200B</option>
                                <option>Large {'>'} 10B</option>
                            </select>
                        </div>
                        <div>
                            <label className="text-xs uppercase text-slate-500">Sector</label>
                            <select className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white mt-1">
                                <option>Technology</option>
                                <option>Finance</option>
                                <option>Healthcare</option>
                            </select>
                        </div>
                        <div>
                            <label className="text-xs uppercase text-slate-500">Technical</label>
                            <select className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white mt-1">
                                <option>RSI {'<'} 30 (Oversold)</option>
                                <option>Above SMA 200</option>
                                <option>Golden Cross</option>
                            </select>
                        </div>
                    </div>
                    <div className="flex gap-2">
                        <button 
                            onClick={runScreen}
                            disabled={loading}
                            className="flex-1 bg-purple-600 hover:bg-purple-500 text-white font-bold py-2 rounded flex items-center justify-center gap-2"
                        >
                            <Play size={16} /> RUN
                        </button>
                        <button className="bg-slate-800 hover:bg-slate-700 text-white p-2 rounded">
                            <Save size={16} />
                        </button>
                    </div>
                </div>

                {/* Results Panel */}
                <div className="lg:col-span-3 bg-slate-900 border border-slate-800 rounded-xl p-6 overflow-hidden flex flex-col">
                    <h3 className="font-bold text-white mb-4">Results ({results.length})</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                                <tr>
                                    <th className="p-3">Symbol</th>
                                    <th className="p-3">Price</th>
                                    <th className="p-3">Change %</th>
                                    <th className="p-3">Volume</th>
                                    <th className="p-3">Action</th>
                                </tr>
                            </thead>
                            <tbody className="text-sm">
                                {results.map(r => (
                                    <tr key={r.symbol} className="border-b border-slate-800 hover:bg-slate-800/50">
                                        <td className="p-3 font-bold text-white font-mono">{r.symbol}</td>
                                        <td className="p-3 text-slate-300 font-mono">${r.price.toFixed(2)}</td>
                                        <td className={`p-3 font-bold ${r.change_pct >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                            {r.change_pct > 0 ? '+' : ''}{r.change_pct}%
                                        </td>
                                        <td className="p-3 text-slate-400 font-mono">{(r.volume / 1000000).toFixed(1)}M</td>
                                        <td className="p-3">
                                            <button className="text-blue-400 hover:text-blue-300 text-xs font-bold uppercase">
                                                + Watchlist
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {results.length === 0 && !loading && (
                                    <tr>
                                        <td colSpan="5" className="p-8 text-center text-slate-500">
                                            Adjust criteria and click Run to see results.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ScreenerBuilder;
