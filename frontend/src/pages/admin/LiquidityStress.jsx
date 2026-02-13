import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Droplets, Clock } from 'lucide-react';

const LiquidityStress = () => {
    const [data, setData] = useState(null);

    const runTest = async () => {
        const res = await apiClient.post('/stress/liquidity/test');
        if (res.data.success) setData(res.data.data);
    };

    useEffect(() => {
        runTest();
    }, []);

    if (!data) return <div>Running Liquidity Stress Test...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Droplets className="text-cyan-500" /> Liquidity Stress Analyzer
                </h1>
                <p className="text-slate-500">Bid-Ask Spread Expansion & Gap Risk</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Simulated Spread</div>
                    <div className="text-3xl font-bold text-white">{data.bid_ask_spread_mult}x</div>
                    <div className="text-xs text-slate-500 mt-2">Normal Expansion</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 border-b-4 border-b-orange-500">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Time to Liquidate</div>
                    <div className="text-3xl font-bold text-orange-400">{data.days_to_liquidate} Days</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Slippage Cost</div>
                    <div className="text-3xl font-bold text-red-400">${data.slippage_cost.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Forced Sale Disc.</div>
                    <div className="text-3xl font-bold text-slate-200">{(data.forced_sale_discount * 100).toFixed(0)}%</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col items-center justify-center min-h-[300px]">
                <Clock size={48} className="text-slate-600 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Liquidity Drain Simulation</h3>
                <div className="w-full max-w-2xl bg-slate-950 h-64 rounded border border-slate-800 flex items-end px-4 gap-1 relative overflow-hidden">
                    {/* Fake Chart Bars for Visual */}
                    {Array.from({ length: 20 }).map((_, i) => (
                        <div 
                            key={i} 
                            className="bg-cyan-900 hover:bg-cyan-500 transition-colors flex-1" 
                            style={{ height: `${100 - (i * 5)}%`, opacity: 0.5 + (i * 0.02) }}
                        ></div>
                    ))}
                    <div className="absolute top-4 left-4 text-xs font-mono text-cyan-500">LIQUIDITY_DEPTH_CHART</div>
                </div>
                <p className="text-slate-500 mt-4 text-sm text-center">
                    Visualization of market depth decay over {data.days_to_liquidate} days.
                </p>
            </div>
        </div>
    );
};

export default LiquidityStress;
