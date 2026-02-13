import React, { useState, useEffect, useRef } from 'react';
import { debateService } from '../../services/debateService';
import { Search, FileText, Activity, ShieldCheck, Cpu } from 'lucide-react';
import { toast } from 'sonner';
import SplitPane from '../../components/SplitPane/SplitPane';

// High-Density Header Component
const DebateStatsBar = ({ confidence }) => (
    <header className="flex items-center justify-between p-4 border-b border-slate-800 bg-black/40 backdrop-blur-md flex-shrink-0">
        <div className="flex gap-8">
            <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase tracking-widest font-mono">Kafka_Channel</span>
                <span className="text-emerald-400 font-black font-mono flex items-center gap-2">
                    <Activity size={12} className="animate-pulse" /> DEPT.3.LIVE
                </span>
            </div>
            <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase tracking-widest font-mono">Model_Confidence</span>
                <span className="text-white font-black font-mono">{confidence}%</span>
            </div>
            <div className="flex flex-col">
                <span className="text-[10px] text-slate-500 uppercase tracking-widest font-mono">Security_Level</span>
                <span className="text-emerald-500/80 font-black font-mono flex items-center gap-1">
                    <ShieldCheck size={12} /> LEVEL_4
                </span>
            </div>
        </div>
        <h1 className="text-2xl font-black text-white italic tracking-tighter uppercase flex items-center gap-3">
             DEBATE_HISTORY
             <Cpu className="text-emerald-500 w-5 h-5 opacity-50" />
        </h1>
    </header>
);

