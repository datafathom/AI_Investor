import React, { useState, useEffect } from 'react';
import { socialTradingService } from '../../services/socialTradingService';
import InfluencerCard from '../../components/cards/InfluencerCard';
import { toast } from 'sonner';
import { Users, Filter, ArrowUpRight, ArrowDownRight, MessageSquare } from 'lucide-react';

const SocialTradingFeed = () => {
    const [feed, setFeed] = useState([]);
    const [influencers, setInfluencers] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        try {
            setLoading(true);
            const [feedRes, infRes] = await Promise.all([
                socialTradingService.getFeed(),
                socialTradingService.getInfluencers()
            ]);
            setFeed(feedRes);
            setInfluencers(infRes);
        } catch (e) {
            toast.error("Failed to load social feed");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const handleFollow = async (id) => {
        try {
            await socialTradingService.toggleFollow(id);
            // Refresh influencers to update UI
            const infRes = await socialTradingService.getInfluencers();
            setInfluencers(infRes);
            toast.success("Updated following status");
        } catch (e) {
            toast.error("Failed to update follow status");
        }
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200 overflow-y-auto">
             <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Users className="text-violet-500" /> Social Trading Feed
                    </h1>
                    <p className="text-slate-400 mt-2">Follow top performing traders and copy their signals.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left: Feed */}
                <div className="lg:col-span-2 space-y-4">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-2">Live Signals</h3>
                    {feed.map(post => (
                        <div key={post.id} className="bg-slate-900 border border-slate-800 rounded-lg p-5 hover:bg-slate-800/50 transition-colors">
                            <div className="flex justify-between items-start mb-3">
                                <div className="flex items-center gap-3">
                                    <div className="text-xl">{post.influencer_avatar}</div>
                                    <div>
                                        <div className="font-bold text-white text-sm">{post.influencer_name}</div>
                                        <div className="text-xs text-slate-500">{new Date(post.timestamp).toLocaleTimeString()}</div>
                                    </div>
                                </div>
                                <div className={`px-2 py-1 rounded text-xs font-bold flex items-center gap-1 ${
                                    post.action === 'BUY' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 
                                    post.action === 'SELL' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 
                                    'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                                }`}>
                                    {post.action === 'BUY' ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                                    {post.action} {post.ticker}
                                </div>
                            </div>
                            
                            <p className="text-slate-300 text-sm mb-3">{post.comment}</p>
                            
                            <div className="flex items-center gap-4 text-xs text-slate-500">
                                <span className="flex items-center gap-1">Price: <span className="text-slate-300 font-mono">${post.price}</span></span>
                                <span className="flex items-center gap-1">Confidence: <span className="text-violet-400">{post.confidence}%</span></span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Right: Influencers */}
                <div className="lg:col-span-1 space-y-4">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-2">Top Traders</h3>
                    {influencers.map(inf => (
                        <InfluencerCard key={inf.id} influencer={inf} onToggleFollow={handleFollow} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SocialTradingFeed;
