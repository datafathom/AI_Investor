import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Activity } from 'lucide-react';

const SentimentHeatmap = () => {
    const [heatmapData, setHeatmapData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
            try {
                const response = await apiClient.get('/social/sentiment/heatmap');
                const result = response.data;
                if (result.status === 'success') {
                    setHeatmapData(result.data);
                }
            } catch (err) {
                console.error("Heatmap fetch error:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
        const interval = setInterval(fetchData, 30000); // refresh every 30s
        return () => clearInterval(interval);
    }, []);

    const getIntensityColor = (value) => {
        // value is -1 to 1
        if (value > 0) {
            return `hsla(var(--success-h), 70%, 50%, ${0.2 + Math.abs(value) * 0.8})`;
        } else {
            return `hsla(var(--danger-h), 70%, 50%, ${0.2 + Math.abs(value) * 0.8})`;
        }
    };

    return (
        <div className="sentiment-heatmap-container glass-premium p-4 rounded-xl h-full flex flex-col">
            <h3 className="text-sm font-semibold mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2 text-primary-light">
                    <Activity size={16} className="text-accent" />
                    Global Sentiment Heatmap
                </div>
                <span className="text-[10px] opacity-50 uppercase tracking-widest">Live Feed</span>
            </h3>

            {loading ? (
                <div className="flex-1 flex items-center justify-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent" />
                </div>
            ) : (
                <div className="grid grid-cols-3 gap-2 flex-1">
                    {heatmapData.map((item) => (
                        <div
                            key={item.id}
                            className="relative group overflow-hidden rounded-lg border border-white/5 transition-transform hover:scale-[1.02] cursor-help"
                            style={{ backgroundColor: 'rgba(255,255,255,0.02)' }}
                        >
                            <div 
                                className="absolute inset-0 opacity-40 transition-opacity group-hover:opacity-60"
                                style={{ backgroundColor: getIntensityColor(item.value) }}
                            />
                            <div className="relative p-3 flex flex-col justify-between h-full">
                                <div className="text-xs font-bold text-white/90">{item.id}</div>
                                <div className="flex items-end justify-between">
                                    <div className="text-[10px] text-white/50">{item.count} Mentions</div>
                                    <div className={`text-xs font-mono font-bold ${item.value > 0 ? 'text-success-light' : 'text-danger-light'}`}>
                                        {(item.value * 100).toFixed(0)}%
                                    </div>
                                </div>
                            </div>
                            {item.value > 0.7 && (
                                <div className="absolute -top-1 -right-1 w-3 h-3 bg-accent rounded-full blur-[4px] animate-pulse" />
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SentimentHeatmap;
