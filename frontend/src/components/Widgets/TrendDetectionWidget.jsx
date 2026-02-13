import React, { useState, useEffect } from 'react';
import { socialService } from '../../services/socialService';
import TrendVelocityChart from '../charts/TrendVelocityChart';
import { Zap, TrendingUp, TrendingDown, Hash } from 'lucide-react';
import { toast } from 'sonner';

const TrendDetectionWidget = () => {
    const [trends, setTrends] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadTrends = async () => {
            try {
                const data = await socialService.getTrends();
                setTrends(data);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        loadTrends();
    }, []);

    if (loading) return <div className="animate-pulse h-64 bg-slate-900 rounded-xl"></div>;

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden h-full flex flex-col">
            <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                <h3 className="font-bold text-white flex items-center gap-2">
                    <Zap className="text-amber-400" size={18} /> Emerging Trends
                </h3>
                <span className="text-xs text-slate-500 uppercase font-bold tracking-wider">Live</span>
            </div>
            
            <div className="overflow-y-auto flex-1 p-2 space-y-2">
                {trends.map((trend, idx) => (
                    <div key={trend.id} className="p-3 rounded-lg bg-slate-800/30 hover:bg-slate-800 border border-slate-700/50 transition-all group">
                        <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-2">
                                <span className="text-slate-500 font-mono text-xs">#{idx + 1}</span>
                                <h4 className="font-bold text-slate-200 text-sm">{trend.topic}</h4>
                            </div>
                            <div className="flex items-center gap-1 text-xs font-mono text-amber-400">
                                <Zap size={12} />
                                {trend.velocity}x
                            </div>
                        </div>

                        <div className="flex items-center gap-2 mb-2">
                            {trend.related_tickers.map(t => (
                                <span key={t} className="text-[10px] px-1.5 py-0.5 rounded bg-slate-700 text-cyan-400 border border-slate-600">
                                    ${t}
                                </span>
                            ))}
                        </div>

                        <div className="flex justify-between items-end">
                            <div className="text-[10px] text-slate-500">
                                {trend.mentions_1h.toLocaleString()} mentions / 1h
                            </div>
                            <div className="w-24 h-8 opacity-50 group-hover:opacity-100 transition-opacity">
                                <TrendVelocityChart color="#fbbf24" />
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TrendDetectionWidget;
