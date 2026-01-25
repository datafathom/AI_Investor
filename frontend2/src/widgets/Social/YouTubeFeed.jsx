import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
    Loader2, 
    Youtube, 
    Zap, 
    FileText, 
    ExternalLink, 
    TrendingUp, 
    Clock 
} from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const YouTubeFeed = () => {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [analyzingId, setAnalyzingId] = useState(null);
    const { toast } = useToast();

    useEffect(() => {
        fetchVideos();
    }, []);

    const fetchVideos = async () => {
        setLoading(true);
        // Simulate YouTube API
        setTimeout(() => {
            setVideos([
                { 
                    id: 'v1', 
                    title: 'Institutional Macro: The 2026 Liquidity Cycle', 
                    channel: 'RealVision', 
                    time: '2h ago',
                    thumbnail: 'https://i.ytimg.com/vi/mock1/hqdefault.jpg',
                    sentiment: 'Bullish',
                    score: 0.85
                },
                { 
                    id: 'v2', 
                    title: 'Why the Fed is Trapped (Strategic Update)', 
                    channel: 'MacroVoices', 
                    time: '5h ago',
                    thumbnail: 'https://i.ytimg.com/vi/mock2/hqdefault.jpg',
                    sentiment: 'Neutral',
                    score: 0.42
                },
                { 
                    id: 'v3', 
                    title: 'Credit Markets Breakdown: What to Watch', 
                    channel: 'Bloomberg', 
                    time: '8h ago',
                    thumbnail: 'https://i.ytimg.com/vi/mock3/hqdefault.jpg',
                    sentiment: 'Bearish',
                    score: 0.15
                }
            ]);
            setLoading(false);
        }, 1200);
    };

    const runAnalysis = (id) => {
        setAnalyzingId(id);
        // Simulate Transcript Analysis
        setTimeout(() => {
            setAnalyzingId(null);
            toast({
                title: "Transcript Analysis Complete",
                description: "Summary: Analyst projects BTC outperformance relative to equities.",
                variant: "default"
            });
        }, 2000);
    };

    return (
        <Card className="w-full h-full bg-slate-950 border-slate-800 text-slate-100 flex flex-col font-sans overflow-hidden">
            <CardHeader className="pb-4 border-b border-slate-800 bg-slate-900/40">
                <div className="flex justify-between items-center">
                    <div>
                        <CardTitle className="text-xl font-bold flex items-center gap-2">
                             <Youtube className="h-6 w-6 text-red-600" />
                             Macro Intelligence
                        </CardTitle>
                        <CardDescription className="text-[10px] uppercase font-semibold tracking-wider text-slate-500">Video Signal Extraction</CardDescription>
                    </div>
                    <Badge variant="outline" className="border-red-900/50 text-red-500 bg-red-900/10 h-5 px-1.5 text-[9px]">YT_API_V3</Badge>
                </div>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto pt-6 space-y-6 custom-scrollbar pr-2">
                {loading ? (
                    <div className="flex flex-col items-center justify-center py-20 space-y-4">
                        <Loader2 className="h-8 w-8 text-red-600 animate-spin" />
                        <p className="text-sm text-slate-500 italic">Scanning institutional channels...</p>
                    </div>
                ) : (
                    videos.map((v) => (
                        <div key={v.id} className="group bg-slate-900/30 border border-slate-800 rounded-xl overflow-hidden hover:border-slate-700 transition-all">
                            <div className="aspect-video bg-slate-800 relative">
                                <img src={v.thumbnail} alt={v.title} className="w-full h-full object-cover opacity-50 grayscale group-hover:grayscale-0 group-hover:opacity-80 transition-all" />
                                <div className="absolute top-2 right-2">
                                     <Badge className={`${v.sentiment === 'Bullish' ? 'bg-green-600' : v.sentiment === 'Bearish' ? 'bg-red-600' : 'bg-slate-700'} text-[10px]`}>
                                         {v.sentiment.toUpperCase()}
                                     </Badge>
                                </div>
                                <div className="absolute bottom-2 left-2 flex items-center gap-1.5 text-[10px] text-slate-100 bg-black/60 px-2 py-0.5 rounded backdrop-blur-sm font-mono">
                                    <Clock className="h-3 w-3" />
                                    {v.time}
                                </div>
                            </div>
                            <div className="p-4 space-y-3">
                                <div>
                                    <div className="text-[10px] text-red-500 font-bold uppercase tracking-tight mb-1">{v.channel}</div>
                                    <h4 className="text-sm font-bold leading-tight group-hover:text-red-400 transition-colors">{v.title}</h4>
                                </div>
                                
                                <div className="flex gap-2">
                                    <Button 
                                        variant="outline" 
                                        size="sm" 
                                        className="flex-1 h-8 text-[10px] gap-2 border-slate-700 hover:bg-slate-800"
                                        onClick={() => runAnalysis(v.id)}
                                        disabled={analyzingId === v.id}
                                    >
                                        {analyzingId === v.id ? <Loader2 className="h-3 w-3 animate-spin" /> : <Zap className="h-3 w-3 text-yellow-500" />}
                                        SUMMARIZE TRANSCRIPT
                                    </Button>
                                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-500 hover:text-white">
                                        <ExternalLink className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </CardContent>
            <div className="p-4 bg-slate-900/50 border-t border-slate-800">
                <div className="flex items-center justify-between text-[10px]">
                    <span className="text-slate-500 font-bold uppercase">Daily Insight Quota</span>
                    <span className="text-slate-300 font-mono">14 / 50</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                    <div className="bg-red-600 h-full w-[28%] shadow-[0_0_8px_rgba(220,38,38,0.5)]"></div>
                </div>
            </div>
        </Card>
    );
};

export default YouTubeFeed;
