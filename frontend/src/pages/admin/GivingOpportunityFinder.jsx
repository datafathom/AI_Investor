import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Radar, Sparkles } from 'lucide-react';

const GivingOpportunityFinder = () => {
    const [opps, setOpps] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/philanthropy/opportunities');
            if (res.data.success) setOpps(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Sparkles className="text-yellow-500" /> Impact Opportunity Finder
                </h1>
                <p className="text-slate-500">AI-Matched Giving Opportunities</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {opps.map((o, i) => (
                    <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-yellow-500/50 transition-colors cursor-pointer">
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="text-xl font-bold text-white">{o.name}</h3>
                            <div className="bg-slate-950 text-emerald-400 font-bold text-sm px-2 py-1 rounded border border-slate-800">
                                {o.match_score}% MATCH
                            </div>
                        </div>
                        <p className="text-slate-400 text-sm mb-6">{o.reason}</p>
                        
                        <div className="flex gap-2">
                            <button className="flex-1 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold py-2 rounded">
                                VIEW PROFILE
                            </button>
                            <button className="flex-1 bg-yellow-600 hover:bg-yellow-500 text-white text-xs font-bold py-2 rounded">
                                SHORTLIST
                            </button>
                        </div>
                    </div>
                ))}

                <div className="bg-slate-900 border border-slate-800 border-dashed rounded-xl p-6 flex flex-col justify-center items-center text-center opacity-50 hover:opacity-100 transition-opacity cursor-pointer">
                    <Radar size={48} className="text-slate-500 mb-2" />
                    <h3 className="font-bold text-white">Scan for More</h3>
                    <p className="text-xs text-slate-500">Analyze new 990 filings</p>
                </div>
            </div>
        </div>
    );
};

export default GivingOpportunityFinder;
