import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Scales, Play } from 'lucide-react';

const Rebalancer = () => {
    const [targets, setTargets] = useState([]);
    const [preview, setPreview] = useState(null);

    useEffect(() => {
        loadTargets();
    }, []);

    const loadTargets = async () => {
        const res = await apiClient.get('/portfolio/targets');
        if (res.data.success) setTargets(res.data.data);
    };

    const generateTrades = async () => {
        const res = await apiClient.post('/portfolio/rebalance/preview');
        if (res.data.success) setPreview(res.data.data);
    };

    const execute = async () => {
        await apiClient.post('/portfolio/rebalance/execute');
        setPreview(null);
        alert("Rebalancing trades executed.");
        loadTargets();
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Scales className="text-orange-500" /> Automated Rebalancer
                </h1>
                <p className="text-slate-500">Drift Management & Allocation Alignment</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-bold text-white">Allocation Targets</h3>
                        <button 
                            onClick={generateTrades}
                            className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded text-sm font-bold"
                        >
                            CHECK FOR DRIFT
                        </button>
                    </div>
                    <table className="w-full text-left text-sm">
                        <thead className="text-slate-500 text-xs uppercase border-b border-slate-800">
                            <tr>
                                <th className="pb-2">Asset Class</th>
                                <th className="pb-2">Target %</th>
                                <th className="pb-2">Current %</th>
                                <th className="pb-2">Drift</th>
                            </tr>
                        </thead>
                        <tbody>
                            {targets.map((t, i) => (
                                <tr key={i} className="border-b border-slate-800 last:border-0">
                                    <td className="py-3 text-white font-bold">{t.asset}</td>
                                    <td className="py-3 text-slate-300">{t.target}%</td>
                                    <td className="py-3 text-slate-300">{t.current}%</td>
                                    <td className={`py-3 font-bold ${Math.abs(t.drift) > 2 ? 'text-red-400' : 'text-emerald-400'}`}>
                                        {t.drift > 0 ? '+' : ''}{t.drift}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {preview && (
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                            <Play size={18} className="text-emerald-500" /> Trade Preview
                        </h3>
                        <div className="space-y-3 mb-6">
                            {preview.map((trade, i) => (
                                <div key={i} className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                                    <div className="flex items-center gap-2">
                                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${trade.action === 'BUY' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                                            {trade.action}
                                        </span>
                                        <span className="text-white font-bold">{trade.qty} {trade.symbol}</span>
                                    </div>
                                    <span className="text-xs text-slate-500">{trade.reason}</span>
                                </div>
                            ))}
                        </div>
                        <button 
                            onClick={execute}
                            className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 rounded"
                        >
                            EXECUTE REBALANCE
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Rebalancer;
