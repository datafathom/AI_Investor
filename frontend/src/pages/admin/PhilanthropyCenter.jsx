import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Heart, Globe } from 'lucide-react';

const PhilanthropyCenter = () => {
    const [summary, setSummary] = useState(null);
    const [missions, setMissions] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [sRes, mRes] = await Promise.all([
                apiClient.get('/philanthropy/summary'),
                apiClient.get('/philanthropy/missions')
            ]);
            if (sRes.data.success) setSummary(sRes.data.data);
            if (mRes.data.success) setMissions(mRes.data.data);
        };
        load();
    }, []);

    if (!summary) return <div>Loading Philanthropy Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Heart className="text-pink-500" /> Philanthropy Mission Center
                </h1>
                <p className="text-slate-500">Mission-Driven Giving & Impact Tracking</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Lifetime Giving</div>
                    <div className="text-3xl font-bold text-pink-400">${summary.lifetime_giving.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">DAF Balance</div>
                    <div className="text-3xl font-bold text-white">${summary.daf_balance.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Impact Score</div>
                    <div className="text-3xl font-bold text-emerald-400">{summary.impact_score}/100</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Top Pillar</div>
                    <div className="text-xl font-bold text-blue-400">{summary.top_pillar}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                        <Globe size={18} className="text-blue-500" /> Active Missions
                    </h3>
                    <div className="space-y-6">
                        {missions.map(m => (
                            <div key={m.id}>
                                <div className="flex justify-between text-sm mb-1">
                                    <span className="font-bold text-white">{m.name}</span>
                                    <span className="text-slate-400">{m.goal}</span>
                                </div>
                                <div className="h-4 bg-slate-950 rounded-full overflow-hidden">
                                    <div className="h-full bg-blue-500" style={{ width: `${m.progress * 100}%` }}></div>
                                </div>
                                <div className="text-right text-xs text-blue-400 mt-1">{(m.progress * 100).toFixed(0)}% Funded</div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center text-center">
                    <Heart size={64} className="text-pink-900/50 mb-4" />
                    <h3 className="text-xl font-bold text-white">Donor Advised Fund (DAF)</h3>
                    <p className="text-slate-500 text-sm mt-2 max-w-xs">
                        Your philanthropic capital is ready to deploy. Grant recommendations can be made instantly.
                    </p>
                    <button className="mt-6 bg-pink-600 hover:bg-pink-500 text-white font-bold py-2 px-6 rounded">
                        RECOMMEND A GRANT
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PhilanthropyCenter;
