import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BarChart2, Layers } from 'lucide-react';

const PerformanceAttribution = () => {
    const [attrib, setAttrib] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/portfolio/analysis/attribution');
            if (res.data.success) setAttrib(res.data.data);
        };
        load();
    }, []);

    if (!attrib) return <div>Loading Attribution...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BarChart2 className="text-indigo-500" /> Performance Attribution
                </h1>
                <p className="text-slate-500">Brinson Analysis & Sources of Return</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Excess Return</div>
                    <div className="text-3xl font-bold text-emerald-400 font-mono">+{attrib.total_excess}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Allocation Effect</div>
                    <div className="text-3xl font-bold text-blue-400 font-mono">+{attrib.allocation_effect}%</div>
                    <div className="text-xs text-slate-500 mt-1">Asset Class Weighting</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Selection Effect</div>
                    <div className="text-3xl font-bold text-purple-400 font-mono">+{attrib.selection_effect}%</div>
                    <div className="text-xs text-slate-500 mt-1">Stock Picking Skill</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <Layers size={18} className="text-slate-400" /> Sector Contribution
                </h3>
                <div className="space-y-4">
                    {Object.entries(attrib.sectors).map(([sector, val]) => (
                        <div key={sector}>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-300">{sector}</span>
                                <span className={`font-bold ${val >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>{val}%</span>
                            </div>
                            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                <div 
                                    className={`h-full ${val >= 0 ? 'bg-emerald-500' : 'bg-red-500'}`} 
                                    style={{ width: `${Math.abs(val) * 10}%` }} // Mock scaling
                                ></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default PerformanceAttribution;
