import React from 'react';
import { Clock, TrendingUp, TrendingDown, ExternalLink, Bookmark } from 'lucide-react';

const NewsCard = ({ article, onClick }) => {
  const getSentimentColor = (label) => {
    if (label === 'Positive') return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (label === 'Negative') return 'text-red-400 border-red-500/30 bg-red-500/10';
    return 'text-slate-400 border-slate-600/30 bg-slate-600/10';
  };

  return (
    <div 
        onClick={() => onClick(article)}
        className="bg-slate-900/50 border border-slate-800 rounded-lg p-4 hover:border-cyan-500/50 hover:bg-slate-800 transition-all cursor-pointer group"
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-2">
          <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">
            {article.source}
          </span>
          <span className="text-slate-600">•</span>
          <div className="flex items-center gap-1 text-xs text-slate-400">
            <Clock size={12} />
            <span>{new Date(article.published_at).toLocaleTimeString()}</span>
          </div>
        </div>
        
        <div className={`px-2 py-0.5 rounded text-[10px] font-mono border ${getSentimentColor(article.sentiment_label)}`}>
            {article.sentiment_label}
        </div>
      </div>

      <h3 className="text-sm font-semibold text-slate-200 mb-2 leading-tight group-hover:text-cyan-400 transition-colors">
        {article.title}
      </h3>

      <div className="flex items-center gap-2 mt-3">
        {article.tickers.slice(0, 3).map(t => (
            <span key={t} className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-cyan-500 border border-slate-700">
                ${t}
            </span>
        ))}
        {article.tags.slice(0, 2).map(t => (
            <span key={t} className="text-[10px] text-slate-500">
                #{t}
            </span>
        ))}
      </div>
    </div>
  );
};

export default NewsCard;
