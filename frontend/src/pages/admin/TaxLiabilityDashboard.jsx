import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Landmark, TrendingDown, Scale } from 'lucide-react';

const TaxLiabilityDashboard = () => {
    const [estimates, setEstimates] = useState(null);
    const [harvesting, setHarvesting] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [eRes, hRes] = await Promise.all([
                apiClient.get('/tax/liabilities/estimated'),
                apiClient.get('/tax/lots/harvesting')
            ]);
            if (eRes.data.success) setEstimates(eRes.data.data);
            if (hRes.data.success) setHarvesting(hRes.data.data);
        };
        load();
    }, []);

    if (!estimates) return <div>Loading Tax Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Landmark className="text-emerald-600" /> Tax Liability Dashboard
                </h1>
                <p className="text-slate-500">Real-Time Estimates & Harvesting Opportunities</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 border-l-4 border-l-red-500">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Estimated Liability</div>
                    <div className="text-4xl font-bold text-white">${estimates.total_estimated.toLocaleString()}</div>
                    <div className="text-xs text-red-400 mt-2 font-bold">UNPAID</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Short Term Gains Tax</div>
                    <div className="text-2xl font-bold text-slate-200">${estimates.federal_short_term.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Harvestable Losses</div>
                    <div className="text-2xl font-bold text-emerald-400">
                        ${harvesting.reduce((acc, curr) => acc + curr.loss_amount, 0).toLocaleString()}
                    </div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <Scale size={20} className="text-orange-400" /> Harvesting Opportunities
                </h3>
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Symbol</th>
                            <th className="p-4">Unrealized Loss</th>
                            <th className="p-4">Wash Sale Risk</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {harvesting.map((h, i) => (
                            <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{h.symbol}</td>
                                <td className="p-4 text-red-400 font-bold">-${h.loss_amount.toLocaleString()}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${h.wash_sale_risk === 'LOW' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                                        {h.wash_sale_risk}
                                    </span>
                                </td>
                                <td className="p-4">
                                    <button className="bg-slate-800 hover:bg-slate-700 text-white text-xs px-3 py-1 rounded font-bold">
                                        HARVEST
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TaxLiabilityDashboard;