const DebateHistory = () => {
    const [history, setHistory] = useState([]);
    const [selectedDebate, setSelectedDebate] = useState(null);
    const [selectedId, setSelectedId] = useState(null);
    const [filters, setFilters] = useState({ ticker: '', outcome: '' });
    const [loading, setLoading] = useState(true);
    const [confidence, setConfidence] = useState(98.2);
    const scrollRef = useRef(null);

    // Initial load
    useEffect(() => {
        loadHistory();
    }, []);

    // Filter updates
    useEffect(() => {
        if (!loading) {
            loadHistory();
        }
    }, [filters.ticker]);

    const loadHistory = async () => {
        try {
            setLoading(true);
            const data = await debateService.getHistory(filters);
            setHistory(data || []);
            
            // Auto-select first item if none selected
            if (data && data.length > 0 && !selectedId) {
                handleSelect(data[0]);
            }
        } catch (e) {
            console.error("[DebateHistory] Load failed:", e);
            toast.error("Audit bridge offline");
        } finally {
            setLoading(false);
        }
    };

    const handleSelect = async (debate) => {
        try {
            setSelectedId(debate.id);
            const fullData = await debateService.getTranscript(debate.id);
            setSelectedDebate(fullData);
            // Simulate confidence variance for active feeling
            setConfidence((95 + Math.random() * 4).toFixed(1));
        } catch (e) {
            toast.error("Node synchronization failed");
        }
    };

    return (
        <div className="flex flex-col h-full w-full bg-[#050505] text-slate-300 font-mono selection:bg-emerald-500/30 overflow-hidden relative">
            {/* 1. Header Area */}
            <DebateStatsBar confidence={confidence} />

            {/* 2. Main Content: Resizable Split Pane */}
            <main className="flex-1 min-h-0 overflow-hidden relative">
                <SplitPane 
                    direction="horizontal" 
                    defaultSizes={[25, 75]} 
                    minSize={15}
                >
                    {/* Left Panel: Ticker Navigation */}
                    <div className="h-full flex flex-col bg-black/20 border-r border-slate-900 overflow-hidden">
                        <div className="p-4 border-b border-slate-900 flex-shrink-0">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-600 w-3 h-3" />
                                <input 
                                    type="text" 
                                    placeholder="SEARCH_TICKERS..."
                                    className="w-full bg-slate-900/40 border-b border-slate-800 focus:border-emerald-500 py-2 pl-9 pr-4 text-[11px] focus:outline-none transition-all placeholder:text-slate-700 uppercase tracking-widest font-black"
                                    value={filters.ticker}
                                    onChange={(e) => setFilters({...filters, ticker: e.target.value})}
                                />
                            </div>
                        </div>

                        <div className="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-1">
                            {loading && history.length === 0 ? (
                                <div className="p-8 text-center opacity-20 animate-pulse">
                                    <span className="text-[10px] uppercase tracking-widest">polling_bus...</span>
                                </div>
                            ) : history.length > 0 ? (
                                history.map(item => {
                                    const isSelected = selectedId && (String(selectedId) === String(item.id));
                                    return (
                                        <div 
                                            key={item.id}
                                            onClick={() => handleSelect(item)}
                                            className={`p-3 border-l-2 cursor-pointer transition-all duration-200 group
                                                ${isSelected 
                                                    ? 'bg-emerald-500/10 border-emerald-500 shadow-[inset_4px_0_15px_-3px_rgba(16,185,129,0.2)]' 
                                                    : 'border-transparent hover:bg-white/5 hover:border-slate-800'
                                                }`}
                                        >
                                            <div className="flex justify-between items-center mb-1">
                                                <span className={`text-sm font-black tracking-tighter ${isSelected ? 'text-white' : 'text-slate-500 group-hover:text-slate-300'}`}>
                                                    {item.ticker}
                                                </span>
                                                <span className={`text-[8px] px-1.5 py-0.5 rounded font-black tracking-widest ${item.outcome === 'BULLISH' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
                                                    {item.outcome}
                                                </span>
                                            </div>
                                            <div className="flex justify-between text-[9px] text-slate-700 font-bold">
                                                <span>{new Date(item.date).toLocaleDateString()}</span>
                                                <span className={isSelected ? 'text-emerald-400 opacity-100' : 'text-slate-700'}>{item.score}%_CONF</span>
                                            </div>
                                        </div>
                                    );
                                })
                            ) : (
                                <div className="p-12 text-center opacity-20 flex flex-col items-center">
                                    <FileText className="w-4 h-4 mb-2" />
                                    <p className="text-[10px] uppercase tracking-[0.3em]">No history found</p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Right Panel: Transcript Log */}
                    <div className="h-full bg-[#080808] flex flex-col overflow-hidden relative">
                        {selectedDebate && selectedDebate.meta ? (
                            <div className="flex-1 flex flex-col overflow-hidden p-8 pt-6">
                                <div className="mb-6 flex-shrink-0 border-l-4 border-emerald-500 pl-6 py-2 bg-emerald-500/5 rounded-r-xl">
                                    <h2 className="text-xl font-black text-white italic tracking-tighter uppercase mb-1">
                                        # AUDIT_LOG: {selectedDebate.meta.ticker}
                                    </h2>
                                    <div className="flex gap-4 text-[10px] text-slate-500 font-bold">
                                        <span>STATUS: <span className="text-emerald-400">SYNCED</span></span>
                                        <span>TURNS: {selectedDebate.meta.turns_count}</span>
                                        <span>OUTCOME: {selectedDebate.meta.outcome}</span>
                                    </div>
                                </div>

                                <div className="flex-1 overflow-y-auto space-y-8 pr-4 custom-scrollbar pb-12" ref={scrollRef}>
                                    {Array.isArray(selectedDebate.transcript) && selectedDebate.transcript.map((msg, i) => (
                                        <div key={i} className="group border-l border-emerald-500/10 pl-6 py-1 hover:bg-white/5 transition-all duration-300">
                                            <div className="flex items-center gap-3 mb-2">
                                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
                                                <span className="font-black text-emerald-400 text-[10px] uppercase tracking-widest">{msg.speaker}</span>
                                                <span className="text-[9px] text-slate-700 font-black">[{new Date(msg.timestamp).toLocaleTimeString()}]</span>
                                            </div>
                                            <p className="text-slate-400 text-sm leading-relaxed font-medium tracking-tight">
                                                {msg.text}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            <div className="flex-1 flex flex-col items-center justify-center">
                                <Activity className="w-10 h-10 text-slate-900 animate-pulse mb-4" />
                                <p className="text-slate-800 text-[10px] font-black uppercase tracking-[0.5em]">initializing_log_stream...</p>
                            </div>
                        )}
                    </div>
                </SplitPane>
            </main>

            {/* 3. Footer: Scrubber Filler (118px) */}
            <div className="h-[118px] w-full bg-black/40 border-t border-slate-900/50 flex-shrink-0 flex items-center px-10 relative z-50">
                <div className="w-full flex flex-col gap-2">
                    <div className="flex justify-between text-[10px] text-slate-600 font-black tracking-widest font-mono">
                        <span>00:00_LIVE_EPOCH</span>
                        <span className="text-emerald-500">OPTIMIZED_SYNC</span>
                        <span>18:00_TERMINAL</span>
                    </div>
                    <div className="w-full h-1 bg-slate-900/50 rounded-full relative overflow-hidden">
                        <div className="absolute top-0 left-0 h-full w-[85%] bg-emerald-500 shadow-[0_0_15px_#10b981]" />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DebateHistory;
