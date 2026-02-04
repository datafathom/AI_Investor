import React from 'react';
import { Radar } from 'lucide-react';
import GlassCard from '../Controls/GlassCard';

const TensorMonitor = ({ tensor, collapsible = false }) => {
    // : Safety check against empty data
    // We access tensor.tensor for the individual components to avoid iterating over the wrapper object
    const data = tensor?.tensor || {
        price_momentum: 0.5,
        retail_sentiment: 0.5,
        smart_money: 0.5,
        macro_health: 0.5
    };

    // Helper to calculate bar width percentage
    const getWidth = (val) => Math.min(Math.max(val, 0) * 100, 100) + '%';

    // Helper for color coding (Low=Red, Mid=Yellow, High=Green)
    const getColor = (val) => {
        if (val < 0.3) return 'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]';
        if (val < 0.7) return 'bg-yellow-400 shadow-[0_0_10px_rgba(250,204,21,0.5)]';
        return 'bg-green-400 shadow-[0_0_10px_rgba(74,222,128,0.5)]';
    };

    return (
        <GlassCard title="MARKET STATE TENSOR" subTitle="Normalized Data Fusion [0.0 - 1.0]" collapsible={collapsible}>
            <div className="space-y-6 mt-4">

                {/* Aggregate Score */}
                <div className="flex items-center justify-between mb-6 pb-6 border-b border-cyan-500/10">
                    <div className="flex items-center gap-3">
                        <Radar className="text-cyan-400" size={24} />
                        <div>
                            <div className="text-xs text-dim uppercase tracking-wider">Aggregate Pulse</div>
                            <div className="text-2xl font-bold text-white font-mono">
                                {(tensor?.aggregate_score || 0.5).toFixed(3)}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tensor Components */}
                {Object.entries(data).map(([key, value]) => {
                    // Safety: Ensure value is a number before calling toFixed
                    const numericValue = typeof value === 'number' ? value : 0.5;

                    return (
                        <div key={key} className="space-y-1">
                            <div className="flex justify-between text-xs uppercase tracking-widest text-dim">
                                <span>{key.replace('_', ' ')}</span>
                                <span className="text-cyan-300 font-mono">{numericValue.toFixed(2)}</span>
                            </div>
                            <div className="h-2 w-full bg-black/40 rounded-full overflow-hidden border border-white/5">
                                <div
                                    className={`h-full rounded-full transition-all duration-1000 ${getColor(numericValue)}`}
                                    style={{ width: getWidth(numericValue) }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="mt-6 text-[10px] text-center text-white/20 uppercase tracking-widest">
                Data Fusion Layer  {new Date().toLocaleTimeString()}
            </div>
        </GlassCard>
    );
};

export default TensorMonitor;
