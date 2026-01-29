import React, { useEffect } from 'react';
import { PieChart as PieIcon, RefreshCw, TrendingDown, TrendingUp, Minus } from 'lucide-react';
import useInstitutionalStore from '../../stores/institutionalStore';
import './AssetAllocationWheel.css';

const AssetAllocationWheel = ({ clientId }) => {
    const { assetAllocation, fetchAssetAllocation, loading } = useInstitutionalStore();

    useEffect(() => {
        if (clientId) fetchAssetAllocation(clientId);
    }, [clientId, fetchAssetAllocation]);

    const data = assetAllocation[clientId] || {
        allocations: [],
        total_aum: 0,
        last_rebalanced: ''
    };

    if (loading && !assetAllocation[clientId]) {
        return <div className="asset-allocation-wheel-loading glass-premium">Calculating Weights...</div>;
    }

    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#6366f1', '#ec4899'];

    return (
        <div className="asset-allocation-wheel glass-premium p-6 rounded-3xl border border-white/5">
            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-slate-400 text-xs uppercase tracking-widest font-bold flex items-center gap-2">
                        <PieIcon size={14} className="text-primary" />
                        Asset Allocation
                    </h3>
                    <div className="text-2xl font-bold mt-1">
                        ${(data.total_aum / 1000000).toFixed(1)}M <span className="text-xs text-slate-500 font-normal">AUM</span>
                    </div>
                </div>
                <button className="p-2 rounded-full bg-white/5 text-slate-400 hover:text-primary transition-colors">
                    <RefreshCw size={16} />
                </button>
            </div>

            <div className="flex items-center gap-8 mb-8">
                {/* Donut Chart (Simulated with simple CSS/SVG circle for now) */}
                <div className="relative w-32 h-32 flex-shrink-0">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 32 32">
                        {data.allocations.reduce((acc, curr, idx) => {
                            const offset = acc.total;
                            acc.total += curr.value;
                            acc.elements.push(
                                <circle
                                    key={curr.category}
                                    cx="16" cy="16" r="14"
                                    fill="transparent"
                                    stroke={colors[idx % colors.length]}
                                    strokeWidth="4"
                                    strokeDasharray={`${curr.value} 100`}
                                    strokeDashoffset={-offset}
                                />
                            );
                            return acc;
                        }, { total: 0, elements: [] }).elements}
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-[10px] text-slate-500 font-bold uppercase">Drift</span>
                        <span className="text-sm font-bold text-error">+5.5%</span>
                    </div>
                </div>

                <div className="flex-grow space-y-2">
                    {data.allocations.map((item, idx) => (
                        <div key={item.category} className="flex items-center justify-between group">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: colors[idx % colors.length] }} />
                                <span className="text-xs text-slate-400 group-hover:text-white transition-colors">{item.category}</span>
                            </div>
                            <div className="text-xs font-bold text-white flex items-center gap-4">
                                <span>{item.value}%</span>
                                <div className={`flex items-center gap-0.5 w-12 justify-end ${
                                    item.drift > 0 ? 'text-error' : item.drift < 0 ? 'text-warning' : 'text-success'
                                }`}>
                                    {item.drift > 0 ? <TrendingUp size={10} /> : item.drift < 0 ? <TrendingDown size={10} /> : <Minus size={10} />}
                                    {Math.abs(item.drift)}%
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="pt-6 border-t border-white/5">
                <div className="flex justify-between text-[10px] mb-4">
                    <span className="text-slate-500 uppercase font-bold">Last Rebalanced</span>
                    <span className="text-slate-300 font-bold">{data.last_rebalanced}</span>
                </div>
                <button className="w-full py-3 rounded-xl bg-white/5 border border-white/10 text-white text-xs font-bold hover:bg-primary hover:border-primary transition-all">
                    AUTO-REBALANCE DRIFT
                </button>
            </div>
        </div>
    );
};

export default AssetAllocationWheel;
