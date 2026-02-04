import React from 'react';
import SentimentChart from '../Analytics/SentimentChart';
import TensorMonitor from '../Analytics/TensorMonitor';
import { Activity, ArrowUpRight, TrendingUp, Cpu } from 'lucide-react';

const MonitorWidget = () => {
    // Mock Tensor Data (Phase 11) - In production this comes from DataFusionService
    const mockTensor = {
        symbol: "TSLA",
        timestamp: new Date().toISOString(),
        aggregate_score: 0.642,
        tensor: {
            price_momentum: 0.72,
            retail_sentiment: 0.85,  // High retail hype
            smart_money: 0.45,       // Institutional caution
            macro_health: 0.20       // Recession warning
        }
    };

    const mockSentimentData = [
        { timestamp: '2026-01-16T00:00:00Z', score: 0.2 },
        { timestamp: '2026-01-16T04:00:00Z', score: -0.5 },
        { timestamp: '2026-01-16T08:00:00Z', score: 0.8 },
        { timestamp: '2026-01-16T12:00:00Z', score: 0.3 },
        { timestamp: '2026-01-16T16:00:00Z', score: 0.1 },
    ];

    const stats = [
        { name: 'System Alpha', value: '1.42%', icon: <Activity className="text-cyan-400" /> },
        { name: 'Active Agents', value: '4', icon: <Cpu className="text-purple-400" /> },
        { name: 'Hype Index', value: 'BULLISH', icon: <TrendingUp className="text-green-400" /> },
    ];

    return (
        <div className="space-y-4 p-4 h-full overflow-auto">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {stats.map((stat) => (
                    <div key={stat.name} className="glass-card flex items-center justify-between p-4">
                        <div>
                            <p className="text-dim text-xs">{stat.name}</p>
                            <h4 className="text-xl font-bold text-main mt-1">{stat.value}</h4>
                        </div>
                        <div className="p-2 bg-white/5 rounded-lg border border-white/5">
                            {stat.icon}
                        </div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {/* Real-time Tensor Monitor (Phase 11) */}
                <div className="lg:col-span-1">
                    <TensorMonitor tensor={mockTensor} collapsible={true} />
                </div>

                {/* Live Order Tape */}
                <div className="glass-card lg:col-span-1 p-4">
                    <h3 className="neon-text mb-4">Live Tape</h3>
                    <div className="space-y-2">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="flex items-center justify-between p-2 bg-white/5 rounded border-l-2 border-cyan-500">
                                <div className="flex items-center gap-2">
                                    <span className="font-bold text-main text-sm">TSLA</span>
                                    <span className="text-[10px] text-dim">11:28:42</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="text-green-400 text-sm">+$2.42</span>
                                    <ArrowUpRight size={12} className="text-green-400" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Sentiment Chart */}
                <div className="lg:col-span-2">
                    <SentimentChart data={mockSentimentData} />
                </div>
            </div>
        </div>
    );
};

export default MonitorWidget;
