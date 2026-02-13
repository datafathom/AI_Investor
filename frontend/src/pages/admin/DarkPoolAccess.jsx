import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { EyeOff, Globe, Lock } from 'lucide-react';

const DarkPoolAccess = () => {
    const [venues, setVenues] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/orders/dark/venues');
            if (res.data.success) setVenues(res.data.data);
        };
        load();
    }, []);

    const routeOrder = async (venueName) => {
        await apiClient.post('/orders/dark/route', null, { params: { venue: venueName } });
        alert(`Order Routed to ${venueName}`);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <EyeOff className="text-slate-400" /> Dark Pool Access
                </h1>
                <p className="text-slate-500">Non-Displayed Liquidity Venues & Block Trading</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {venues.map(v => (
                    <div key={v.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-slate-600 transition-colors">
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="text-xl font-bold text-white">{v.name}</h3>
                            <Lock size={18} className="text-slate-500" />
                        </div>
                        <div className="flex items-center gap-2 text-sm text-slate-400 mb-6">
                            <Globe size={14} /> Global Equities
                        </div>
                        
                        <div className="flex justify-between items-center mb-6">
                            <span className="text-xs uppercase text-slate-500 font-bold">Liquidity Profile</span>
                            <span className={`px-2 py-0.5 rounded text-xs font-bold ${v.liquidity === 'HIGH' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                                {v.liquidity}
                            </span>
                        </div>

                        <button 
                            onClick={() => routeOrder(v.name)}
                            className="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold py-2 rounded text-sm"
                        >
                            ROUTE ORDER
                        </button>
                    </div>
                ))}
            </div>

            <div className="mt-12 p-6 bg-slate-900 border border-slate-800 rounded-xl">
                <h3 className="font-bold text-white mb-2">Dark Pool Rules & Compliance</h3>
                <ul className="list-disc list-inside text-sm text-slate-400 space-y-1">
                    <li>Minimum block size requirements may apply (e.g., 10k shares).</li>
                    <li>Refer to Best Execution Policy regarding dark venue prioritization.</li>
                    <li>IOIs (Indications of Interest) are non-binding.</li>
                </ul>
            </div>
        </div>
    );
};

export default DarkPoolAccess;
