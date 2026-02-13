import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Loader, TrendingUp, Flame } from 'lucide-react';

const WealthBenchmark = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/wealth/sustainability');
            if (res.data.success) setData(res.data.data);
        };
        load();
    }, []);

    if (!data) return <div>Loading Benchmarks...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                     <Loader className="text-cyan-500" /> Generational Wealth Benchmark
                </h1>
                <p className="text-slate-500">Longevity & Sustainability Analysis</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Sustainability Score</div>
                    <div className="text-4xl font-bold text-emerald-400">{data.sustainability_score}/100</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Years to Exhaustion</div>
                    <div className="text-2xl font-bold text-white">{data.years_until_exhaustion}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Legacy Projection</div>
                    <div className="text-2xl font-bold text-blue-400">${data.legacy_projection.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2 flex items-center gap-1">
                        Lifestyle Burn <Flame size={12} className="text-orange-500" />
                    </div>
                    <div className="text-2xl font-bold text-orange-400">{(data.burn_rate * 100).toFixed(1)}%</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center text-slate-500 min-h-[300px]">
                <TrendingUp size={64} className="mb-4 opacity-20" />
                <p className="text-lg">Monte Carlo Longevity Chart</p>
                <p className="text-sm mt-2">Projection of wealth over next 50 years across 10,000 market scenarios.</p>
            </div>
        </div>
    );
};

export default WealthBenchmark;
