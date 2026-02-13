import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Target, CheckCircle } from 'lucide-react';

const RobustnessLab = () => {
    const [score, setScore] = useState(null);
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        const load = async () => {
            const sRes = await apiClient.get('/stress/robustness/score');
            if (sRes.data.success) setScore(sRes.data.data);
            
            const rRes = await apiClient.post('/stress/hardening/optimize');
            if (rRes.data.success) setRecommendations(rRes.data.data);
        };
        load();
    }, []);

    if (!score) return <div>Loading Robustness Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Target className="text-green-500" /> Robustness Scorecard
                </h1>
                <p className="text-slate-500">Hardening Lab & Portfolio Optimization</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center text-center">
                    <div className="text-6xl font-black text-white mb-2">{score.score}</div>
                    <div className="text-emerald-400 font-bold uppercase tracking-widest text-sm mb-6">{score.rating}</div>
                    
                    <div className="w-full space-y-2 text-left">
                        <div className="text-xs uppercase text-slate-500 font-bold">Strengths</div>
                        <div className="flex flex-wrap gap-2">
                            {score.strengths.map((s, i) => (
                                <span key={i} className="bg-emerald-900/30 text-emerald-400 px-2 py-1 rounded text-xs border border-emerald-900">{s}</span>
                            ))}
                        </div>
                        
                        <div className="text-xs uppercase text-slate-500 font-bold mt-4">Weaknesses</div>
                        <div className="flex flex-wrap gap-2">
                            {score.weaknesses.map((w, i) => (
                                <span key={i} className="bg-red-900/30 text-red-400 px-2 py-1 rounded text-xs border border-red-900">{w}</span>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6">Hardening Recommendations</h3>
                    <div className="space-y-4">
                        {recommendations.map((rec, i) => (
                            <div key={i} className="flex justify-between items-center p-4 bg-slate-950 rounded border border-slate-800 hover:border-green-500/50 transition-colors cursor-pointer group">
                                <div className="flex items-center gap-4">
                                    <div className="bg-slate-800 p-2 rounded-full text-slate-400 group-hover:text-green-400 group-hover:bg-green-900/20">
                                        <CheckCircle size={20} />
                                    </div>
                                    <div>
                                        <div className="font-bold text-white">{rec.action}</div>
                                        <div className="text-xs text-slate-500">Protection: {rec.protection}</div>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <div className="text-white font-bold">${rec.cost.toLocaleString()}</div>
                                    <div className="text-xs text-slate-500">Est. Cost</div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <button className="w-full mt-6 bg-slate-800 hover:bg-slate-700 text-white font-bold py-3 rounded text-sm">
                        EXECUTE ALL OPTIMIZATIONS
                    </button>
                </div>
            </div>
        </div>
    );
};

export default RobustnessLab;
