import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Globe, TrendingUp, TrendingDown, RefreshCcw, Info, ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import apiClient from '@/services/apiClient';

const MarketRegimeWidget = () => {
    const [regimeData, setRegimeData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchRegime = useCallback(async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const response = await apiClient.get('/market/regime');
            setRegimeData(response.data);
        } catch (error) {
            console.error("Failed to fetch regime", error);
        } finally {
            if (!silent) setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchRegime();
        const interval = setInterval(() => fetchRegime(true), 60000);
        return () => clearInterval(interval);
    }, [fetchRegime]);

    const getRegimeColor = (regime) => {
        switch (regime) {
            case "BULL": return "text-green-400 border-green-900 bg-green-900/20 shadow-[0_0_15px_rgba(34,197,94,0.1)]";
            case "BEAR": return "text-red-400 border-red-900 bg-red-900/20 shadow-[0_0_15px_rgba(239,68,68,0.1)]";
            case "CHOPPY": return "text-yellow-400 border-yellow-900 bg-yellow-900/20 shadow-[0_0_15px_rgba(234,179,8,0.1)]";
            default: return "text-indigo-400 border-indigo-900 bg-indigo-900/20 shadow-[0_0_15px_rgba(99,102,241,0.1)]";
        }
    };

    const getIndicatorIcon = (name) => {
        if (name.includes("Volatility")) return <Activity className="h-3 w-3" />;
        if (name.includes("Trend")) return <TrendingUp className="h-3 w-3" />;
        return <Globe className="h-3 w-3" />;
    };

    return (
        <Card className="bg-slate-950/60 border-slate-800 backdrop-blur-xl overflow-hidden shadow-2xl h-full flex flex-col">
            <CardHeader className="p-4 border-b border-white/5 bg-slate-950">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Globe className="h-4 w-4 text-indigo-500" />
                        <CardTitle className="text-xs font-black uppercase tracking-[0.2em] text-white">Macro_Regime_Node</CardTitle>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-4 flex-1 flex flex-col gap-6">
                <AnimatePresence mode="wait">
                    {regimeData ? (
                        <motion.div
                            key="regime"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="space-y-6"
                        >
                            {/* Current State Label */}
                            <div className="text-center space-y-2 py-4 rounded-xl border border-slate-900 bg-slate-900/20">
                                <div className="text-[10px] uppercase font-mono text-slate-500 tracking-[0.3em]">Current_Environment</div>
                                <div className={`text-4xl font-black italic tracking-tighter ${getRegimeColor(regimeData.regime).split(' ')[0]}`}>
                                    {regimeData.regime}
                                </div>
                                <Badge variant="outline" className={`${getRegimeColor(regimeData.regime)} text-[10px] font-mono h-4 border-none bg-transparent`}>
                                    Confidence: {regimeData.confidence}%
                                </Badge>
                            </div>

                            {/* Transition Probabilities */}
                            <div className="space-y-3">
                                <div className="flex items-center justify-between text-[8px] font-black uppercase tracking-[0.2em] text-slate-500">
                                    <span>Transition_Map</span>
                                    <span>Next_Cycle_Prob</span>
                                </div>
                                <div className="grid grid-cols-1 gap-2">
                                    {Object.entries(regimeData.transition_probabilities || {}).map(([regime, prob]) => (
                                        <div key={regime} className="space-y-1">
                                            <div className="flex justify-between items-center text-[10px] font-mono">
                                                <span className="text-slate-400">{regime}</span>
                                                <span className="text-white font-bold">{prob}%</span>
                                            </div>
                                            <div className="w-full bg-slate-900 h-1 rounded-full overflow-hidden">
                                                <motion.div 
                                                    initial={{ width: 0 }}
                                                    animate={{ width: `${prob}%` }}
                                                    className={`h-full ${regime === regimeData.regime ? 'bg-indigo-500' : 'bg-slate-700'}`}
                                                />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Core Indicators */}
                            <div className="pt-4 border-t border-slate-900 grid grid-cols-2 gap-3">
                                {regimeData.indicators.slice(0, 4).map((ind, i) => (
                                    <div key={i} className="p-2 rounded border border-slate-900 bg-slate-900/10 space-y-1">
                                        <div className="text-[8px] text-slate-600 uppercase tracking-widest truncate">{ind.name}</div>
                                        <div className="flex justify-between items-center">
                                            <span className="text-[10px] font-mono text-white font-black">{ind.value}</span>
                                            <span className={`text-[8px] font-mono ${ind.signal === 'STABLE' || ind.signal === 'POSITIVE' || ind.signal === 'STRONG' ? 'text-green-500' : 'text-red-500'}`}>
                                                {ind.signal}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    ) : (
                        <div className="py-20 text-center space-y-4">
                            <RefreshCcw className="h-8 w-8 text-slate-800 mx-auto animate-spin opacity-20" />
                            <p className="text-[10px] font-mono text-slate-600 uppercase tracking-widest">Synthesizing Macro Signals...</p>
                        </div>
                    )}
                </AnimatePresence>
            </CardContent>
            <div className="p-3 bg-indigo-500/5 border-t border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-[8px] font-mono text-indigo-400">
                    <ArrowRight className="h-3 w-3" />
                    PREDICTED_SHIFT: {regimeData?.regime === 'BULL' ? 'CHOPPY' : 'BULL'}
                </div>
                <Info className="h-3 w-3 text-slate-700 cursor-help" />
            </div>
        </Card>
    );
};

export default MarketRegimeWidget;
