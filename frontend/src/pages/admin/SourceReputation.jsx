import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ShieldCheck, Star } from 'lucide-react';

const SourceReputation = () => {
    const [sources, setSources] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/reputation/sources');
            if (res.data.success) setSources(res.data.data);
        };
        load();
    }, []);

    const updateScore = async (id, score) => {
        // Mock update
        console.log(`Updating ${id} to ${score}`);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <ShieldCheck className="text-yellow-500" /> Source Reputation Manager
                </h1>
                <p className="text-slate-500">Data Provider Trust Scoring & Reliability</p>
            </header>

            <div className="grid grid-cols-1 gap-6">
                {sources.map(src => (
                    <div key={src.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center justify-between">
                        <div>
                            <div className="flex items-center gap-3">
                                <h3 className="font-bold text-white text-lg">{src.name}</h3>
                                <span className="text-xs text-slate-500 uppercase px-2 py-1 bg-slate-950 rounded">{src.type}</span>
                            </div>
                            <div className="text-sm text-slate-400 mt-1">Error Rate: {src.error_rate}</div>
                            <div className="text-sm text-slate-400">Status: <span className={src.status === 'TRUSTED' ? 'text-emerald-400' : 'text-red-400'}>{src.status}</span></div>
                        </div>
                        
                        <div className="flex items-center gap-4">
                            <div className="text-right">
                                <div className="text-xs uppercase text-slate-500 font-bold">Trust Score</div>
                                <div className="text-3xl font-bold text-white font-mono">{src.trust_score}</div>
                            </div>
                            <div className="flex gap-1">
                                {[1, 2, 3, 4, 5].map(star => (
                                    <Star 
                                        key={star} 
                                        size={20} 
                                        className={`${(src.trust_score / 20) >= star ? 'text-yellow-500 fill-yellow-500' : 'text-slate-700'}`}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SourceReputation;
