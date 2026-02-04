import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, MessageSquare, TrendingUp, TrendingDown, RefreshCcw, Search } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const StockTwitsFeed = () => {
    const [messages, setMessages] = useState([]);
    const [symbol, setSymbol] = useState('BTC.X');
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState(null);
    const { toast } = useToast();

    useEffect(() => {
        fetchFeed();
    }, [symbol]);

    const fetchFeed = async () => {
        setLoading(true);
        // Simulate StockTwits API
        setTimeout(() => {
            setMessages([
                { id: 1, user: 'CryptoKing', body: 'Accumulating $BTC here. Looks strong for the weekly close!', sentiment: 'Bullish', time: '2m' },
                { id: 2, user: 'BearishBob', body: 'The macro outlook is terrible. $BTC going to 30k soon.', sentiment: 'Bearish', time: '5m' },
                { id: 3, user: 'AlphaSeeker', body: 'Just look at the $NVDA chart. Unstoppable momentum.', sentiment: 'Bullish', time: '12m' },
                { id: 4, user: 'MarketMaverick', body: 'Scaling out of $TSLA. RSI is overbought.', sentiment: 'Bearish', time: '15m' },
                { id: 5, user: 'HODL_PRO', body: 'Diamond hands only. $BTC 100k incoming.', sentiment: 'Bullish', time: '20m' }
            ]);
            setStats({
                bullishRatio: '68%',
                bearishRatio: '32%',
                volumeStatus: 'HIGH'
            });
            setLoading(false);
        }, 1000);
    };

    const getSentimentBadge = (sentiment) => {
        if (sentiment === 'Bullish') return <Badge className="bg-green-600 text-[9px] h-4">BULLISH</Badge>;
        if (sentiment === 'Bearish') return <Badge className="bg-red-600 text-[9px] h-4">BEARISH</Badge>;
        return <Badge variant="outline" className="text-[9px] h-4 text-slate-500">NEUTRAL</Badge>;
    };

    return (
        <Card className="w-full h-full bg-slate-950 border-slate-800 text-slate-100 flex flex-col font-sans">
            <CardHeader className="pb-4 border-b border-slate-800 bg-slate-900/30">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="text-lg font-bold flex items-center gap-2">
                            <MessageSquare className="h-4 w-4 text-blue-400" />
                            StockTwits Pulse
                        </CardTitle>
                        <CardDescription className="text-[10px] text-slate-500 font-bold uppercase tracking-tight">Real-time Retail Sentiment</CardDescription>
                    </div>
                    <div className="flex gap-2">
                        <div className="flex items-center gap-1 bg-slate-900 px-2 py-1 rounded border border-slate-800">
                             <TrendingUp className="h-3 w-3 text-green-500" />
                             <span className="text-[10px] font-mono font-bold text-green-500">{stats?.bullishRatio}</span>
                        </div>
                        <Button variant="ghost" size="icon" className="h-7 w-7 text-slate-400" onClick={fetchFeed}>
                             <RefreshCcw className={`h-3 w-3 ${loading ? 'animate-spin' : ''}`} />
                        </Button>
                    </div>
                </div>
                <div className="flex gap-2 mt-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-2 top-2 h-3 w-3 text-slate-500" />
                        <Input 
                            value={symbol}
                            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                            className="h-7 bg-slate-900 border-slate-800 pl-7 text-[10px] uppercase font-mono"
                            placeholder="SEARCH TICKER..."
                        />
                    </div>
                </div>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto pt-4 space-y-4 no-scrollbar">
                {loading ? (
                    <div className="flex flex-col items-center justify-center py-12 space-y-2">
                        <Loader2 className="h-6 w-6 text-blue-500 animate-spin" />
                        <p className="text-[10px] text-slate-500 uppercase font-bold">Streaming community feed...</p>
                    </div>
                ) : (
                    messages.map((m) => (
                        <div key={m.id} className="bg-slate-900/40 border-l-2 border-slate-800 p-3 space-y-2 hover:bg-slate-900/60 transition-colors">
                            <div className="flex justify-between items-center text-[10px]">
                                <span className="font-bold text-blue-400">@{m.user}</span>
                                <div className="flex items-center gap-2">
                                    {getSentimentBadge(m.sentiment)}
                                    <span className="text-slate-600">{m.time}</span>
                                </div>
                            </div>
                            <p className="text-xs text-slate-300 leading-relaxed font-medium">
                                {m.body}
                            </p>
                        </div>
                    ))
                )}
            </CardContent>
            <div className="p-3 border-t border-slate-800 bg-slate-900/20">
                 <Button className="w-full h-8 text-[10px] font-bold bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-400">
                     LOAD MORE CONVERSATIONS
                 </Button>
            </div>
        </Card>
    );
};

export default StockTwitsFeed;
