import React, { useState, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, TrendingDown, RefreshCcw, Activity } from "lucide-react";
import { notify } from "@/components/ui/use-toast";
import { motion } from "framer-motion";
import apiClient from '@/services/apiClient';

// Sub-components
import FragilityScoreCard from '@/components/cards/FragilityScoreCard';
import LiquidityTrapAlert from '@/components/alerts/LiquidityTrapAlert';
import SectorFragilityTable from '@/components/tables/SectorFragilityTable';
import PassiveConcentrationHeatmap from '@/components/charts/PassiveConcentrationHeatmap';

const ForcedSellerMonitor = () => {
    const [risks, setRisks] = useState([]);
    const [heatmap, setHeatmap] = useState([]);
    const [traps, setTraps] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");

    const fetchData = useCallback(async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const [risksRes, heatmapRes, trapsRes] = await Promise.all([
                apiClient.get('/market-data/forced-sellers'),
                apiClient.get('/market-data/forced-sellers/heatmap'),
                apiClient.get('/market-data/forced-sellers/liquidity-traps')
            ]);
            
            setRisks(risksRes || []);
            setHeatmap(heatmapRes || []);
            setTraps(trapsRes || []);
            
        } catch (error) {
            console.error("Failed to fetch data", error);
            notify({ 
                title: "Data Acquisition Error", 
                body: "Failed to load market fragility metrics.", 
                type: "error" 
            });
        } finally {
            if (!silent) setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => fetchData(true), 30000); // 30s background refresh
        return () => clearInterval(interval);
    }, [fetchData]);

    const filteredRisks = risks.filter(r => 
        r.ticker.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="p-8 space-y-8 max-w-[1600px] mx-auto text-slate-200">
            {/* Header Section */}
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 border-b border-slate-800 pb-8">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="p-2 bg-red-500/10 rounded-lg border border-red-500/20">
                            <TrendingDown className="h-6 w-6 text-red-500" />
                        </div>
                        <h1 className="text-4xl font-black tracking-tighter text-white uppercase italic">
                            Forced Seller <span className="text-red-600">Monitor</span>
                        </h1>
                    </div>
                    <p className="text-slate-400 font-mono text-sm max-w-2xl">
                        STRUCTURAL FRAGILITY PROTOCOL v4.0 // Analyzing passive ownership concentration and liquidity vacuum risks across industrial nodes.
                    </p>
                </div>
                
                <div className="flex items-center gap-4 w-full lg:w-auto">
                    <div className="relative flex-1 lg:w-80">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                        <Input 
                            placeholder="SCAN TICKER..." 
                            className="pl-10 bg-slate-900/50 border-slate-800 font-mono uppercase text-xs tracking-widest h-11"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <Button 
                        onClick={() => fetchData()} 
                        variant="outline" 
                        disabled={loading}
                        className="bg-slate-900 border-slate-700 hover:bg-slate-800 h-11 gap-2"
                    >
                        <RefreshCcw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                        <span className="hidden sm:inline font-mono text-xs tracking-tighter">REFRESH_CORE</span>
                    </Button>
                </div>
            </div>

            {/* Critical Alerts Layer */}
            <LiquidityTrapAlert traps={traps} />

            <Tabs defaultValue="overview" className="w-full">
                <div className="flex items-center justify-between mb-6">
                    <TabsList className="bg-slate-900/50 border border-slate-800 p-1">
                        <TabsTrigger value="overview" className="data-[state=active]:bg-indigo-600 font-mono text-xs px-6 uppercase tracking-widest">Risk Grid</TabsTrigger>
                        <TabsTrigger value="heatmap" className="data-[state=active]:bg-indigo-600 font-mono text-xs px-6 uppercase tracking-widest">Heatmap</TabsTrigger>
                        <TabsTrigger value="sectors" className="data-[state=active]:bg-indigo-600 font-mono text-xs px-6 uppercase tracking-widest">Sector Audit</TabsTrigger>
                    </TabsList>
                    
                    <div className="hidden md:flex items-center gap-2 text-[10px] font-mono text-slate-500 uppercase tracking-widest">
                        <Activity className="h-3 w-3 animate-pulse text-green-500" />
                        System Status: <span className="text-green-500">Live_Scan_Active</span>
                    </div>
                </div>

                {/* Grid View of Fragile Tickers */}
                <TabsContent value="overview" className="mt-0">
                    {loading && risks.length === 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-pulse">
                            {[...Array(8)].map((_, i) => (
                                <div key={i} className="h-48 rounded-xl bg-slate-900/50 border border-slate-800" />
                            ))}
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {filteredRisks.map((risk) => (
                                <FragilityScoreCard key={risk.ticker} data={risk} />
                            ))}
                            {filteredRisks.length === 0 && (
                                <div className="col-span-full py-20 text-center border-2 border-dashed border-slate-800 rounded-2xl">
                                    <p className="text-slate-500 font-mono uppercase tracking-widest">No structural anomalies detected for query.</p>
                                </div>
                            )}
                        </div>
                    )}
                </TabsContent>

                {/* Heatmap View */}
                <TabsContent value="heatmap" className="mt-0">
                    <PassiveConcentrationHeatmap data={heatmap} />
                </TabsContent>

                {/* Detailed Sector Table */}
                <TabsContent value="sectors" className="mt-0">
                    <SectorFragilityTable data={heatmap} loading={loading} />
                </TabsContent>
            </Tabs>

            {/* Industrial Footer/Status */}
            <div className="pt-12 border-t border-slate-800/50 flex flex-col sm:flex-row justify-between items-center gap-4 text-[10px] text-slate-600 font-mono uppercase tracking-[0.2em]">
                <div className="flex items-center gap-6">
                    <span>Alpha_Vantage_Node: EXT_READY</span>
                    <span>SEC_Edgar_13F: FETCH_SUCCESS</span>
                </div>
                <div>Last Convergence: {new Date().toLocaleTimeString()}</div>
            </div>
        </div>
    );
};

export default ForcedSellerMonitor;
