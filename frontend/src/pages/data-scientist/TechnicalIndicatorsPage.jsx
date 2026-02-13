import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Binary, Calculator, Search, Activity, ChevronRight, Zap, Target, Gauge, RefreshCcw } from "lucide-react";
import { toast } from "@/components/ui/use-toast";
import { motion } from "framer-motion";
import apiClient from '@/services/apiClient';

// Sub-components
import ParameterTuner from '@/components/forms/ParameterTuner';

const TechnicalIndicatorsPage = () => {
    const [indicators, setIndicators] = useState([]);
    const [selectedIndicator, setSelectedIndicator] = useState(null);
    const [calcResult, setCalcResult] = useState(null);
    const [loading, setLoading] = useState(true);
    const [calcLoading, setCalcLoading] = useState(false);
    const [ticker, setTicker] = useState('AAPL');

    const fetchIndicators = useCallback(async () => {
        setLoading(true);
        try {
            const response = await apiClient.get('/indicators');
            const data = response.data || [];
            setIndicators(data);
            if (data.length > 0) setSelectedIndicator(data[0]);
        } catch (error) {
            console.error("Failed to fetch indicators", error);
            toast({ 
                title: "Quant Lib Fault", 
                description: "Failed to load technical indicator library.",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchIndicators();
    }, [fetchIndicators]);

    const handleCalculate = async (indicatorId, params) => {
        setCalcLoading(true);
        setCalcResult(null);
        try {
            const response = await apiClient.post(`/indicators/calculate`, {
                ticker: ticker.toUpperCase(),
                indicator: indicatorId,
                period: "1y",
                params: params
            });
            setCalcResult(response.data);
            toast({ 
                title: "Calculation Success", 
                description: `Computed ${indicatorId} for ${ticker.toUpperCase()}`,
                variant: "success"
            });
        } catch (error) {
            console.error("Calculation failed", error);
            toast({ 
                title: "Compute Error", 
                description: "The quantification engine encountered a numerical instability.",
                variant: "destructive"
            });
        } finally {
            setCalcLoading(false);
        }
    };

    return (
        <div className="p-8 space-y-8 max-w-[1700px] mx-auto text-slate-200">
            {/* Command Header */}
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 border-b border-slate-800 pb-8">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-indigo-500/10 rounded-lg border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.1)]">
                            <Binary className="h-6 w-6 text-indigo-500" />
                        </div>
                        <h1 className="text-4xl font-black tracking-tighter text-white uppercase">
                            Quant <span className="text-indigo-500">Analytics</span>
                        </h1>
                    </div>
                    <p className="text-slate-500 font-mono text-xs uppercase tracking-[0.3em]">
                        Technical Study Library & Numerical Backtest Engine // v4.0.1_STABLE
                    </p>
                </div>

                <div className="flex items-center gap-3 bg-slate-950 p-1.5 rounded-xl border border-slate-800 shadow-xl">
                    <div className="flex items-center gap-2 px-3 border-r border-slate-800">
                        <Search className="h-4 w-4 text-slate-500" />
                        <Input 
                            value={ticker}
                            onChange={(e) => setTicker(e.target.value.toUpperCase())}
                            className="w-24 bg-transparent border-none font-black font-mono text-white focus-visible:ring-0 uppercase h-8"
                            placeholder="TICKER"
                        />
                    </div>
                    <div className="flex items-center gap-4 px-3 py-1 font-mono text-[10px] text-slate-500 uppercase">
                        <div className="flex items-center gap-1.5">
                            <Activity className="h-3 w-3 text-green-500" />
                            Engine_Ready
                        </div>
                        <div className="flex items-center gap-1.5 text-slate-600">
                            RAM: 1.2GB Free
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
                {/* Left: Indicator Browser */}
                <div className="xl:col-span-1 space-y-4">
                    <div className="flex items-center gap-2 px-2 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">
                        <Target className="h-3 w-3" />
                        Indicator_Manifest
                    </div>
                    <div className="space-y-2 max-h-[700px] overflow-y-auto pr-2 custom-scrollbar">
                        {loading ? (
                            Array(8).fill(0).map((_, i) => (
                                <div key={i} className="h-16 bg-slate-900/50 rounded-lg animate-pulse border border-slate-800/50" />
                            ))
                        ) : (
                            indicators.map((ind) => (
                                <motion.div
                                    key={ind.id}
                                    whileHover={{ x: 4 }}
                                    onClick={() => setSelectedIndicator(ind)}
                                    className={`p-4 rounded-lg border cursor-pointer transition-all flex items-center justify-between group ${
                                        selectedIndicator?.id === ind.id 
                                        ? 'bg-indigo-500/10 border-indigo-500/50 shadow-[0_0_20px_rgba(99,102,241,0.05)]' 
                                        : 'bg-slate-950/40 border-slate-800 hover:border-slate-700'
                                    }`}
                                >
                                    <div className="flex flex-col gap-1">
                                        <span className={`text-xs font-black uppercase tracking-wider ${selectedIndicator?.id === ind.id ? 'text-indigo-400' : 'text-slate-400 group-hover:text-slate-200'}`}>
                                            {ind.name}
                                        </span>
                                        <div className="flex gap-2">
                                            <span className="inline-flex items-center rounded-full border border-slate-800 bg-slate-900 px-2 py-0.5 text-[8px] font-mono text-slate-600">
                                                {ind.category}
                                            </span>
                                        </div>
                                    </div>
                                    <ChevronRight className={`h-4 w-4 transition-transform ${selectedIndicator?.id === ind.id ? 'text-indigo-500 translate-x-1' : 'text-slate-700 group-hover:text-slate-400'}`} />
                                </motion.div>
                            ))
                        )}
                    </div>
                </div>

                {/* Center: Parameter Tuning */}
                <div className="xl:col-span-1">
                    <ParameterTuner indicator={selectedIndicator} onCalculate={handleCalculate} calcLoading={calcLoading} />
                    
                    <div className="mt-8 p-6 rounded-xl border border-slate-800 bg-slate-950/20 space-y-4">
                        <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2">
                            <Gauge className="h-4 w-4" /> Usage_Analytics
                        </div>
                        <div className="space-y-4">
                            <div className="flex justify-between items-end">
                                <span className="text-[10px] font-mono text-slate-600">Total Queries</span>
                                <span className="font-mono text-slate-300">1,248</span>
                            </div>
                            <div className="w-full bg-slate-900 h-1 rounded-full overflow-hidden">
                                <div className="bg-indigo-500 h-full w-[65%]" />
                            </div>
                            <div className="flex justify-between items-end">
                                <span className="text-[10px] font-mono text-slate-600">Computation Time</span>
                                <span className="font-mono text-slate-300">avg 12.4ms</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right: Results / Output */}
                <div className="xl:col-span-2 space-y-6">
                    <Card className="bg-slate-950/60 border-slate-800 backdrop-blur-xl h-full flex flex-col min-h-[500px] shadow-2xl">
                        <CardHeader className="p-6 border-b border-slate-900 bg-slate-900/20">
                            <div className="flex items-center justify-between">
                                <div>
                                    <CardTitle className="text-lg font-black text-white flex items-center gap-2">
                                        <Calculator className="h-5 w-5 text-indigo-400" />
                                        ANALYSIS_OUTPUT_STREAM
维持                                    </CardTitle>
                                    <CardDescription className="text-xs font-mono uppercase tracking-widest text-slate-500">
                                        Real-time quantitative signal projection and buffer.
                                    </CardDescription>
                                </div>
                                {calcLoading && <div className="p-2 rounded-full border border-indigo-500/20 bg-indigo-500/10"><RefreshCcw className="h-4 w-4 text-indigo-500 animate-spin" /></div>}
                            </div>
                        </CardHeader>
                        <CardContent className="p-6 overflow-auto">
                            {calcResult ? (
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between mb-4">
                                        <h4 className="text-xs font-black text-slate-400 uppercase tracking-widest">Calculated_Signals</h4>
                                    </div>
                                    <div className="rounded-lg border border-slate-900 overflow-hidden">
                                        <Table>
                                            <TableHeader>
                                                <TableRow className="bg-slate-900/50 hover:bg-slate-900/50 border-slate-800">
                                                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase">Timestamp</TableHead>
                                                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase">Value</TableHead>
                                                </TableRow>
                                            </TableHeader>
                                            <TableBody>
                                                {calcResult.values?.slice(0, 10).map((v, idx) => (
                                                    <TableRow key={idx} className="border-slate-900 hover:bg-slate-900/30">
                                                        <TableCell className="text-slate-400 font-mono text-[11px] truncate">{v.timestamp?.split('T')[0] || v.timestamp}</TableCell>
                                                        <TableCell className="font-mono text-indigo-400">{v.value?.toFixed(4) || v.value}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    </div>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center justify-center h-[300px] text-slate-700 space-y-4">
                                    <Calculator className="h-12 w-12 opacity-20" />
                                    <div className="text-center">
                                        <p className="text-xs font-black uppercase tracking-widest opacity-40">Stream_Idle</p>
                                        <p className="text-[10px] font-mono opacity-30 mt-1">EXECUTE_INDICATOR_TO_BEGIN_ANALYSIS</p>
                                    </div>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default TechnicalIndicatorsPage;
