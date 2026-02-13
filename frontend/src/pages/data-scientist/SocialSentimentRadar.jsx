import React, { useState, useEffect } from 'react';
import { socialService } from '../../services/socialService';
import SentimentGauge from '../../components/charts/SentimentGauge';
import TrendDetectionWidget from '../../components/widgets/TrendDetectionWidget';
import { toast } from 'sonner';
import { Radar, MessageCircle, TrendingUp, Share2, BarChart2 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const SocialSentimentRadar = () => {
    const [ticker, setTicker] = useState('TSLA');
    const [sentimentData, setSentimentData] = useState(null);
    const [history, setHistory] = useState([]);
    const [topMovers, setTopMovers] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadTickerData = async (symbol) => {
        try {
            setLoading(true);
            const [sent, hist, corr] = await Promise.all([
                socialService.getTickerSentiment(symbol),
                socialService.getSentimentHistory(symbol),
                // socialService.getCorrelation(symbol) // Optional for MVP
            ]);
            setSentimentData(sent);
            setHistory(hist);
        } catch (e) {
            toast.error("Failed to load sentiment data");
        } finally {
            setLoading(false);
        }
    };

    const loadTopMovers = async () => {
        const movers = await socialService.getTopSentiment();
        setTopMovers(movers);
    };

    useEffect(() => {
        loadTopMovers();
        loadTickerData(ticker);
    }, []);

    const handleTickerChange = (e) => {
        if (e.key === 'Enter') {
            setTicker(e.target.value.toUpperCase());
            loadTickerData(e.target.value.toUpperCase());
        }
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200 overflow-y-auto">
            {/* Header */}
             <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Radar className="text-indigo-500" /> Social Sentiment Radar
                    </h1>
                    <p className="text-slate-400 mt-2">Real-time sentiment analysis across social platforms.</p>
                </div>
                 <div className="relative">
                    <input 
                        type="text" 
                        defaultValue={ticker}
                        onKeyDown={handleTickerChange}
                        className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white font-mono focus:border-indigo-500 outline-none w-32 text-center uppercase"
                        placeholder="SYMBOL"
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                {/* Main Gauge Card */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center lg:col-span-1">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4">{ticker} AGGREGATE SENTIMENT</h3>
                    {loading ? <div className="animate-pulse h-32 w-32 bg-slate-800 rounded-full"></div> : 
                        <SentimentGauge score={sentimentData?.overall_score || 0} />
                    }
                    <div className="mt-4 flex gap-4 text-sm text-slate-400">
                        <span className="flex items-center gap-1"><MessageCircle size={14} /> {sentimentData?.volume?.toLocaleString()} Mentions</span>
                        <span className="flex items-center gap-1"><Share2 size={14} /> High Virality</span>
                    </div>
                </div>

                {/* Platform Breakdown */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 lg:col-span-1">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4">Platform Breakdown</h3>
                    {!loading && sentimentData?.platforms && Object.entries(sentimentData.platforms).map(([platform, data]) => (
                        <div key={platform} className="mb-4 last:mb-0">
                            <div className="flex justify-between text-sm mb-1">
                                <span className="capitalize text-slate-300">{platform}</span>
                                <span className={data.score > 0 ? 'text-emerald-400' : 'text-red-400'}>{data.score > 0 ? '+' : ''}{data.score}</span>
                            </div>
                            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                <div 
                                    className={`h-full ${data.score > 0 ? 'bg-emerald-500' : 'bg-red-500'}`} 
                                    style={{width: `${Math.abs(data.score)}%`}}
                                ></div>
                            </div>
                        </div>
                    ))}
                </div>

                 {/* Top Movers List */}
                 <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 lg:col-span-1">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4">Top Sentiment Movers</h3>
                    <div className="space-y-3">
                        {topMovers.map(m => (
                            <div key={m.ticker} 
                                 onClick={() => { setTicker(m.ticker); loadTickerData(m.ticker); }}
                                 className="flex justify-between items-center p-2 hover:bg-slate-800 rounded cursor-pointer group"
                            >
                                <span className="font-mono font-bold text-white group-hover:text-indigo-400 transition-colors">{m.ticker}</span>
                                <div className="flex items-center gap-3">
                                    <span className={`text-sm ${m.overall_score > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                        {m.overall_score > 0 ? '+' : ''}{m.overall_score}
                                    </span>
                                    <BarChart2 size={14} className="text-slate-600" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Time Series Chart */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex-1 min-h-[300px]">
                <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4">Sentiment vs Price Correlation (7 Days)</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={history}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="timestamp" tick={false} stroke="#475569" />
                        <YAxis yAxisId="left" stroke="#10b981" />
                        <YAxis yAxisId="right" orientation="right" stroke="#6366f1" />
                        <Tooltip 
                            contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b'}} 
                            itemStyle={{color: '#cbd5e1'}}
                        />
                        <Line yAxisId="left" type="monotone" dataKey="score" stroke="#10b981" dot={false} strokeWidth={2} name="Sentiment" />
                        <Line yAxisId="right" type="monotone" dataKey="price_chg" stroke="#6366f1" dot={false} strokeWidth={2} name="Price Impact" />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* Trends Section */}
            <div className="mt-6 h-96">
                 <TrendDetectionWidget />
            </div>
        </div>
    );
};

export default SocialSentimentRadar;
