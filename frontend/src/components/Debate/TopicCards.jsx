import React from 'react';
import { Tag } from 'lucide-react';

const TopicCards = () => {
    const topics = [
        { label: 'Inflation', sentiment: 'negative', relevance: 98 },
        { label: 'AI Capex', sentiment: 'positive', relevance: 85 },
        { label: 'Labour Market', sentiment: 'neutral', relevance: 72 },
        { label: 'Yield Curve', sentiment: 'negative', relevance: 65 },
        { label: 'Tech Valuations', sentiment: 'positive', relevance: 60 }
    ];

    return (
        <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-500 uppercase px-1 mb-2 flex items-center gap-2">
                <Tag size={12} /> Key Drivers
            </h3>
            <div className="flex flex-wrap gap-2">
                {topics.map((t, i) => (
                    <div
                        key={i}
                        className={`px-3 py-1.5 rounded text-xs font-bold border transition-all hover:scale-105 cursor-default ${t.sentiment === 'positive' ? 'bg-green-500/10 text-green-400 border-green-500/30' :
                                t.sentiment === 'negative' ? 'bg-red-500/10 text-red-400 border-red-500/30' :
                                    'bg-slate-700/30 text-slate-400 border-slate-600'
                            }`}
                        title={`Relevance: ${t.relevance}%`}
                    >
                        {t.label}
                        <span className="ml-1 opacity-50 px-1 bg-black/20 rounded text-[8px]">{t.relevance}%</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TopicCards;
