/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/News/SentimentFlowRadar.jsx
 * ROLE: Real-time Sector Sentiment Heatmap
 * PURPOSE: Visualizes the velocity and magnitude of news sentiment shifts
 *          across major market sectors.
 * ==============================================================================
 */

import React, { useEffect, useMemo } from 'react';
import { Radar, RefreshCcw, TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import useNewsStore from '../../stores/newsStore';
import './SentimentFlowRadar.css';

const SentimentFlowRadar = () => {
    const { sectorSentiment, fetchSectorSentiment, loading } = useNewsStore();

    useEffect(() => {
        fetchSectorSentiment();
        // Poll for updates every 60s
        const interval = setInterval(fetchSectorSentiment, 60000);
        return () => clearInterval(interval);
    }, [fetchSectorSentiment]);

    const sortedSectors = useMemo(() => {
        return [...sectorSentiment].sort((a, b) => b.overall_sentiment - a.overall_sentiment);
    }, [sectorSentiment]);

    const getSentimentColor = (score) => {
        if (score > 0.4) return 'var(--color-success-bold)';
        if (score > 0.1) return 'var(--color-success-muted)';
        if (score < -0.4) return 'var(--color-error-bold)';
        if (score < -0.1) return 'var(--color-error-muted)';
        return 'var(--color-neutral-muted)';
    };

    return (
        <div className="sentiment-radar">
            <div className="sentiment-radar__header">
                <div className="flex items-center gap-2">
                    <Radar size={16} className="text-purple-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Sentiment Flow Radar</h3>
                </div>
                <button 
                    onClick={fetchSectorSentiment} 
                    className={`p-1 hover:bg-white/5 rounded transition-transform ${loading.sectors ? 'animate-spin' : ''}`}
                >
                    <RefreshCcw size={14} className="text-slate-500" />
                </button>
            </div>

            <div className="sentiment-radar__grid">
                {sortedSectors.map((s) => (
                    <div key={s.sector} className="sentiment-radar__card">
                        <div className="flex justify-between items-start mb-1">
                            <span className="text-[10px] font-bold text-slate-400 truncate max-w-[80px]">
                                {s.sector}
                            </span>
                            <div className="flex items-center gap-1">
                                {s.velocity > 0 ? (
                                    <TrendingUp size={10} className="text-emerald-400" />
                                ) : (
                                    <TrendingDown size={10} className="text-red-400" />
                                )}
                            </div>
                        </div>

                        <div className="sentiment-radar__value-box">
                            <div 
                                className="sentiment-radar__bar" 
                                style={{ 
                                    width: `${Math.abs(s.overall_sentiment * 100)}%`,
                                    backgroundColor: getSentimentColor(s.overall_sentiment),
                                    marginLeft: s.overall_sentiment < 0 ? 'auto' : '0',
                                    marginRight: s.overall_sentiment > 0 ? 'auto' : '0',
                                }}
                            />
                        </div>

                        <div className="flex justify-between items-center mt-2">
                            <span className="text-[9px] font-mono text-white/50">{s.article_count} articles</span>
                            <span 
                                className="text-[10px] font-black"
                                style={{ color: getSentimentColor(s.overall_sentiment) }}
                            >
                                {s.overall_sentiment > 0 ? '+' : ''}{s.overall_sentiment.toFixed(2)}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            <div className="sentiment-radar__footer">
                <div className="flex items-center gap-1 text-[9px] text-slate-500">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span>Bullish Alpha</span>
                    <div className="w-2 h-2 rounded-full bg-red-500 ml-2" />
                    <span>Bearish Risk</span>
                </div>
                <div className="text-[9px] font-mono text-slate-600">
                    UPDATED: {new Date().toLocaleTimeString()}
                </div>
            </div>
        </div>
    );
};

export default SentimentFlowRadar;
