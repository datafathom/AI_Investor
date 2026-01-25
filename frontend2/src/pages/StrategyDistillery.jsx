import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';
import { Dna, Zap, Play, FlaskConical, GitBranch, Search, TrendingUp } from 'lucide-react';
import BattleArena from '../components/Strategy/BattleArena';
import ComparisonMatrix from '../components/Strategy/ComparisonMatrix';
import RiskEditor from '../components/Strategy/RiskEditor';
import PageHeader from '../components/Navigation/PageHeader';
import './StrategyDistillery.css';

/**
 * Strategy Distillery Page
 * Theme: Biotech / Lab (Clean White/Teal, Dark Mode support, Hexagons)
 */
const StrategyDistillery = () => {
    const [generation, setGeneration] = useState(42);
    const [isEvolving, setIsEvolving] = useState(false);
    const [evolutionData, setEvolutionData] = useState([]);

    // Mock Genome Data
    const [genomeData] = useState([
        { subject: 'Momentum', A: 80, fullMark: 100 },
        { subject: 'Mean Rev', A: 45, fullMark: 100 },
        { subject: 'Volatility', A: 60, fullMark: 100 },
        { subject: 'Sentiment', A: 90, fullMark: 100 },
        { subject: 'Macro', A: 30, fullMark: 100 },
        { subject: 'Risk', A: 50, fullMark: 100 },
    ]);

    useEffect(() => {
        // Generate mock evolution data
        const data = Array.from({ length: 50 }, (_, i) => ({
            gen: i,
            fitness: 50 + Math.log(i + 1) * 10 + Math.random() * 5,
            avg: 40 + Math.log(i + 1) * 8
        }));
        setEvolutionData(data);
    }, []);

    useEffect(() => {
        let interval;
        if (isEvolving) {
            interval = setInterval(() => {
                setGeneration(g => g + 1);
                setEvolutionData(prev => {
                    const last = prev[prev.length - 1];
                    return [...prev.slice(1), {
                        gen: last.gen + 1,
                        fitness: last.fitness + (Math.random() - 0.3),
                        avg: last.avg + (Math.random() - 0.4)
                    }];
                });
            }, 500);
        }
        return () => clearInterval(interval);
    }, [isEvolving]);

    return (
        <div className="full-bleed-page strategy-distillery-page">
            <header className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-fuchsia-900/30 rounded-xl border border-fuchsia-500/30 interact-hover">
                        <FlaskConical size={32} className="text-fuchsia-400 group-hover:animate-bounce" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-fuchsia-300 to-purple-300">
                            Strategy Distillery
                        </h1>
                        <p className="text-slate-400 text-sm">Evolutionary Optimization Lab</p>
                    </div>
                </div>
                <div className="flex gap-4">
                    <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-lg border border-slate-700">
                        <Dna size={18} className="text-fuchsia-400" />
                        <span className="font-mono text-sm">GEN: <span className="text-white font-bold">{generation}</span></span>
                    </div>
                    <button
                        onClick={() => setIsEvolving(!isEvolving)}
                        className={`flex items-center gap-2 px-6 py-2 rounded-lg font-bold transition-all interact-hover ${isEvolving ? 'bg-fuchsia-900/50 border border-fuchsia-500 text-fuchsia-300 shadow-[0_0_20px_rgba(192,38,211,0.4)]' : 'bg-fuchsia-600 hover:bg-fuchsia-500 shadow-lg shadow-fuchsia-500/20'}`}
                    >
                        {isEvolving ? <Zap size={18} className="animate-neon-pulse" /> : <Play size={18} />}
                        {isEvolving ? "EVOLVING..." : "START EVOLUTION"}
                    </button>
                </div>
            </header>

            <div className="scrollable-content-wrapper">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* LEFT COLUMN: Main Charts */}
                    <div className="lg:col-span-2 flex flex-col gap-6">
                        {/* Evolution Chart */}
                        <div className="glass-panel p-6 h-[400px] relative overflow-hidden glass-premium shadow-emerald-900/20">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-lg font-bold text-emerald-400 flex items-center gap-2">
                                    <Search size={20} /> Evolutionary Trajectory
                                </h3>
                                <div className="flex gap-4 text-xs font-mono text-slate-400">
                                    <span>Pop: 1000</span>
                                    <span>Mut: 0.05</span>
                                </div>
                            </div>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={evolutionData}>
                                    <defs>
                                        <linearGradient id="colorFit" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                    <XAxis dataKey="gen" stroke="#475569" tick={{ fontSize: 10 }} />
                                    <YAxis stroke="#475569" domain={['auto', 'auto']} tick={{ fontSize: 10 }} />
                                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                                    <Area type="monotone" dataKey="fitness" stroke="#10b981" fillOpacity={1} fill="url(#colorFit)" strokeWidth={2} />
                                    <Area type="monotone" dataKey="avg" stroke="#64748b" strokeDasharray="5 5" fill="transparent" strokeWidth={1} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        {/* New Strategy Analysis Section */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[300px]">
                            <BattleArena />
                            <div className="glass-panel p-4 overflow-hidden">
                                <ComparisonMatrix />
                            </div>
                        </div>
                    </div>

                    {/* RIGHT COLUMN: Genome & Controls */}
                    <div className="lg:col-span-1 flex flex-col gap-6">
                        <div className="glass-panel p-6 glass-premium shadow-purple-900/20">
                            <h3 className="text-lg font-bold text-purple-400 mb-4 flex items-center gap-2">
                                <Dna size={20} /> Active Genome
                            </h3>
                            <div className="h-48 mb-6">
                                <ResponsiveContainer width="100%" height="100%">
                                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={genomeData}>
                                        <PolarGrid stroke="#334155" />
                                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                                        <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                                        <Radar name="Alpha Candidate" dataKey="A" stroke="#c026d3" fill="#c026d3" fillOpacity={0.4} />
                                    </RadarChart>
                                </ResponsiveContainer>
                            </div>

                            <RiskEditor />
                        </div>

                        {/* Top Candidates List (Compact) */}
                        <div className="glass-panel p-4 flex-1">
                            <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Top Candidates</h4>
                            <div className="space-y-2">
                                {[1, 2, 3, 4, 5].map(i => (
                                    <div key={i} className="flex justify-between items-center p-2 bg-slate-800/50 rounded border border-slate-700/50 hover:border-purple-500/50 transition-all hover:scale-[1.02] cursor-pointer group interact-hover text-xs">
                                        <div className="flex flex-col">
                                            <span className="text-slate-300 font-mono">Strat_Gen{generation}_{i}</span>
                                            <span className="text-[10px] text-slate-500">Sharpe: {(2.5 - i * 0.1).toFixed(2)}</span>
                                        </div>
                                        <button className="text-purple-400 hover:text-white">
                                            <GitBranch size={14} />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default StrategyDistillery;
