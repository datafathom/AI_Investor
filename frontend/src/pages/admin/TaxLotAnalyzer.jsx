import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { DollarSign, Layers } from 'lucide-react';

const TaxLotAnalyzer = () => {
    const [lots, setLots] = useState([]);
    const [gl, setGl] = useState(null);

    useEffect(() => {
        const load = async () => {
            const [lRes, gRes] = await Promise.all([
                apiClient.get('/reporting/tax-lots'),
                apiClient.get('/reporting/unrealized-gl')
            ]);
            if (lRes.data.success) setLots(lRes.data.data);
            if (gRes.data.success) setGl(gRes.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Layers className="text-purple-500" /> Tax Lot Analyzer
                </h1>
                <p className="text-slate-500">Unrealized G/L & Tax Optimization</p>
            </header>

            {gl && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Unrealized G/L</div>
                        <div className="text-3xl font-bold text-emerald-400 font-mono">+${gl.total.toLocaleString()}</div>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="text-xs uppercase text-slate-500 font-bold mb-2">Long Term</div>
                        <div className="text-2xl font-bold text-blue-400 font-mono">+${gl.long_term.toLocaleString()}</div>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="text-xs uppercase text-slate-500 font-bold mb-2">Harvestable Losses</div>
                        <div className="text-2xl font-bold text-red-500 font-mono">${gl.harvestable_losses.toLocaleString()}</div>
                    </div>
                </div>
            )}

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Symbol</th>
                            <th className="p-4">Date Acquired</th>
                            <th className="p-4">Qty</th>
                            <th className="p-4">Cost Basis</th>
                            <th className="p-4">Unrealized P/L</th>
                            <th className="p-4">Term</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {lots.map(l => (
                            <tr key={l.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{l.symbol}</td>
                                <td className="p-4 text-slate-400">{l.date_acquired}</td>
                                <td className="p-4 text-slate-300">{l.qty}</td>
                                <td className="p-4 font-mono text-slate-400">${l.cost_basis.toFixed(2)}</td>
                                <td className={`p-4 font-mono font-bold ${l.unrealized_pl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                    {l.unrealized_pl >= 0 ? '+' : ''}{l.unrealized_pl.toLocaleString()}
                                </td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        l.term === 'LONG' ? 'bg-blue-500/20 text-blue-400' : 'bg-yellow-500/20 text-yellow-400'
                                    }`}>
                                        {l.term}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TaxLotAnalyzer;
