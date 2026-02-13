import React from 'react';
import { AlertTriangle, ThumbsUp, ThumbsDown, CheckCircle, XCircle, HelpCircle } from 'lucide-react';

const RumorCard = ({ rumor, onVote }) => {
    const getStatusIcon = (status) => {
        if (status === 'CONFIRMED') return <CheckCircle size={16} className="text-emerald-500" />;
        if (status === 'DEBUNKED') return <XCircle size={16} className="text-red-500" />;
        return <HelpCircle size={16} className="text-amber-500" />;
    };

    const getStatusColor = (status) => {
        if (status === 'CONFIRMED') return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
        if (status === 'DEBUNKED') return 'text-red-400 border-red-500/30 bg-red-500/10';
        return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 hover:border-slate-700 transition-all">
            <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${getStatusColor(rumor.status)} flex items-center gap-1`}>
                        {getStatusIcon(rumor.status)}
                        {rumor.status}
                    </span>
                    <span className="text-xs text-slate-500 font-mono">
                        {new Date(rumor.created_at).toLocaleDateString()}
                    </span>
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    {rumor.type}
                </div>
            </div>

            <h3 className="text-lg font-bold text-slate-200 mb-2">{rumor.title}</h3>
            <p className="text-slate-400 text-sm mb-4 leading-relaxed">{rumor.description}</p>

            <div className="flex justify-between items-center border-t border-slate-800 pt-4">
                <div className="flex items-center gap-2">
                     <span className="text-xs font-bold bg-slate-800 px-2 py-1 rounded text-cyan-400">
                        ${rumor.ticker}
                    </span>
                    <span className="text-xs text-slate-500">
                        Source: {rumor.source}
                    </span>
                </div>

                <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-slate-400 mr-2">
                        Confidence: <span className={rumor.confidence > 0.7 ? 'text-emerald-400' : 'text-slate-200'}>{Math.round(rumor.confidence * 100)}%</span>
                    </span>
                    
                    <button 
                        onClick={() => onVote(rumor.id, 'up')}
                        className="flex items-center gap-1 text-slate-500 hover:text-emerald-400 transition-colors"
                    >
                        <ThumbsUp size={16} />
                        <span className="text-xs">{rumor.upvotes}</span>
                    </button>
                    
                    <button 
                        onClick={() => onVote(rumor.id, 'down')}
                        className="flex items-center gap-1 text-slate-500 hover:text-red-400 transition-colors"
                    >
                        <ThumbsDown size={16} />
                        <span className="text-xs">{rumor.downvotes}</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default RumorCard;
