import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { GitBranch, User, FileText } from 'lucide-react';

const EstateVisualizer = () => {
    const [mapData, setMapData] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/wealth/estate/map');
            if (res.data.success) setMapData(res.data.data);
        };
        load();
    }, []);

    if (!mapData) return <div>Loading Estate Map...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <GitBranch className="text-emerald-500" /> Estate Visualizer
                </h1>
                <p className="text-slate-500">Asset Flow & Trust Structure Map</p>
            </header>

            <div className="flex flex-col items-center gap-8">
                {/* Grantor Level */}
                <div className="p-6 bg-slate-900 border border-slate-700 rounded-xl text-center w-64">
                    <div className="bg-emerald-500/20 p-4 rounded-full w-fit mx-auto mb-4">
                        <User size={32} className="text-emerald-400" />
                    </div>
                    <div className="font-bold text-white text-lg">{mapData.grantor}</div>
                    <div className="text-xs uppercase text-slate-500">Grantor</div>
                </div>

                <div className="h-8 w-0.5 bg-slate-700"></div>

                {/* Trust Level */}
                <div className="flex flex-wrap justify-center gap-8 w-full">
                    {mapData.trusts.map(t => (
                        <div key={t.id} className="p-6 bg-slate-900 border border-slate-700 rounded-xl w-64 relative">
                            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-slate-800 text-xs px-2 py-0.5 rounded text-slate-300 border border-slate-600">
                                {t.type}
                            </div>
                            <h3 className="font-bold text-white mb-2 mt-2">{t.name}</h3>
                            <div className="text-emerald-400 font-mono font-bold">${t.assets.toLocaleString()}</div>
                        </div>
                    ))}
                </div>

                <div className="h-8 w-0.5 bg-slate-700"></div>

                {/* Beneficiary Level */}
                <div className="flex flex-wrap justify-center gap-8 w-full">
                    {mapData.beneficiaries.map(b => (
                        <div key={b.id} className="p-4 bg-slate-950 border border-slate-800 rounded-xl w-48 text-center text-sm">
                            <div className="font-bold text-white">{b.name}</div>
                            <div className="text-slate-500 mt-1">Share: {(b.share * 100)}%</div>
                            <div className="mt-2 text-xs text-slate-600 bg-slate-900 py-1 rounded">
                                Designated Beneficiary
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="mt-12 bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <FileText size={18} className="text-slate-400" /> Critical Document Vault
                </h3>
                <div className="flex gap-4">
                     <button className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded text-sm text-slate-300">Start Will.pdf</button>
                     <button className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded text-sm text-slate-300">Trust_Agreement_2024.pdf</button>
                     <button className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded text-sm text-slate-300">POA_Directives.pdf</button>
                </div>
            </div>
        </div>
    );
};

export default EstateVisualizer;
