import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Lightbulb, Plus, MoreHorizontal } from 'lucide-react';

const OpportunityTracker = () => {
    const [opps, setOpps] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/opportunities/');
            if (res.data.success) setOpps(res.data.data);
        };
        load();
    }, []);

    const columns = ['NEW', 'RESEARCHING', 'READY', 'ACTIVE', 'CLOSED'];

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Lightbulb className="text-amber-500" /> Opportunity Tracker
                    </h1>
                    <p className="text-slate-500">Investment Thesis & Idea Pipeline</p>
                </div>
                <button className="bg-amber-600 hover:bg-amber-500 text-black px-4 py-2 rounded font-bold flex items-center gap-2">
                    <Plus size={18} /> NEW IDEA
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 h-[600px]">
                {columns.map(col => (
                    <div key={col} className="bg-slate-900 border border-slate-800 rounded-xl flex flex-col h-full">
                        <div className="p-3 border-b border-slate-800 font-bold text-slate-400 text-xs uppercase flex justify-between">
                            {col}
                            <span className="bg-slate-800 text-slate-500 px-2 rounded-full">{opps.filter(o => o.status === col).length}</span>
                        </div>
                        <div className="p-2 space-y-2 flex-1 overflow-y-auto">
                            {opps.filter(o => o.status === col).map(o => (
                                <div key={o.id} className="bg-slate-800 p-3 rounded hover:bg-slate-700 cursor-grab active:cursor-grabbing shadow-sm border border-slate-700">
                                    <div className="flex justify-between items-start mb-2">
                                        <h4 className="font-bold text-white text-sm">{o.title}</h4>
                                        <button className="text-slate-500 hover:text-white"><MoreHorizontal size={14} /></button>
                                    </div>
                                    <p className="text-xs text-slate-400 line-clamp-3 mb-3">{o.thesis}</p>
                                    <div className="flex justify-between items-center">
                                        <span className={`text-[10px] font-bold px-1 rounded ${
                                            o.conviction >= 8 ? 'bg-green-500/20 text-green-400' : 'bg-slate-700 text-slate-400'
                                        }`}>
                                            CONF: {o.conviction}/10
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default OpportunityTracker;
