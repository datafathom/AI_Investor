import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Anchor, TrendingUp, TrendingDown, Users, RefreshCcw, BarChart3, Radio } from "lucide-react";
import { notify } from "@/components/ui/use-toast";
import { motion } from "framer-motion";
import apiClient from '@/services/apiClient';

// Sub-components
import SectorCrowdingGauge from '@/components/charts/SectorCrowdingGauge';
import FilingDeltaTimeline from '@/components/charts/FilingDeltaTimeline';
import WhaleSellingTable from '@/components/tables/WhaleSellingTable';

const WhaleFlowTerminal = () => {
    const [summary, setSummary] = useState(null);
    const [filings, setFilings] = useState([]);
    const [crowding, setCrowding] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const [summaryRes, filingsRes, crowdingRes] = await Promise.all([
                apiClient.get('/market-data/whale-flow'),
                apiClient.get('/market-data/whale-flow/filings?limit=20'),
                apiClient.get('/market-data/whale-flow/crowding')
            ]);
            
            setSummary(summaryRes.data || null);
            setFilings(filingsRes.data || []);
            setCrowding(crowdingRes.data || []);
            
        } catch (error) {
            console.error("Failed to fetch whale flow data", error);
            notify({ 
                title: "Intelligence Link Failure", 
                body: "Failed to establish secure connection to institutional filing nodes.", 
                type: "error" 
            });
        } finally {
            if (!silent) setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => fetchData(true), 60000); // 1 min background refresh
        return () => clearInterval(interval);
    }, [fetchData]);

    return (
        <div className="p-8 space-y-8 max-w-[1600px] mx-auto text-slate-200">
            {/* Header / Command Bar */}
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 border-b border-slate-800 pb-8">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
                            <Anchor className="h-6 w-6 text-blue-500" />
                        </div>
                        <h1 className="text-4xl font-black tracking-tighter text-white uppercase italic">
                            Whale Flow <span className="text-blue-600">Terminal</span>
                        </h1>
                    </div>
                    <p className="text-slate-400 font-mono text-sm max-w-2xl uppercase tracking-wider opacity-60">
                        INSTITUTIONAL INTELLIGENCE PROTOCOL v2.1 // Monitoring 13F deltas and distribution cycles.
                    </p>
                </div>
                
                <div className="flex items-center gap-4">
                    <div className="flex flex-col items-end mr-4">
                        <div className="flex items-center gap-2 text-[10px] font-mono text-blue-400 uppercase tracking-[0.2em] mb-1">
                            <Radio className="h-3 w-3 animate-pulse" />
                            Live_Stream_Active
                        </div>
                        <div className="text-[8px] text-slate-600 font-mono">QUARTERLY_RUN_CYC: {summary?.total_filings_this_quarter || 0} SEC_NODES</div>
                    </div>
                    <Button 
                        onClick={() => fetchData()} 
                        variant="outline" 
                        disabled={loading}
                        className="bg-slate-900 border-slate-700 hover:bg-slate-800 h-11 gap-2 border-2"
                    >
                        <RefreshCcw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                        <span className="font-mono text-xs font-bold tracking-widest">RELAY_SYNC</span>
                    </Button>
                </div>
            </div>

            {/* Top Level Summary Stats */}
            {summary && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {[
                        { label: "Net Buying ($B)", value: summary.net_buying_billions, sub: "Institutional Delta", trend: summary.net_buying_billions > 0 },
                        { label: "Avg Position Δ", value: `${summary.average_position_change_pct}%`, sub: "Flow Velocity", trend: summary.average_position_change_pct > 0 },
                        { label: "Top Accumulation", value: summary.most_bought_ticker, sub: "Strong Hands", icon: <TrendingUp className="h-4 w-4 text-green-500" /> },
                        { label: "Top Distribution", value: summary.most_sold_ticker, sub: "Whale Exit", icon: <TrendingDown className="h-4 w-4 text-red-500" /> }
                    ].map((stat, i) => (
                        <Card key={i} className="bg-slate-950/40 border-slate-800 backdrop-blur-md">
                            <CardHeader className="py-4 px-6">
                                <CardDescription className="text-[10px] font-mono uppercase tracking-[0.2em] text-slate-500">{stat.label}</CardDescription>
                                <div className="flex items-center justify-between mt-1">
                                    <div className={`text-2xl font-black font-mono ${stat.trend === true ? 'text-green-400' : (stat.trend === false ? 'text-red-400' : 'text-white')}`}>
                                        {stat.trend === true && '+'}{stat.value}
                                    </div>
                                    {stat.icon}
                                </div>
                                <div className="text-[8px] font-mono text-slate-600 mt-1">{stat.sub}</div>
                            </CardHeader>
                        </Card>
                    ))}
                </div>
            )}

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                {/* Left Column: Recent Filings Table */}
                <div className="xl:col-span-2 space-y-8">
                    <Tabs defaultValue="all" className="w-full">
                        <div className="flex items-center justify-between mb-4">
                            <TabsList className="bg-slate-950 border border-slate-800">
                                <TabsTrigger value="all" className="data-[state=active]:bg-blue-600 text-xs font-mono uppercase px-4">All Filings</TabsTrigger>
                                <TabsTrigger value="exits" className="data-[state=active]:bg-red-600 text-xs font-mono uppercase px-4">Distribution Scan</TabsTrigger>
                            </TabsList>
                            <span className="text-[10px] font-mono text-slate-600 uppercase">Buffer: 4.8 GBps // Local_Time: {new Date().toLocaleTimeString()}</span>
                        </div>

                        <TabsContent value="all" className="mt-0">
                            <Card className="bg-slate-950/40 border-slate-800 backdrop-blur-md">
                                <CardHeader className="p-4 border-b border-slate-900">
                                    <CardTitle className="text-sm font-mono flex items-center gap-2">
                                        <Users className="h-4 w-4 text-blue-500" /> RAW_SEC_FILING_STREAM
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <Table>
                                        <TableHeader className="bg-slate-900/30">
                                            <TableRow className="border-slate-800">
                                                <TableHead className="text-[10px] font-mono uppercase">Holder</TableHead>
                                                <TableHead className="text-[10px] font-mono uppercase text-center">Asset</TableHead>
                                                <TableHead className="text-[10px] font-mono uppercase text-center">Action</TableHead>
                                                <TableHead className="text-[10px] font-mono uppercase text-right">Shares Δ</TableHead>
                                                <TableHead className="text-[10px] font-mono uppercase text-right">Value ($M)</TableHead>
                                            </TableRow>
                                        </TableHeader>
                                        <TableBody>
                                            {filings.map((f, idx) => (
                                                <TableRow key={idx} className="border-slate-900 hover:bg-slate-800/20 group h-12">
                                                    <TableCell className="text-xs font-medium text-slate-200">{f.holder}</TableCell>
                                                    <TableCell className="text-center">
                                                        <span className="font-mono font-black text-white px-2 py-0.5 border border-slate-800 rounded bg-black/40 text-xs tracking-tighter group-hover:border-blue-500 transition-colors">
                                                            {f.ticker}
                                                        </span>
                                                    </TableCell>
                                                    <TableCell className="text-center">
                                                        <Badge className={`${f.action === 'BUY' ? 'bg-green-500/10 text-green-500 border-green-500/20' : (f.action === 'SELL' ? 'bg-red-500/10 text-red-500 border-red-500/20' : 'bg-slate-800 text-slate-400')} text-[8px] font-bold h-4`}>
                                                            {f.action}
                                                        </Badge>
                                                    </TableCell>
                                                    <TableCell className={`text-right font-mono text-[10px] ${f.shares_changed >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                                        {f.shares_changed !== 0 ? (f.shares_changed > 0 ? '+' : '') + f.shares_changed.toLocaleString() : '--'}
                                                    </TableCell>
                                                    <TableCell className="text-right font-mono text-white text-xs font-bold">${f.position_value_millions.toLocaleString()}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </CardContent>
                            </Card>
                        </TabsContent>
                        
                        <TabsContent value="exits" className="mt-0">
                            <WhaleSellingTable filings={filings} loading={loading} />
                        </TabsContent>
                    </Tabs>
                </div>

                {/* Right Column: Visual Analysis */}
                <div className="space-y-8">
                    {/* Crowd Indices */}
                    <div className="space-y-4">
                        <div className="flex items-center gap-2 mb-2">
                            <BarChart3 className="h-4 w-4 text-indigo-500" />
                            <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Sector Crowd Analysis</h3>
                        </div>
                        <div className="grid grid-cols-1 gap-4">
                            {crowding.slice(0, 3).map((sector) => (
                                <SectorCrowdingGauge key={sector.sector} sector={sector} />
                            ))}
                        </div>
                    </div>

                    {/* Historic Timeline */}
                    {crowding[0]?.history && (
                        <FilingDeltaTimeline history={crowding[0].history} />
                    )}

                    {/* System Meta */}
                    <Card className="bg-slate-950/80 border-slate-800 border-t-2 border-t-blue-500">
                        <CardContent className="p-4 space-y-4">
                            <div className="flex items-center gap-3">
                                <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]" />
                                <span className="text-[10px] font-mono text-slate-300 tracking-wider">SEC_ENDPOINT_STABLE</span>
                            </div>
                            <div className="space-y-1">
                                <div className="text-[8px] text-slate-600 uppercase tracking-widest">Encrypted_Bridge_ID</div>
                                <div className="text-[10px] font-mono text-slate-400 truncate">0xAF-1337-BH-99-WW-77-QX</div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default WhaleFlowTerminal;
