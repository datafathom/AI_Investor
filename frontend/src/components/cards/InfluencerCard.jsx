import React from 'react';
import { UserPlus, UserCheck, TrendingUp, Award } from 'lucide-react';

const InfluencerCard = ({ influencer, onToggleFollow }) => {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex items-center justify-between hover:border-violet-500/50 transition-colors">
            <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center text-2xl border border-slate-700">
                    {influencer.avatar}
                </div>
                <div>
                    <h4 className="font-bold text-white text-sm">{influencer.name}</h4>
                    <p className="text-xs text-slate-400">{influencer.followers.toLocaleString()} followers</p>
                </div>
            </div>
            
            <div className="flex items-center gap-6">
                <div className="text-right hidden md:block">
                    <div className="text-xs text-slate-500 uppercase font-bold">Win Rate</div>
                    <div className="text-emerald-400 font-mono">{influencer.win_rate}%</div>
                </div>
                 <button 
                    onClick={() => onToggleFollow(influencer.id)}
                    className={`p-2 rounded-full transition-all ${
                        influencer.is_following 
                        ? 'bg-violet-500 text-white hover:bg-violet-600' 
                        : 'bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700'
                    }`}
                >
                    {influencer.is_following ? <UserCheck size={18} /> : <UserPlus size={18} />}
                </button>
            </div>
        </div>
    );
};

export default InfluencerCard;
