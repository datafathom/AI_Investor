import React, { useState } from 'react';
import { Search, Info, TrendingUp, TrendingDown, Clock } from 'lucide-react';
import GlassCard from '../Controls/GlassCard';
import Badge from '../Controls/Badge';
import Button from '../Controls/Button';
import OptionsFlowTable from '../Analytics/OptionsFlowTable';

const ResearchWidget = () => {
    const [query, setQuery] = useState('');
    const [mockAlerts, setMockAlerts] = useState([
        { symbol: 'TSLA', type: 'call', strike: '220', expiration: '2026-01-23', volume: '12400', open_interest: '5000', alert_type: 'WHALE_FLOW' },
        { symbol: 'NVDA', type: 'call', strike: '500', expiration: '2026-02-20', volume: '8500', open_interest: '3200', alert_type: 'UNUSUAL_VOLUME' },
        { symbol: 'SPY', type: 'put', strike: '470', expiration: '2026-01-19', volume: '45000', open_interest: '12000', alert_type: 'WHALE_FLOW' }
    ]);

    const results = [
        { symbol: 'TSLA', name: 'Tesla, Inc.', sentiment: 0.82, trending: 'up', source: 'Reddit (r/wsb)' },
        { symbol: 'NVDA', name: 'NVIDIA Corporation', sentiment: 0.94, trending: 'up', source: 'Google Trends' },
        { symbol: 'AMZN', name: 'Amazon.com, Inc.', sentiment: -0.12, trending: 'down', source: 'Combined' },
    ];

    return (
        <div className="space-y-4 p-4 h-full overflow-auto">
            <div className="relative max-w-2xl mx-auto mb-6">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-cyan-400/50" size={20} />
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="DISCOVER ASSET DATA... (e.g. BTC, AI, TECH)"
                    className="w-full bg-white/5 border border-cyan-500/30 rounded-xl p-3 pl-12 text-lg text-main focus:border-cyan-500 shadow-[0_0_20px_rgba(0,242,255,0.1)] outline-none transition-all font-display"
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {results.map((res) => (
                    <GlassCard key={res.symbol} className="hover:border-white/20 cursor-pointer transition-all hover:scale-[1.02]">
                        <div className="flex justify-between items-start mb-2">
                            <div>
                                <h2 className="text-xl font-bold text-main">{res.symbol}</h2>
                                <p className="text-dim text-xs">{res.name}</p>
                            </div>
                            <Badge status={res.sentiment > 0.5 ? 'success' : res.sentiment < 0 ? 'error' : 'info'}>
                                {Math.abs(res.sentiment * 100).toFixed(0)}% ENERGY
                            </Badge>
                        </div>

                        <div className="space-y-2 mt-4">
                            <div className="flex items-center justify-between text-xs p-2 bg-white/5 rounded">
                                <span className="text-dim flex items-center gap-2"><Clock size={12} /> SCAN SOURCE</span>
                                <span className="text-cyan-400">{res.source}</span>
                            </div>
                            <div className="flex items-center justify-between text-xs p-2 bg-white/5 rounded">
                                <span className="text-dim flex items-center gap-2">
                                    {res.trending === 'up' ? <TrendingUp size={12} className="text-green-400" /> : <TrendingDown size={12} className="text-red-400" />}
                                    VELOCITY
                                </span>
                                <span className={res.trending === 'up' ? 'text-green-400' : 'text-red-400'}>HIGH</span>
                            </div>
                        </div>

                        <Button variant="ghost" className="w-full mt-4 flex items-center gap-2 justify-center text-xs">
                            <Info size={14} /> ANALYZE WHALE FLOW
                        </Button>
                    </GlassCard>
                ))}
            </div>

            <div className="mt-6">
                <OptionsFlowTable alerts={mockAlerts} />
            </div>
        </div>
    );
};

export default ResearchWidget;
