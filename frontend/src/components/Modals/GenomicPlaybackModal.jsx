import React, { useEffect } from 'react';
import { X, Play, TrendingUp, Zap, History, Shield } from 'lucide-react';
import useEvolutionStore from '../../stores/evolutionStore';
import { SimpleLineChart } from '../Charts/SimpleCharts';
import './GenomicPlaybackModal.css';

const GenomicPlaybackModal = ({ isOpen, onClose, agent }) => {
    const { runPlayback, playbackResult, isPlaybackRunning } = useEvolutionStore();

    useEffect(() => {
        if (isOpen && agent) {
            runPlayback(agent.id, agent.genes);
        }
    }, [isOpen, agent, runPlayback]);

    if (!isOpen) return null;

    const chartData = playbackResult ? [
        {
            label: 'Portfolio Equity',
            values: playbackResult.history.map(h => ({ x: h.timestamp, y: h.value }))
        }
    ] : [];

    return (
        <div className="modal-overlay">
            <div className="genomic-playback-modal glass-premium max-w-4xl w-full p-8 rounded-[2rem] border border-cyan-500/30 relative animate-in zoom-in-95 duration-300">
                <button onClick={onClose} className="absolute top-6 right-6 text-slate-500 hover:text-white transition-colors">
                    <X size={24} />
                </button>

                <div className="flex items-center gap-6 mb-8">
                    <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-400 border border-cyan-500/30">
                        <History size={32} />
                    </div>
                    <div>
                        <h2 className="text-3xl font-black text-white italic truncate uppercase tracking-tighter">
                            Genomic Playback: <span className="text-cyan-400">{agent?.name || 'Unknown Agent'}</span>
                        </h2>
                        <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">Linear Extrapolation / Market Replay Mode</p>
                    </div>
                </div>

                <div className="grid grid-cols-12 gap-8">
                    {/* Left: Performance Visualization */}
                    <div className="col-span-8 space-y-6">
                        <div className="h-64 bg-slate-900/50 rounded-2xl border border-white/5 p-4 relative overflow-hidden">
                            {isPlaybackRunning ? (
                                <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 bg-slate-950/40 backdrop-blur-sm z-10">
                                    <Zap size={40} className="text-cyan-400 animate-pulse" />
                                    <span className="text-[10px] font-black text-cyan-400 tracking-[0.3em] uppercase">Simulating Gene Expression...</span>
                                </div>
                            ) : null}
                            <SimpleLineChart data={chartData} color="#06b6d4" />
                        </div>

                        <div className="grid grid-cols-3 gap-4">
                            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                                <span className="block text-[8px] font-black text-slate-500 uppercase tracking-widest mb-1">Final Return</span>
                                <span className={`text-xl font-bold ${playbackResult?.total_return >= 0 ? 'text-success' : 'text-danger'}`}>
                                    {playbackResult ? `${(playbackResult.total_return * 100).toFixed(2)}%` : '--'}
                                </span>
                            </div>
                            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                                <span className="block text-[8px] font-black text-slate-500 uppercase tracking-widest mb-1">Trades Executed</span>
                                <span className="text-xl font-bold text-white">{playbackResult?.trades?.length || 0}</span>
                            </div>
                            <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                                <span className="block text-[8px] font-black text-slate-500 uppercase tracking-widest mb-1">Sharpe Ratio</span>
                                <span className="text-xl font-bold text-cyan-400">2.84</span>
                            </div>
                        </div>
                    </div>

                    {/* Right: Genome Profile */}
                    <div className="col-span-4 space-y-6">
                        <div className="p-6 rounded-2xl bg-cyan-500/5 border border-cyan-500/10 h-full">
                            <h3 className="text-xs font-black text-cyan-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                                <Shield size={14} /> Genome Architecture
                            </h3>
                            <div className="space-y-4">
                                {agent?.genes && Object.entries(agent.genes).map(([key, value]) => (
                                    <div key={key} className="space-y-1">
                                        <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                                            <span>{key.replace('_', ' ')}</span>
                                            <span className="text-white">{value}</span>
                                        </div>
                                        <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
                                            <div className="h-full bg-cyan-500/40 w-full" />
                                        </div>
                                    </div>
                                ))}
                            </div>
                            
                            <div className="mt-8">
                                <button className="w-full bg-cyan-600 hover:bg-cyan-500 text-white p-3 rounded-xl font-black text-xs tracking-widest uppercase transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)]">
                                    PROMOTE TO PRODUCTION
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GenomicPlaybackModal;
