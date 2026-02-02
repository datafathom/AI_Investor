import React, { useState, useEffect, useRef } from 'react';
import apiClient from '../services/apiClient';
import { MessageSquare, Scale, TrendingUp, TrendingDown, ShieldCheck, AlertOctagon, Send } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import SentimentGraph from '../components/Debate/SentimentGraph';
import ConsensusMeter from '../components/Debate/ConsensusMeter';
import ArgumentTree from '../widgets/Debate/ArgumentTree';

const ResponsiveGridLayout = WidthProvider(Responsive);

const DebateRoom = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'podium', x: 0, y: 0, w: 3, h: 8 },
            { i: 'transcript', x: 3, y: 0, w: 6, h: 8 },
            { i: 'verdict', x: 9, y: 0, w: 3, h: 4 },
            { i: 'sentiment', x: 9, y: 4, w: 3, h: 4 }
        ]
    };
    const STORAGE_KEY = 'layout_debate_room';

    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const [loading, setLoading] = useState(false);
    const [displayedResponses, setDisplayedResponses] = useState([]);
    const [result, setResult] = useState(null);
    const transcriptEndRef = useRef(null);

    // Live Data Loop
    useEffect(() => {
        // Start debate on load
        startDebate();
        
        // Poll for updates
        const interval = setInterval(fetchUpdates, 3000);
        return () => clearInterval(interval);
    }, []);

    const startDebate = async () => {
        setLoading(true);
        try {
            const res = await apiClient.post('/ai/debate/start', { ticker: 'SPY' });
            const data = res.data;
            updateState(data);
        } catch (e) {
            console.error("Debate start failed", e);
        } finally {
            setLoading(false);
        }
    };

    const fetchUpdates = async () => {
        try {
            const res = await apiClient.get('/ai/debate/stream');
            const data = res.data;
            updateState(data);
        } catch (e) {
            console.error("Polling failed", e);
        }
    };

    const updateState = (data) => {
        if (!data || !data.transcript) return;
        setDisplayedResponses(data.transcript);
        setResult({ consensus: data.consensus });
    };

    const handleInject = async (e) => {
        e.preventDefault();
        const input = e.target.elements.argument.value;
        if (!input) return;
        
        e.target.reset(); // clear input immediately for UX
        
        // Optimistic update (optional, but good for UX)
        // setDisplayedResponses(prev => [...prev, { persona: 'User', reasoning: input, role: 'Human' }]);

        try {
            await apiClient.post('/ai/debate/inject', { argument: input });
            fetchUpdates(); // trigger immediate refresh
        } catch (e) {
            console.error("Injection failed", e);
        }
    };

    useEffect(() => {
        transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [displayedResponses]);

    return (
        <div className="full-bleed-page debate-room-container text-slate-300 font-sans">
            <header className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-amber-900/20 border border-amber-500/30 rounded-full">
                        <Scale size={32} className="text-amber-500" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-black text-white tracking-tight italic">DEBATE CHAMBER</h1>
                        <p className="text-xs text-amber-500 font-mono tracking-widest uppercase">Multi-Agent Strategic Consensus</p>
                    </div>
                </div>
                <div className="text-right font-mono">
                    <div className="text-slate-500 text-[10px] uppercase">Session Hash</div>
                    <div className="text-white text-xs">LIVE-Orch-v2</div>
                </div>
            </header>

            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={80}
                    isDraggable={true}
                    isResizable={true}
                    draggableHandle=".glass-panel"
                    margin={[16, 16]}
                >
                    {/* Left: The Podium (Agents) */}
                    <div key="podium" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <div className="h-full flex flex-col gap-4">
                            <AgentPodium
                                name="The Bull" role="Growth Advocate" color="green"
                                icon={<TrendingUp size={24} />} active={true}
                            />
                            <AgentPodium
                                name="The Bear" role="Skeptic & Critic" color="red"
                                icon={<TrendingDown size={24} />} active={true}
                            />
                            <AgentPodium
                                name="The Risk Manager" role="Capital Guardian" color="blue"
                                icon={<ShieldCheck size={24} />} active={true}
                            />

                            <div className="glass-panel p-4 bg-slate-900/40 border border-slate-800 rounded-xl flex-1 flex flex-col min-h-[200px]">
                                <h3 className="text-xs font-bold text-slate-500 uppercase mb-2 text-center">Debate Structure</h3>
                                <ArgumentTree transcript={displayedResponses} />
                            </div>
                        </div>
                    </div>

                    {/* Center: Live Transcript */}
                    <div key="transcript" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <div className="glass-panel w-full h-full flex flex-col bg-slate-900/30 border border-slate-800 rounded-xl overflow-hidden relative">
                            <div className="p-4 border-b border-slate-800 bg-slate-900/30 flex justify-between items-center cursor-move" style={{ cursor: 'move' }}>
                                <span className="text-xs font-mono text-slate-500 uppercase flex items-center gap-2">
                                    <MessageSquare size={14} /> Official Transcript
                                </span>
                                <div className="flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                                    <span className="text-green-500 text-[10px] font-mono">LIVE FEED</span>
                                </div>
                            </div>

                            <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
                                {displayedResponses.map((resp, idx) => (
                                    <div key={idx} className={`transcript-entry flex flex-col gap-2 ${resp.persona === 'The Bull' ? 'items-start' : resp.persona === 'The Bear' ? 'items-end' : resp.persona === 'User' ? 'items-end' : 'items-center'}`}>
                                        <div className="flex items-center gap-2">
                                            <span className={`text-[10px] font-black uppercase tracking-widest ${resp.persona === 'The Bull' ? 'text-green-400' : resp.persona === 'The Bear' ? 'text-red-400' : resp.persona === 'User' ? 'text-purple-400' : 'text-blue-400'}`}>
                                                {resp.persona}
                                            </span>
                                        </div>
                                        <div className={`p-4 rounded-2xl max-w-[80%] border text-sm shadow-xl transition-all hover:scale-[1.01] cursor-default glass-premium ${resp.persona === 'The Bull' ? 'bg-green-950/20 border-green-500/30 text-green-100' :
                                            resp.persona === 'The Bear' ? 'bg-red-950/20 border-red-500/30 text-red-100' :
                                            resp.persona === 'User' ? 'bg-purple-950/20 border-purple-500/30 text-purple-100' :
                                                'bg-blue-950/20 border-blue-500/30 text-blue-100 text-center'
                                            }`}>
                                            {resp.reasoning}
                                        </div>
                                    </div>
                                ))}
                                <div ref={transcriptEndRef} />
                            </div>

                            {/* Input Area */}
                            <form onSubmit={handleInject} className="p-4 border-t border-slate-800 bg-black/40 flex gap-2">
                                <input 
                                    name="argument"
                                    type="text" 
                                    placeholder="Inject an argument (e.g., 'What about inflation?')..." 
                                    className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-amber-500 transition-colors"
                                />
                                <button type="submit" className="p-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg transition-colors">
                                    <Send size={18} />
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* Right: Verdict & Metrics */}
                    <div key="verdict" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <div className="glass-panel p-6 flex flex-col items-center justify-center bg-slate-900/40 border border-slate-800 rounded-xl h-full glass-premium shadow-amber-900/20">
                            <h3 className="text-amber-200 font-bold mb-8 flex items-center gap-2 uppercase tracking-widest text-xs">
                                <Scale size={16} /> Final Decision
                            </h3>
                            {result && result.consensus && (
                                <div className="w-full space-y-8">
                                    <ConsensusMeter score={result.consensus.buy_ratio * 100} />
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="text-center p-3 bg-black/40 rounded-lg border border-slate-800">
                                            <div className="text-[10px] text-slate-500 uppercase">Conviction</div>
                                            <div className="text-2xl font-black text-white">{result.consensus.score}/10</div>
                                        </div>
                                        <div className="text-center p-3 bg-black/40 rounded-lg border border-slate-800">
                                            <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Signal</div>
                                            <div className={`text-xl font-black ${result.consensus.is_approved === false && result.consensus.decision === 'HOLD' ? 'text-amber-400' : result.consensus.decision === 'BUY' ? 'text-green-400 text-glow-cyan' : 'text-red-400 text-glow-red'}`}>
                                                {result.consensus.decision}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    <div key="sentiment" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                        <div className="glass-panel p-4 flex-1 bg-slate-900/40 border border-slate-800 rounded-xl flex flex-col h-full">
                            <h3 className="text-xs font-bold text-slate-500 uppercase mb-4 text-center">Bull/Bear Sentiment Oscillator</h3>
                            <div className="flex-1">
                                <SentimentGraph />
                            </div>
                        </div>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

const AgentPodium = ({ name, role, color, icon, active }) => (
    <div className={`p-4 border-l-4 rounded-r-xl transition-all cursor-crosshair hover:scale-[1.05] interact-hover ${color === 'green' ? 'border-green-500 bg-green-950/20 shadow-green-950/50' :
        color === 'red' ? 'border-red-500 bg-red-950/20 shadow-red-950/50' :
            'border-blue-500 bg-blue-950/20 shadow-blue-950/50'
        } ${active ? 'opacity-100 shadow-2xl glass-premium' : 'opacity-40'}`}>
        <div className="flex items-center gap-4">
            <div className={`p-2 rounded-lg transition-transform duration-300 group-hover:scale-110 ${color === 'green' ? 'text-green-400 bg-green-400/10' :
                color === 'red' ? 'text-red-400 bg-red-400/10' :
                    'text-blue-400 bg-blue-400/10'
                } ${active ? 'animate-neon-pulse' : ''}`}>
                {icon}
            </div>
            <div>
                <h4 className="text-white font-bold text-sm tracking-tight group-hover:text-glow-cyan transition-all">{name}</h4>
                <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest">{role}</p>
            </div>
        </div>
    </div>
);

const getMockDebateData = (ticker) => ({
    ticker: ticker,
    responses: [
        { persona: 'The Bull', signal: 'BUY', reasoning: `${ticker} momentum is accelerating after a key breakout. Order flow shows massive institutional size on the bid.` },
        { persona: 'The Bear', signal: 'SELL', reasoning: `Macro headwinds are rising. ${ticker} is overextended on the weekly RSI. Expect a mean reversion soon.` },
        { persona: 'The Risk Manager', signal: 'HOLD', reasoning: `Correlations across sectors are peaking. Defensive sizing is recommended until IV crushes.` }
    ],
    consensus: {
        decision: 'HOLD',
        is_approved: false,
        buy_ratio: 0.5,
        avg_score: 5.2
    }
});

export default DebateRoom;
