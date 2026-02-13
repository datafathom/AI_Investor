import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Building, MapPin, DollarSign } from 'lucide-react';

const RealEstateSuite = () => {
    const [properties, setProperties] = useState([]);
    const [yields, setYields] = useState(null);

    useEffect(() => {
        const load = async () => {
            const [pRes, yRes] = await Promise.all([
                apiClient.get('/assets/real-estate/properties'),
                apiClient.get('/assets/real-estate/yield')
            ]);
            if (pRes.data.success) setProperties(pRes.data.data);
            if (yRes.data.success) setYields(yRes.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Building className="text-orange-500" /> Real Estate Suite
                </h1>
                <p className="text-slate-500">Property Management & Yield Analysis</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Portfolio Cap Rate</div>
                    <div className="text-3xl font-bold text-emerald-400">{yields?.avg_cap_rate}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Net Income</div>
                    <div className="text-3xl font-bold text-white">${yields?.total_net_income.toLocaleString()}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {properties.map(p => (
                    <div key={p.id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden hover:border-slate-600 transition-colors">
                        <div className="h-32 bg-slate-800 flex items-center justify-center text-slate-600">
                            <MapPin size={48} />
                        </div>
                        <div className="p-6">
                            <h3 className="font-bold text-white mb-1">{p.address}</h3>
                            <div className="flex gap-2 mb-4">
                                <span className={`px-2 py-0.5 rounded text-xs font-bold ${p.occupancy === 100 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                                    {p.occupancy}% OCCUPIED
                                </span>
                            </div>
                            
                            <div className="space-y-2 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-slate-400">Cap Rate</span>
                                    <span className="text-white font-bold">{p.cap_rate}%</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-slate-400">Net Income</span>
                                    <span className={`font-bold ${p.net_income > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                        ${p.net_income.toLocaleString()}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RealEstateSuite;
