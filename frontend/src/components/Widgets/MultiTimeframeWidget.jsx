import React, { useState, useEffect } from 'react';
import { chartService } from '../../services/chartService';
import { AreaChart, Area, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { LayoutGrid, ArrowUp, ArrowDown, Minus } from 'lucide-react';

const MiniChart = ({ data, trend }) => {
    const color = trend === 'BULLISH' || trend === 'STRONG BULLISH' ? '#10b981' : 
                  trend === 'BEARISH' || trend === 'STRONG BEARISH' ? '#ef4444' : '#64748b';
    
    // Mock data if real data isn't passed for simplicity of this widget
    const mockData = data || Array.from({length: 20}, (_, i) => ({
        val: Math.random() * 10 + (trend.includes('BULLISH') ? i : trend.includes('BEARISH') ? 20-i : 10)
    }));

    return (
        <div className="h-24 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockData}>
                    <defs>
                        <linearGradient id={`grad-${trend}`} x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor={color} stopOpacity={0.3}/>
                            <stop offset="95%" stopColor={color} stopOpacity={0}/>
                        </linearGradient>
                    </defs>
                    <Area type="monotone" dataKey="val" stroke={color} fill={`url(#grad-${trend})`} strokeWidth={2} />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export const MultiTimeframeWidget = ({ ticker = 'AAPL' }) => {
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await chartService.getMTFAnalysis(ticker);
                setAnalysis(res);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [ticker]);

    if (loading) return <div className="animate-pulse h-64 bg-slate-900 rounded-xl"></div>;
    if (!analysis) return null;

    const getIcon = (trend) => {
        if (trend.includes("BULLISH")) return <ArrowUp size={16} className="text-emerald-500" />;
        if (trend.includes("BEARISH")) return <ArrowDown size={16} className="text-red-500" />;
        return <Minus size={16} className="text-slate-500" />;
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-full">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider flex items-center gap-2">
                    <LayoutGrid size={16} /> MTF Analysis: <span className="text-white">{ticker}</span>
                </h3>
                <div className={`px-3 py-1 rounded-full text-xs font-bold border ${
                    analysis.overall_signal.includes("BULLISH") ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                    analysis.overall_signal.includes("BEARISH") ? "bg-red-500/10 text-red-400 border-red-500/20" :
                    "bg-slate-800 text-slate-400 border-slate-700"
                }`}>
                    {analysis.overall_signal}
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
                {Object.entries(analysis.timeframes).map(([tf, data]) => (
                    <div key={tf} className="bg-slate-950 border border-slate-800 rounded-lg p-3">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-xs font-bold text-slate-300">{tf}</span>
                            <div className="flex items-center gap-1">
                                {getIcon(data.trend)}
                                <span className="text-[10px] font-mono text-slate-500">{data.trend}</span>
                            </div>
                        </div>
                        <MiniChart trend={data.trend} />
                        <div className="flex justify-between mt-2 text-[10px] text-slate-500 font-mono">
                            <span>RSI: {data.rsi}</span>
                            <span>MACD: {data.macd}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
