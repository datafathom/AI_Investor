import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Volume2, Megaphone, AlertCircle, TrendingUp, Info } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import apiClient from '@/services/apiClient';

const VolumePromoWidget = () => {
    const [spikes, setSpikes] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchSpikes = useCallback(async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const response = await apiClient.get('/market-data/promotions');
            // Filter only high risk for the widget
            const riskSpikes = (response.data || []).filter(s => s.risk_score > 60);
            setSpikes(riskSpikes);
        } catch (error) {
            console.error("Failed to fetch promo spikes", error);
        } finally {
            if (!silent) setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchSpikes();
        const interval = setInterval(() => fetchSpikes(true), 45000);
        return () => clearInterval(interval);
    }, [fetchSpikes]);

    return (
        <Card className="bg-slate-950/60 border-slate-800 backdrop-blur-xl overflow-hidden shadow-2xl">
            <CardHeader className="p-4 border-b border-white/5 bg-gradient-to-r from-orange-500/10 to-transparent">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Megaphone className="h-4 w-4 text-orange-500" />
                        <CardTitle className="text-xs font-black uppercase tracking-[0.2em] text-white">Promo_Detector</CardTitle>
                    </div>
                    <div className="flex items-center gap-1.5 font-mono text-[10px] text-slate-500">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                        LIVE_SCAN
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-2">
                <AnimatePresence mode="popLayout">
                    {spikes.length > 0 ? (
                        <div className="space-y-2">
                            {spikes.slice(0, 5).map((spike) => (
                                <motion.div
                                    key={spike.ticker}
                                    layout
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    className={`p-3 rounded-lg border flex flex-col gap-2 transition-all ${
                                        spike.risk_score > 85 ? 'bg-red-500/10 border-red-500/30' : 'bg-slate-900/50 border-slate-800'
                                    }`}
                                >
                                    <div className="flex justify-between items-center">
                                        <div className="flex items-center gap-2">
                                            <span className="text-sm font-black font-mono text-white">{spike.ticker}</span>
                                            <Badge variant="outline" className={`text-[8px] h-4 px-1 ${
                                                spike.severity === 'CRITICAL' ? 'text-red-400 border-red-900' : 'text-orange-400 border-orange-900'
                                            }`}>
                                                {spike.severity}
                                            </Badge>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-[10px] font-black text-white font-mono">{spike.risk_score}</div>
                                            <div className="text-[7px] text-slate-500 uppercase tracking-widest font-mono">Risk Index</div>
                                        </div>
                                    </div>
                                    
                                    <div className="grid grid-cols-2 gap-2 text-[9px] font-mono">
                                        <div className="flex flex-col">
                                            <span className="text-slate-500 uppercase">Vol_Delta</span>
                                            <span className="text-white flex items-center gap-1">
                                                <TrendingUp className="h-2 w-2 text-green-500" />
                                                {spike.volume_ratio}x
                                            </span>
                                        </div>
                                        <div className="flex flex-col items-end">
                                            <span className="text-slate-500 uppercase">Soc_Intense</span>
                                            <span className="text-white">{(spike.social_intensity * 100).toFixed(0)}%</span>
                                        </div>
                                    </div>

                                    {spike.risk_score > 75 && (
                                        <div className="flex items-center gap-1.5 text-[8px] text-red-400 uppercase font-black tracking-widest mt-1">
                                            <AlertCircle className="h-2 w-2" />
                                            Wash_Trading_Signal_Detected
                                        </div>
                                    )}
                                </motion.div>
                            ))}
                        </div>
                    ) : (
                        <div className="py-12 text-center">
                            <Volume2 className="h-8 w-8 text-slate-800 mx-auto mb-2 opacity-20" />
                            <p className="text-[10px] font-mono text-slate-600 uppercase tracking-widest">No structural promo spikes in range.</p>
                        </div>
                    )}
                </AnimatePresence>
            </CardContent>
            <div className="p-2 border-t border-white/5 bg-black/20 flex justify-between items-center">
                <span className="text-[8px] font-mono text-slate-600 uppercase tracking-wider">SEC_Auditor_Lvl_2: ENABLED</span>
                <Info className="h-3 w-3 text-slate-700 cursor-help" />
            </div>
        </Card>
    );
};

export default VolumePromoWidget;
