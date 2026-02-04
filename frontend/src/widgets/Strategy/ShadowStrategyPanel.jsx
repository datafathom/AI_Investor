import React, { useState } from 'react';
import { GitFork, TrendingUp, TrendingDown, Clock, Activity, Zap, BarChart2 } from 'lucide-react';
import useAlgoStore from '../../stores/algoStore';
import useScenarioStore from '../../stores/scenarioStore';

/**
 * Sprint 6: Shadow Strategy Panel (Enhanced)
 * Allows users to fork a live strategy into a "shadow" parallel simulation
 * to see projected 30-day divergence using real GBM simulation via ScenarioService.
 */
const ShadowStrategyPanel = ({ strategy, userId }) => {
    const { forkToShadow, isLoading: isAlgoLoading } = useAlgoStore();
    const { runShadowRun, isSimulating, impactResults } = useScenarioStore();
    const [shadowFork, setShadowFork] = useState(null);
    const [forking, setForking] = useState(false);

    const shadowResult = impactResults?.shadowRun;

    const handleForkToShadow = async () => {
        if (!strategy?.id) return;
        setForking(true);
        try {
            // 1. Fork the strategy record in the DB
            const result = await forkToShadow(strategy.id, userId);
            
            // 2. Run the actual What-If simulation
            const baselineParams = { mu: 0.08, sigma: 0.15 }; // Default baseline
            const shadowParams = { mu: 0.12, sigma: 0.22 };  // Default shadow (e.g., more aggressive)
            
            await runShadowRun(1000000, baselineParams, shadowParams, 30);
            
            setShadowFork(result);
        } catch (err) {
            console.error('Shadow fork/sim failed:', err);
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
                <span className="text-[9px] uppercase tracking-widest text-slate-500 font-mono">Phase 51 | SPRINT 6</span>
            </div>

            {/* Strategy Info */}
            <div className="bg-black/40 rounded-lg p-3 mb-4 border border-slate-800">
                <p className="text-xs text-slate-400 mb-1">Active Strategy</p>
                <div className="flex justify-between items-center">
                    <p className="text-white text-sm font-bold truncate">{strategy.name || strategy.id}</p>
                    <p className="text-emerald-400 text-[10px] flex items-center gap-1">
                        <Activity size={10} /> LIVE
                    </p>
                </div>
            </div>

            {/* Fork Button */}
            {!shadowResult ? (
                <div className="space-y-4">
                    <div className="text-[10px] text-slate-500 bg-slate-800/20 p-2 rounded border border-slate-800/50 leading-relaxed">
                        Forking creates a parallel execution path in "Ghost Mode". 
                        The engine will run a Geometric Brownian Motion projection using current volatility vectors.
                    </div>
                    <button
                        onClick={handleForkToShadow}
                        disabled={forking || isSimulating || isAlgoLoading}
                        className="w-full py-3 px-4 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-300 text-sm font-bold hover:bg-purple-500/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {forking || isSimulating ? (
                            <>
                                <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
                                Simulating Fork...
                            </>
                        ) : (
                            <>
                                <GitFork size={16} />
                                Initialize Shadow Simulation
                            </>
                        )}
                    </button>
                </div>
            ) : (
                /* Divergence Results */
                <div className="flex-1 space-y-3 overflow-y-auto pr-1 custom-scrollbar">
                    <div className="flex items-center justify-center gap-2 text-emerald-400 text-xs animate-pulse">
                        <Zap size={12} />
                        <span>Projection complete (Horizon: {shadowResult.horizon_days}d)</span>
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-2 gap-2">
                        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                            <p className="text-[9px] uppercase text-blue-400 mb-1">Baseline Exp.</p>
                            <p className="text-lg font-black text-white">
                                ${ (shadowResult.paths[shadowResult.paths.length-1].baseline / 1000).toFixed(0) }k
                            </p>
                        </div>
                        <div className="bg-purple-500/10 border border-purple-500/20 rounded-lg p-3">
                            <p className="text-[9px] uppercase text-purple-400 mb-1">Shadow Exp.</p>
                            <p className="text-lg font-black text-white">
                                ${ (shadowResult.paths[shadowResult.paths.length-1].shadow / 1000).toFixed(0) }k
                            </p>
                        </div>
                    </div>

                    {/* Divergence Card */}
                    <div className="bg-black/40 rounded-lg p-3 border border-slate-800">
                        <div className="flex justify-between items-center mb-1">
                            <span className="text-[10px] text-slate-400 uppercase">Projected Net Divergence</span>
                            <span className={`text-sm font-bold ${shadowResult.divergence > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {shadowResult.divergence > 0 ? '+' : ''}${ (shadowResult.divergence / 1000).toFixed(1) }k
                            </span>
                        </div>
                        
                        <div className="flex items-center gap-2 mt-2">
                             <BarChart2 size={12} className="text-slate-500" />
                             <div className="text-[9px] text-slate-500 uppercase flex-1">Trend Analysis</div>
                        </div>

                        {/* Simple ASCII trend to represent path divergence */}
                        <div className="mt-2 h-12 flex items-end gap-[2px]">
                            {shadowResult.paths.filter((_, i) => i % 2 === 0).map((p, idx) => {
                                const h1 = (p.baseline / shadowResult.initial_value) * 20;
                                const h2 = (p.shadow / shadowResult.initial_value) * 20;
                                return (
                                    <div key={idx} className="flex-1 flex flex-col items-center gap-[1px]">
                                        <div className="w-full bg-blue-500/30 rounded-t" style={{ height: `${h1}px` }} />
                                        <div className="w-full bg-purple-500/50 rounded-t" style={{ height: `${h2}px` }} />
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Controls */}
                    <div className="pt-2 space-y-2">
                        <button
                            className="w-full py-2 bg-emerald-500/20 border border-emerald-500/30 rounded text-emerald-400 text-[10px] font-bold uppercase hover:bg-emerald-500/30 transition-all"
                        >
                            Promote Shadow to Live
                        </button>
                        <button
                            onClick={() => useScenarioStore.getState().reset()}
                            className="w-full py-1 text-slate-500 text-[9px] uppercase tracking-wider hover:text-white transition-colors"
                        >
                            ← Discard & Reset
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ShadowStrategyPanel;
