import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Play, AlertTriangle } from 'lucide-react';
import SentimentChart from '../Analytics/SentimentChart';

const BacktestDemo = () => {
    const [isRunning, setIsRunning] = useState(false);
    const [results, setResults] = useState(null);

    const mockSentimentData = [
        { timestamp: '2026-01-16T00:00:00Z', score: 0.2 },
        { timestamp: '2026-01-16T04:00:00Z', score: -0.5 },
        { timestamp: '2026-01-16T08:00:00Z', score: 0.8 },
        { timestamp: '2026-01-16T12:00:00Z', score: 0.3 },
        { timestamp: '2026-01-16T16:00:00Z', score: 0.1 },
    ];

    const handleStart = () => {
        setIsRunning(true);
        setTimeout(() => {
            setResults({
                return: "+14.2%",
                sharpe: "2.1",
                trades: 42,
                winRate: "68%"
            });
            setIsRunning(false);
        }, 2000);
    };

    return (
        <div className="p-4 h-full flex flex-col gap-4">
            <header>
                <h1 className="neon-text text-2xl mb-1">Simulation Command</h1>
                <p className="text-dim text-xs">Phase 23 Backtesting Engine v0.1 | Hybrid NLP Sentiment Fusion</p>
            </header>

            <div className="flex-1 flex flex-col gap-4 overflow-auto">
                <div className="glass-card flex flex-col justify-between p-4">
                    <div>
                        <h3 className="neon-text mb-2 text-sm">Engine Control</h3>
                        <div className="space-y-2 text-xs">
                            <div className="flex justify-between">
                                <span className="text-dim">Strategy:</span>
                                <span className="text-cyan-400">Crowd_Wisdom_V1</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-dim">Symbol:</span>
                                <span className="text-cyan-400">NVDA / TSLA</span>
                            </div>
                        </div>
                    </div>

                    <button
                        onClick={handleStart}
                        disabled={isRunning}
                        className={`mt-4 flex items-center justify-center gap-2 p-2 rounded font-bold text-xs transition-all ${isRunning ? 'bg-gray-800' : 'bg-cyan-500/20 border border-cyan-500 hover:bg-cyan-500/40'
                            }`}
                    >
                        {isRunning ? 'RUNNING...' : <><Play size={14} /> START BACKTEST</>}
                    </button>
                </div>

                {results && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card border-neon-purple shadow-[0_0_15px_rgba(188,19,254,0.3)] p-4"
                    >
                        <h3 className="text-purple-400 mb-2 font-display text-sm">Execution Results</h3>
                        <div className="grid grid-cols-2 gap-2">
                            <div className="text-center p-2 bg-white/5 rounded">
                                <div className="text-dim text-[10px]">TOTAL RETURN</div>
                                <div className="text-lg text-green-400 font-bold">{results.return}</div>
                            </div>
                            <div className="text-center p-2 bg-white/5 rounded">
                                <div className="text-dim text-[10px]">SHARPE RATIO</div>
                                <div className="text-lg text-cyan-400 font-bold">{results.sharpe}</div>
                            </div>
                            <div className="text-center p-2 bg-white/5 rounded">
                                <div className="text-dim text-[10px]">TRADES</div>
                                <div className="text-lg text-purple-400">{results.trades}</div>
                            </div>
                            <div className="text-center p-2 bg-white/5 rounded">
                                <div className="text-dim text-[10px]">WIN RATE</div>
                                <div className="text-lg text-yellow-400">{results.winRate}</div>
                            </div>
                        </div>
                    </motion.div>
                )}

                <div className="h-48">
                    <SentimentChart data={mockSentimentData} />
                </div>
            </div>

            <div className="glass-card border-red-500/30 p-3 mt-auto">
                <h3 className="text-red-500 flex items-center gap-2 mb-1 text-xs font-bold">
                    <AlertTriangle size={14} /> System Guards
                </h3>
                <p className="text-dim text-[10px]">
                    ProtectorAgent active. Simulation uses 0.1% slippage.
                </p>
            </div>
        </div>
    );
};

export default BacktestDemo;
