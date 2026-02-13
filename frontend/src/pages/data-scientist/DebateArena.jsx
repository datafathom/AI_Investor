import React, { useState, useEffect, useRef } from 'react';
import { debateService } from '../../services/debateService';
import { Play, MessageSquare, Send, Mic, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { ConsensusVotingPanel } from '../../components/debate/ConsensusVotingPanel';
import { toast } from 'sonner';

const SentimentMeter = ({ score }) => {
    // Score 0-100. 0=Bearish, 100=Bullish
    return (
        <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden mt-2 relative">
            <div 
                className="h-full transition-all duration-500 bg-gradient-to-r from-red-500 via-slate-500 to-emerald-500"
                style={{ width: '100%' }}
            />
            <div 
                className="absolute top-0 w-1 h-full bg-white shadow-glow transition-all duration-500"
                style={{ left: `${score}%` }}
            />
        </div>
    );
};

const ParticipantCard = ({ agent }) => (
    <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex flex-col items-center text-center">
        <div className="text-4xl mb-2">{agent.avatar}</div>
        <h3 className="font-bold text-white text-sm">{agent.name}</h3>
        <span className="text-xs text-slate-500 uppercase tracking-wider">{agent.role}</span>
    </div>
);

const DebateMessage = ({ turn }) => {
    const isHuman = turn.is_human;
    const isBull = turn.sentiment === 'BULLISH';
    const isBear = turn.sentiment === 'BEARISH';
    
    const borderColor = isHuman ? 'border-purple-500/50' : isBull ? 'border-emerald-500/30' : isBear ? 'border-red-500/30' : 'border-slate-700';
    const bgColor = isHuman ? 'bg-purple-500/10' : 'bg-slate-800/50';

    return (
        <div className={`flex gap-4 ${isHuman ? 'flex-row-reverse' : ''} mb-4 animate-fade-in`}>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-xl shrink-0 ${isHuman ? 'bg-purple-900 text-purple-200' : 'bg-slate-800'}`}>
                {isHuman ? '👤' : turn.speaker === 'The Bull' ? '🐂' : turn.speaker === 'The Bear' ? '🐻' : '🛡️'}
            </div>
            <div className={`flex-1 p-4 rounded-xl border ${borderColor} ${bgColor}`}>
                <div className="flex justify-between items-center mb-1">
                    <span className={`font-bold text-sm ${isHuman ? 'text-purple-400' : 'text-slate-300'}`}>{turn.speaker}</span>
                    <span className="text-xs text-slate-500">{new Date(turn.timestamp).toLocaleTimeString()}</span>
                </div>
                <p className="text-slate-200 text-sm leading-relaxed">{turn.text}</p>
                {turn.sentiment !== 'NEUTRAL' && (
                    <div className="mt-2 flex gap-2">
                        <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${isBull ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-500'}`}>
                            {turn.sentiment}
                        </span>
                    </div>
                )}
            </div>
        </div>
    );
};

const DebateArena = () => {
    const [ticker, setTicker] = useState('AAPL');
    const [session, setSession] = useState(null);
    const [loading, setLoading] = useState(false);
    const [input, setInput] = useState('');
    const scrollRef = useRef(null);

    const startDebate = async () => {
        setLoading(true);
        try {
            const data = await debateService.startDebate(ticker);
            setSession(data);
        } catch (e) {
            toast.error("Failed to start debate");
        }
        setLoading(false);
    };

    const refreshSession = async () => {
        if (!session) return;
        try {
            const data = await debateService.getSession(session.id);
            // Only update if transcript length changed to prevent jitter
            if (data.transcript.length !== session.transcript.length || data.consensus.score !== session.consensus.score) {
                 setSession(data);
            }
        } catch (e) {
            console.error(e);
        }
    };
    
    // Poll for updates
    useEffect(() => {
        if (session) {
            const interval = setInterval(refreshSession, 2000);
            return () => clearInterval(interval);
        }
    }, [session]);

    // Auto-scroll
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [session?.transcript]);

    const handleInject = async () => {
        if (!input.trim() || !session) return;
        try {
            await debateService.injectArgument(session.id, input, "NEUTRAL"); // Default neutral for now
            setInput('');
            refreshSession();
        } catch (e) {
            toast.error("Failed to inject argument");
        }
    };

    return (
        <div className="h-full bg-slate-950 p-6 text-slate-200 flex flex-col">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                        <MessageSquare className="text-cyan-500" /> AI Debate Arena
                    </h1>
                    <p className="text-slate-500 text-sm">Real-time multi-agent consensus engine</p>
                </div>
                
                {!session && (
                    <div className="flex gap-2">
                        <input 
                            value={ticker}
                            onChange={e => setTicker(e.target.value.toUpperCase())}
                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm w-32 focus:border-cyan-500 outline-none"
                            placeholder="TICKER"
                        />
                        <button 
                            onClick={startDebate}
                            disabled={loading}
                            className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-colors"
                        >
                            <Play size={16} /> {loading ? 'Initializing...' : 'Start Debate'}
                        </button>
                    </div>
                )}
                
                {session && (
                    <div className="flex items-center gap-4">
                        <div className="text-right">
                            <div className="text-xs text-slate-500">CONSENSUS</div>
                            <div className={`font-bold text-xl ${session.consensus.decision === 'BULLISH' ? 'text-emerald-400' : session.consensus.decision === 'BEARISH' ? 'text-red-400' : 'text-slate-300'}`}>
                                {session.consensus.decision}
                            </div>
                        </div>
                        <div className="w-32">
                           <SentimentMeter score={session.consensus.score} />
                        </div>
                    </div>
                )}
            </div>

            {session ? (
                <div className="flex-1 flex gap-6 overflow-hidden">
                    {/* Left: Participants */}
                    <div className="w-64 flex flex-col gap-4 overflow-y-auto">
                        <ConsensusVotingPanel sessionId={session.id} />
                        {session.participants.map((p, i) => (
                            <ParticipantCard key={i} agent={p} />
                        ))}
                    </div>

                    {/* Middle: Transcript */}
                    <div className="flex-1 flex flex-col bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden">
                        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar" ref={scrollRef}>
                            {session.transcript.map(turn => (
                                <DebateMessage key={turn.id} turn={turn} />
                            ))}
                        </div>
                        
                        {/* Input Area */}
                        <div className="p-4 bg-slate-900 border-t border-slate-800 flex gap-2">
                             <input 
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleInject()}
                                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-sm focus:border-cyan-500 outline-none"
                                placeholder="Inject an argument or observation..."
                            />
                            <button 
                                onClick={handleInject}
                                className="bg-purple-600 hover:bg-purple-500 text-white p-3 rounded-lg transition-colors"
                            >
                                <Send size={18} />
                            </button>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="flex-1 flex items-center justify-center text-slate-600">
                    <div className="text-center">
                        <MessageSquare size={48} className="mx-auto mb-4 opacity-50" />
                        <p>Enter a ticker to convene the council of agents.</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DebateArena;
