import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { AlertCircle, TrendingDown, ShieldAlert, RefreshCcw, Activity, Filter } from "lucide-react";
import { motion } from "framer-motion";
import apiClient from '@/services/apiClient';

// Sub-components
import PassiveConcentrationHeatmap from '@/components/Charts/PassiveConcentrationHeatmap';
import SectorFragilityTable from '@/components/tables/SectorFragilityTable';

const ForcedSellerMonitor = () => {
    const [stats, setStats] = useState(null);
    const [fragilityData, setFragilityData] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const [statsRes, fragilityRes] = await Promise.all([
                apiClient.get('/market-data/forced-sellers'),
                apiClient.get('/market-data/forced-sellers/fragility')
            ]);
            
            setStats(statsRes || null);
            setFragilityData(fragilityRes || []);
            
        } catch (error) {
            console.error("Failed to fetch forced seller data", error);
        } finally {
            if (!silent) setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => fetchData(true), 30000);
        return () => clearInterval(interval);
    }, [fetchData]);

    return (
        <div className="p-8 space-y-8 max-w-[1600px] mx-auto text-slate-200">
            {/* Header */}
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
                <div>
                    <h1 className="text-4xl font-black tracking-tighter text-white uppercase italic flex items-center gap-3">
                        <ShieldAlert className="h-10 w-10 text-red-600" />
                        Forced Seller <span className="text-red-600">Monitor</span>
                    </h1>
                    <p className="text-slate-400 font-mono text-sm mt-2 uppercase tracking-[0.2em] opacity-70">
                        Structural Vulnerability & Liquidation Risk Analysis // Institutional Flow Scan
                    </p>
                </div>
                <Button onClick={() => fetchData()} variant="outline" className="border-red-900/50 hover:bg-red-950/20">
                    <RefreshCcw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                    REFRESH_SCAN
                </Button>
            </div>

            {/* High Level Risk Pulse */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="bg-red-950/20 border-red-900/30">
                    <CardHeader className="pb-2">
                        <CardDescription className="text-red-400 font-mono text-xs uppercase">Aggregate Fragility</CardDescription>
                        <CardTitle className="text-4xl font-black text-white">{stats?.aggregate_fragility_score || '--'}/100</CardTitle>
                    </CardHeader>
                </Card>
                <Card className="bg-slate-950/40 border-slate-800">
                    <CardHeader className="pb-2">
                        <CardDescription className="text-slate-400 font-mono text-xs uppercase">Liquidation Pressure</CardDescription>
                        <CardTitle className="text-4xl font-black text-white">{stats?.liquid_pressure_index || '--'}</CardTitle>
                    </CardHeader>
                </Card>
                <Card className="bg-slate-950/40 border-slate-800">
                    <CardHeader className="pb-2">
                        <CardDescription className="text-slate-400 font-mono text-xs uppercase">High Risk Sectors</CardDescription>
                        <CardTitle className="text-4xl font-black text-white">{stats?.high_risk_sectors || 0}</CardTitle>
                    </CardHeader>
                </Card>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                {/* Heatmap Analysis */}
                <div className="space-y-4">
                    <div className="flex items-center gap-2 px-1">
                        <Activity className="h-4 w-4 text-red-500" />
                        <h3 className="text-xs font-black uppercase tracking-widest text-slate-400">Structural Vulnerability Heatmap</h3>
                    </div>
                    <PassiveConcentrationHeatmap data={fragilityData} />
                </div>

                {/* Fragility Table */}
                <div className="space-y-4">
                    <div className="flex items-center gap-2 px-1">
                        <Filter className="h-4 w-4 text-red-500" />
                        <h3 className="text-xs font-black uppercase tracking-widest text-slate-400">Sector Fragility Breakdown</h3>
                    </div>
                    <SectorFragilityTable data={fragilityData} loading={loading} />
                </div>
            </div>
        </div>
    );
};

export default ForcedSellerMonitor;
