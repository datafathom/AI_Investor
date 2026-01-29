import React, { useState } from 'react';
import { GitFork, TrendingUp, TrendingDown, Clock, Activity, Zap } from 'lucide-react';
import useAlgoStore from '../../stores/algoStore';

/**
 * Sprint 6: Shadow Strategy Panel
 * Allows users to fork a live strategy into a "shadow" parallel simulation
 * to see projected 24h divergence before committing changes.
 */
const ShadowStrategyPanel = ({ strategy, userId }) => {
    const { forkToShadow, isLoading } = useAlgoStore();
    const [shadowFork, setShadowFork] = useState(null);
    const [forking, setForking] = useState(false);

    // Mock divergence data for demo - in production this would come from backend
    const mockDivergence = {
        liveReturn: 2.3,
        shadowReturn: 3.1,
        divergence: 0.8,
        timeToProject: '1.2s',
        confidence: 87
    };

    const handleForkToShadow = async () => {
        if (!strategy?.id) return;
        setForking(true);
        try {
            const result = await forkToShadow(strategy.id, userId);
            if (result) {
                setShadowFork({
                    ...result,
                    divergence: mockDivergence
                });
            }
        } finally {
            setForking(false);
        }
    };

    if (!strategy) {
        return (
            <div className="h-full flex flex-col items-center justify-center p-6 bg-slate-900/50 rounded-xl border border-slate-800">
                <GitFork size={32} className="text-slate-600 mb-3" />
                <p className="text-slate-500 text-sm text-center">Select a strategy to enable Shadow Mode</p>
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col p-4 bg-slate-900/50 rounded-xl border border-slate-800">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <GitFork size={16} className="text-purple-400" />
                    <h3 className="text-white text-sm font-bold">Shadow Engine</h3>
                </div>
                <span className="text-[9px] uppercase tracking-widest text-slate-500 font-mono">Phase 51</span>
            </div>

            {/* Strategy Info */}
            <div className="bg-black/40 rounded-lg p-3 mb-4 border border-slate-800">
                <p className="text-xs text-slate-400 mb-1">Active Strategy</p>
                <p className="text-white text-sm font-bold truncate">{strategy.name || strategy.id}</p>
                <p className="text-emerald-400 text-[10px] mt-1 flex items-center gap-1">
                    <Activity size={10} /> LIVE
                </p>
            </div>

            {/* Fork Button */}
            {!shadowFork ? (
                <button
                    onClick={handleForkToShadow}
                    disabled={forking || isLoading}
                    className="w-full py-3 px-4 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-300 text-sm font-bold hover:bg-purple-500/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {forking ? (
                        <>
                            <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
                            Forking...
                        </>
                    ) : (
                        <>
                            <GitFork size={16} />
                            Copy to Shadow
                        </>
                    )}
                </button>
            ) : (
                /* Divergence Results */
                <div className="flex-1 space-y-3">
                    <div className="flex items-center justify-center gap-2 text-emerald-400 text-xs animate-pulse">
                        <Zap size={12} />
                        <span>Shadow simulation complete in {mockDivergence.timeToProject}</span>
                    </div>

                    {/* Divergence Metrics */}
                    <div className="grid grid-cols-2 gap-2">
                        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3 text-center">
                            <p className="text-[9px] uppercase text-blue-400 mb-1">Live Return</p>
                            <p className="text-xl font-black text-white flex items-center justify-center gap-1">
                                {mockDivergence.liveReturn > 0 ? <TrendingUp size={16} className="text-emerald-400" /> : <TrendingDown size={16} className="text-red-400" />}
                                {mockDivergence.liveReturn.toFixed(1)}%
                            </p>
                        </div>
                        <div className="bg-purple-500/10 border border-purple-500/20 rounded-lg p-3 text-center">
                            <p className="text-[9px] uppercase text-purple-400 mb-1">Shadow Return</p>
                            <p className="text-xl font-black text-white flex items-center justify-center gap-1">
                                {mockDivergence.shadowReturn > 0 ? <TrendingUp size={16} className="text-emerald-400" /> : <TrendingDown size={16} className="text-red-400" />}
                                {mockDivergence.shadowReturn.toFixed(1)}%
                            </p>
                        </div>
                    </div>

                    {/* Divergence Bar */}
                    <div className="bg-black/40 rounded-lg p-3 border border-slate-800">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-[10px] text-slate-400 uppercase">24h Projected Divergence</span>
                            <span className={`text-sm font-bold ${mockDivergence.divergence > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {mockDivergence.divergence > 0 ? '+' : ''}{mockDivergence.divergence.toFixed(1)}%
                            </span>
                        </div>
                        <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                            <div 
                                className="h-full bg-gradient-to-r from-purple-500 to-emerald-500 transition-all"
                                style={{ width: `${Math.min(mockDivergence.confidence, 100)}%` }}
                            />
                        </div>
                        <p className="text-[9px] text-slate-500 mt-1 text-right">
                            Confidence: {mockDivergence.confidence}%
                        </p>
                    </div>

                    {/* Reset Button */}
                    <button
                        onClick={() => setShadowFork(null)}
                        className="w-full py-2 text-slate-400 text-xs hover:text-white transition-colors"
                    >
                        ← Run New Simulation
                    </button>
                </div>
            )}
        </div>
    );
};

export default ShadowStrategyPanel;
