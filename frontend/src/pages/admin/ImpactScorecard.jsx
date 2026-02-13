import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Leaf, Scale, Users } from 'lucide-react';

const ImpactScorecard = () => {
    const [scores, setScores] = useState(null);
    const [alignment, setAlignment] = useState(null);

    useEffect(() => {
        const load = async () => {
            const [sRes, aRes] = await Promise.all([
                apiClient.get('/philanthropy/scores'),
                apiClient.get('/philanthropy/alignment')
            ]);
            if (sRes.data.success) setScores(sRes.data.data);
            if (aRes.data.success) setAlignment(aRes.data.data);
        };
        load();
    }, []);

    if (!scores) return <div>Loading Impact Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Leaf className="text-green-500" /> Impact Scorecard & ESG Mirror
                </h1>
                <p className="text-slate-500">Portfolio Sustainability & SDGs</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center">
                    <div className="text-5xl font-black text-white mb-2">{scores.esg_total}</div>
                    <div className="text-emerald-400 font-bold uppercase tracking-widest text-sm">ESG Score</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex items-center gap-2 mb-2 font-bold text-slate-300">
                        <Leaf size={16} className="text-green-500" /> Environment
                    </div>
                    <div className="text-2xl font-bold text-white">{scores.environmental}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex items-center gap-2 mb-2 font-bold text-slate-300">
                        <Users size={16} className="text-blue-500" /> Social
                    </div>
                    <div className="text-2xl font-bold text-white">{scores.social}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex items-center gap-2 mb-2 font-bold text-slate-300">
                        <Scale size={16} className="text-purple-500" /> Governance
                    </div>
                    <div className="text-2xl font-bold text-white">{scores.governance}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Alignment Analysis</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-slate-300">Aligned Holdings</span>
                            <span className="font-bold text-emerald-400">{alignment?.aligned_holdings}%</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-red-900/30">
                            <span className="text-slate-300">Misaligned Holdings</span>
                            <span className="font-bold text-red-400">{alignment?.misaligned_holdings}%</span>
                        </div>
                        
                        <div>
                            <div className="text-xs uppercase text-slate-500 font-bold mb-2">Red Flags</div>
                            <div className="flex flex-wrap gap-2">
                                {alignment?.flags.map((f, i) => (
                                    <span key={i} className="bg-red-900/30 text-red-300 px-2 py-1 rounded text-xs border border-red-900">{f}</span>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">SDG Mapping</h3>
                    <div className="space-y-2">
                        {scores.sdg_alignment.map((sdg, i) => (
                            <div key={i} className="flex items-center gap-3 p-2 bg-slate-950 rounded border border-slate-800">
                                <div className="w-8 h-8 rounded bg-gradient-to-br from-blue-500 to-green-500 flex items-center justify-center text-white font-bold text-xs">
                                    {i+1}
                                </div>
                                <span className="font-bold text-slate-300">{sdg}</span>
                            </div>
                        ))}
                    </div>
                    <div className="mt-4 pt-4 border-t border-slate-800 text-sm text-slate-500">
                        Carbon Footprint: <span className="text-emerald-400 font-bold">{scores.carbon_footprint}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ImpactScorecard;
