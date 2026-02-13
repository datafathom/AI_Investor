import React, { useState, useEffect, useRef } from 'react';
import { newsService } from '../../services/newsService';
import NewsCard from '../../components/cards/NewsCard';
import { toast } from 'sonner';
import { Search, Filter, RefreshCw, Radio, Settings, Globe } from 'lucide-react';

const NewsAggregator = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [sources, setSources] = useState([]);
    const [filters, setFilters] = useState({ ticker: '', source: '', tag: '' });
    const [liveMode, setLiveMode] = useState(false);
    const wsRef = useRef(null);

    const loadData = async () => {
        try {
            setLoading(true);
            const [artRes, srcRes] = await Promise.all([
                newsService.getArticles(filters),
                newsService.getSources()
            ]);
            setArticles(artRes.articles || []);
            setSources(srcRes || []);
        } catch (e) {
            console.error(e);
            toast.error("Failed to load news");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, [filters]); // Reload when filters change

    // WebSocket logic for Live Mode
    useEffect(() => {
        if (liveMode) {
            const url = newsService.getStreamUrl();
            wsRef.current = new WebSocket(url);
            
            wsRef.current.onopen = () => toast.success("Connected to Live News Wire");
            wsRef.current.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                if (msg.type === 'news') {
                    setArticles(prev => [msg.data, ...prev].slice(0, 50));
                }
            };
            wsRef.current.onclose = () => toast("Live connection closed");

            return () => {
                if (wsRef.current) wsRef.current.close();
            };
        }
    }, [liveMode]);

    const handleFilterChange = (key, value) => {
        setFilters(prev => ({ ...prev, [key]: value }));
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Globe className="text-cyan-500" /> News Aggregator
                    </h1>
                    <p className="text-slate-400 mt-2">Global financial news wire, aggregated and analyzed.</p>
                </div>
                <div className="flex items-center gap-3">
                    <button 
                        onClick={() => setLiveMode(!liveMode)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium border transition-all ${
                            liveMode 
                            ? 'bg-red-500/10 text-red-500 border-red-500/30 animate-pulse' 
                            : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
                        }`}
                    >
                        <Radio size={16} /> {liveMode ? 'LIVE WIRE' : 'Go Live'}
                    </button>
                    <button 
                        onClick={loadData}
                        className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 text-slate-400 hover:text-white transition-colors"
                    >
                        <RefreshCw size={20} className={loading && !liveMode ? "animate-spin" : ""} />
                    </button>
                </div>
            </div>

            {/* Filters */}
            <div className="flex gap-4 mb-6 p-4 bg-slate-900 border border-slate-800 rounded-lg overflow-x-auto">
                <div className="flex items-center gap-2 text-slate-500 border-r border-slate-800 pr-4">
                    <Filter size={18} />
                    <span className="text-sm font-medium">Filters</span>
                </div>
                
                <input 
                    type="text" 
                    placeholder="Ticker (e.g. AAPL)" 
                    className="bg-slate-950 border border-slate-800 rounded px-3 py-1 text-sm focus:border-cyan-500 outline-none w-32"
                    value={filters.ticker}
                    onChange={(e) => handleFilterChange('ticker', e.target.value)}
                />

                <select 
                    className="bg-slate-950 border border-slate-800 rounded px-3 py-1 text-sm focus:border-cyan-500 outline-none"
                    value={filters.source}
                    onChange={(e) => handleFilterChange('source', e.target.value)}
                >
                    <option value="">All Sources</option>
                    {sources.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>

                <select 
                    className="bg-slate-950 border border-slate-800 rounded px-3 py-1 text-sm focus:border-cyan-500 outline-none"
                    value={filters.tag}
                    onChange={(e) => handleFilterChange('tag', e.target.value)}
                >
                    <option value="">All Tags</option>
                    <option value="Earnings">Earnings</option>
                    <option value="M&A">M&A</option>
                    <option value="Macro">Macro</option>
                    <option value="Regulatory">Regulatory</option>
                </select>
            </div>

            {/* Feed */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 overflow-y-auto flex-1 pb-4">
                {articles.map(article => (
                    <NewsCard 
                        key={article.id} 
                        article={article} 
                        onClick={(a) => toast.info(`Opening ${a.title}`)} 
                    />
                ))}
                
                {articles.length === 0 && !loading && (
                    <div className="col-span-full py-12 text-center text-slate-500">
                        No articles found matching filters.
                    </div>
                )}
            </div>
        </div>
    );
};

export default NewsAggregator;
