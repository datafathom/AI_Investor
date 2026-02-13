import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { PieChart, List, Sliders } from 'lucide-react';

const AttributionAnalysis = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/reporting/attribution');
            if (res.data.success) setData(res.data.data);
        };
        load();
    }, []);

    if (!data) return <div>Loading Attribution...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <PieChart className="text-purple-500" /> Attribution Analysis
                </h1>
                <p className="text-slate-500">Brinson-Fachler Model: Breaking Down Returns</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Excess Return</div>
                    <div className="text-3xl font-bold text-white">{data.total_excess_return}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Allocation Effect</div>
                    <div className="text-3xl font-bold text-blue-400">{data.allocation_effect}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Selection Effect</div>
                    <div className="text-3xl font-bold text-emerald-400">{data.selection_effect}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Interaction Effect</div>
                    <div className="text-3xl font-bold text-orange-400">{data.interaction_effect}%</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4">Sector Contribution Breakdown</h3>
                <div className="space-y-4">
                    {data.sector_breakdown.map((s, i) => (
                        <div key={i} className="flex items-center gap-4">
                            <div className="w-32 font-bold text-slate-300">{s.sector}</div>
                            <div className="flex-1 bg-slate-950 h-4 rounded-full overflow-hidden relative">
                                <div 
                                    className={`h-full absolute top-0 ${s.contribution > 0 ? 'bg-emerald-500 left-1/2' : 'bg-red-500 right-1/2'}`}
                                    style={{ width: `${Math.abs(s.contribution) * 20}%` }} // Scaling for visual
                                ></div>
                                <div className="absolute left-1/2 top-0 h-full w-px bg-slate-700"></div>
                            </div>
                            <div className={`w-16 text-right font-bold ${s.contribution > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {s.contribution > 0 ? '+' : ''}{s.contribution}%
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AttributionAnalysis;
